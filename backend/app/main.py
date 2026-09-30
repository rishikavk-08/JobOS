from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .ingest_routes import router as ingest_router   # add with the other imports at the top

app.include_router(ingest_router)                      # add right after app.add_middleware(...)

from .database import get_connection
from .ai_analyzer import analyze_job

app = FastAPI(
    title="JobOS API",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "JobOS API"
    }


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    company,
                    title,
                    job_url,
                    location,
                    source,
                    status,
                    fit_score,
                    fit_category
                FROM jobs
                WHERE id = %s
                """,
                (job_id,)
            )

            job = cur.fetchone()

            if job is None:
                raise HTTPException(
                    status_code=404,
                    detail="Job not found"
                )

            columns = [desc.name for desc in cur.description]

            return dict(zip(columns, job))


@app.get("/jobs/{job_id}/analysis")
def get_job_analysis(job_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    company,
                    title,
                    job_url,
                    location,
                    source,
                    status,
                    fit_score,
                    fit_category
                FROM jobs
                WHERE id = %s
                """,
                (job_id,)
            )

            job = cur.fetchone()

            if job is None:
                raise HTTPException(
                    status_code=404,
                    detail="Job not found"
                )

            job_columns = [desc.name for desc in cur.description]
            job_data = dict(zip(job_columns, job))

            cur.execute(
                """
                SELECT
                    id,
                    requirement,
                    requirement_type,
                    importance,
                    matched,
                    match_score,
                    reasoning,
                    evidence_ids
                FROM job_requirements
                WHERE job_id = %s
                ORDER BY id
                """,
                (job_id,)
            )

            requirements = cur.fetchall()
            requirement_columns = [desc.name for desc in cur.description]

            requirement_data = [
                dict(zip(requirement_columns, row))
                for row in requirements
            ]

            return {
                "job": job_data,
                "requirements": requirement_data
            }

@app.post("/jobs/{job_id}/analyze")
def analyze_job_endpoint(job_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT raw_description
                FROM jobs
                WHERE id = %s
                """,
                (job_id,)
            )

            job = cur.fetchone()

            if job is None:
                raise HTTPException(
                    status_code=404,
                    detail="Job not found"
                )

            job_description = job[0]

            cur.execute(
                """
                SELECT id, title, description, metric_value, metric_unit
                FROM evidence
                ORDER BY id
                """
            )

            evidence_rows = cur.fetchall()

            evidence_text = "\n".join(
                f"[Evidence {row[0]}] {row[1]}: {row[2]} "
                f"({row[3] or ''} {row[4] or ''})"
                for row in evidence_rows
            )

    analysis = analyze_job(
        job_description,
        evidence_text
    )

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Remove previous AI-generated requirements
            cur.execute(
                "DELETE FROM job_requirements WHERE job_id = %s",
                (job_id,)
            )

            # Save each requirement
            for req in analysis["requirements"]:
                cur.execute(
                    """
                    INSERT INTO job_requirements (
                        job_id,
                        requirement,
                        requirement_type,
                        importance,
                        matched,
                        match_score,
                        evidence_ids,
                        reasoning
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        job_id,
                        req["requirement"],
                        "AI_ANALYZED",
                        req["importance"],
                        req["matched"],
                        req["match_score"],
                        req["evidence_ids"],
                        req["reasoning"]
                    )
                )

            # Save/update overall opportunity analysis
            cur.execute(
                """
                INSERT INTO opportunity_analyses (
                    job_id,
                    overall_opportunity_score,
                    decision,
                    reasoning
                )
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (job_id)
                DO UPDATE SET
                    overall_opportunity_score = EXCLUDED.overall_opportunity_score,
                    decision = EXCLUDED.decision,
                    reasoning = EXCLUDED.reasoning,
                    updated_at = NOW()
                """,
                (
                    job_id,
                    analysis["fit_score"],
                    analysis["recommendation"],
                    analysis["reasoning"]
                )
            )

    return {
        "job_id": job_id,
        "analysis": analysis,
        "saved": True
    }
from pydantic import BaseModel


class JobCreate(BaseModel):
    company: str
    title: str
    location: str
    raw_description: str
    source: str = "Manual"


@app.post("/jobs")
def create_job(job: JobCreate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO jobs
                (company, title, location, raw_description, source)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, company, title, location, source, status;
                """,
                (
                    job.company,
                    job.title,
                    job.location,
                    job.raw_description,
                    job.source,
                ),
            )

            result = cur.fetchone()
            conn.commit()

            return {
                "id": result[0],
                "company": result[1],
                "title": result[2],
                "location": result[3],
                "source": result[4],
                "status": result[5],
            }

    finally:
        conn.close()
