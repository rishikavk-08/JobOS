import html
import re
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

import psycopg
from psycopg.types.json import Jsonb

from .database import get_connection

SOURCE_NAME = "LinkedIn (Apify)"
MAX_REPORTED_FAILURES = 50

COMPANY_KEYS = ["companyName", "company", "company_name"]
TITLE_KEYS = ["title", "jobTitle", "positionName", "position"]
URL_KEYS = ["link", "jobUrl", "job_url", "url", "applyUrl"]
LOCATION_KEYS = ["location", "jobLocation", "formattedLocation"]
PLAIN_DESC_KEYS = ["descriptionText", "description", "jobDescription"]
HTML_DESC_KEYS = ["descriptionHtml"]


def _first(record: dict, keys: list[str]) -> Optional[str]:
    for key in keys:
        value = record.get(key)
        if isinstance(value, dict):
            value = value.get("name") or value.get("text")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _html_to_text(value: str) -> str:
    value = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</div>", "\n", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n\s*\n+", "\n\n", value)
    return value.strip()


def normalize_url(raw: str) -> Optional[str]:
    parts = urlsplit(raw.strip())
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return None
    host = parts.netloc.lower()
    path = parts.path.rstrip("/")
    # LinkedIn query strings are tracking params; other sites may need theirs.
    query = "" if host.endswith("linkedin.com") else parts.query
    return urlunsplit((parts.scheme, host, path, query, ""))


def map_item(item) -> tuple[Optional[dict], Optional[str]]:
    """Map one Apify record to a JobOS job. Returns (job, error)."""
    if not isinstance(item, dict):
        return None, "record is not a JSON object"

    company = _first(item, COMPANY_KEYS)
    title = _first(item, TITLE_KEYS)
    raw_url = _first(item, URL_KEYS)

    missing = [n for n, v in (("company", company), ("title", title), ("job_url", raw_url)) if not v]
    if missing:
        return None, f"missing required field(s): {', '.join(missing)}"

    job_url = normalize_url(raw_url)
    if not job_url:
        return None, f"invalid job URL: {raw_url!r}"

    description = _first(item, PLAIN_DESC_KEYS)
    if not description:
        html_desc = _first(item, HTML_DESC_KEYS)
        description = _html_to_text(html_desc) if html_desc else ""

    return {
        "company": company,
        "title": title,
        "job_url": job_url,
        "location": _first(item, LOCATION_KEYS) or "",
        "raw_description": description,
        "source": SOURCE_NAME,
    }, None


def _has_raw_payload_column(conn) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'jobs'
              AND column_name = 'raw_payload'
              AND data_type = 'jsonb'
            """
        )
        return cur.fetchone() is not None


_INSERT_BASE = """
INSERT INTO jobs (company, title, location, raw_description, source, job_url{extra_cols})
SELECT %s::text, %s::text, %s::text, %s::text, %s::text, %s::text{extra_vals}
WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE job_url = %s::text)
RETURNING id
"""


def ingest_items(items: list) -> dict:
    summary = {
        "fetched": len(items),
        "inserted": 0,
        "skipped_duplicates": 0,
        "failed_validation": 0,
        "failed_db": 0,
        "raw_payload_preserved": False,
        "inserted_ids": [],
        "failures": [],
    }

    def record_failure(index: int, reason: str):
        if len(summary["failures"]) < MAX_REPORTED_FAILURES:
            summary["failures"].append({"index": index, "reason": reason})

    seen_urls: set[str] = set()

    with get_connection() as conn:
        use_raw = _has_raw_payload_column(conn)
        summary["raw_payload_preserved"] = use_raw
        sql = _INSERT_BASE.format(
            extra_cols=", raw_payload" if use_raw else "",
            extra_vals=", %s::jsonb" if use_raw else "",
        )

        for index, item in enumerate(items):
            job, error = map_item(item)
            if error:
                summary["failed_validation"] += 1
                record_failure(index, error)
                continue

            if job["job_url"] in seen_urls:
                summary["skipped_duplicates"] += 1
                continue
            seen_urls.add(job["job_url"])

            params = [
                job["company"], job["title"], job["location"],
                job["raw_description"], job["source"], job["job_url"],
            ]
            if use_raw:
                params.append(Jsonb(item))
            params.append(job["job_url"])  # for the NOT EXISTS check

            try:
                with conn.transaction():  # savepoint: one bad row can't abort the batch
                    with conn.cursor() as cur:
                        cur.execute(sql, params)
                        row = cur.fetchone()
            except psycopg.Error as exc:
                summary["failed_db"] += 1
                record_failure(index, f"database error: {exc.__class__.__name__}")
                continue

            if row is None:
                summary["skipped_duplicates"] += 1
            else:
                summary["inserted"] += 1
                summary["inserted_ids"].append(row[0])

    return summary
