import os

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_BASE_URL = "https://api.apify.com/v2"
PAGE_SIZE = 500
REQUEST_TIMEOUT = 60


class ApifyError(Exception):
    """Apify returned an error or was unreachable."""


class ApifyConfigError(ApifyError):
    """Apify is not configured (e.g. missing token)."""


class ApifyRunNotReady(ApifyError):
    """The Apify run has not finished successfully."""


def _headers() -> dict:
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise ApifyConfigError("APIFY_API_TOKEN is not set in the environment")
    return {"Authorization": f"Bearer {token}"}


def _get(path: str, params: dict | None = None) -> requests.Response:
    try:
        response = requests.get(
            f"{APIFY_BASE_URL}{path}",
            headers=_headers(),
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        raise ApifyError(f"Apify returned HTTP {status} for {path}") from exc
    except requests.RequestException as exc:
        raise ApifyError(f"Could not reach Apify: {exc}") from exc


def get_run_dataset_id(run_id: str) -> str:
    """Resolve an Actor run ID to its default dataset ID."""
    data = _get(f"/actor-runs/{run_id}").json().get("data", {})
    status = data.get("status")
    if status != "SUCCEEDED":
        raise ApifyRunNotReady(f"Run {run_id} status is {status!r}, not SUCCEEDED")
    dataset_id = data.get("defaultDatasetId")
    if not dataset_id:
        raise ApifyError(f"Run {run_id} has no defaultDatasetId")
    return dataset_id


def fetch_dataset_items(dataset_id: str, max_items: int = 1000) -> list:
    """Fetch up to max_items records from a dataset, paginating."""
    items: list = []
    offset = 0
    while len(items) < max_items:
        limit = min(PAGE_SIZE, max_items - len(items))
        page = _get(
            f"/datasets/{dataset_id}/items",
            params={"format": "json", "clean": "true", "offset": offset, "limit": limit},
        ).json()
        if not isinstance(page, list):
            raise ApifyError("Unexpected dataset response (expected a JSON list)")
        items.extend(page)
        if len(page) < limit:
            break
        offset += len(page)
    return items
