import re
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator

from .apify_client import (
    ApifyConfigError,
    ApifyError,
    ApifyRunNotReady,
    fetch_dataset_items,
    get_run_dataset_id,
)
from .job_ingestion import ingest_items

router = APIRouter()

_ID_PATTERN = re.compile(r"^[A-Za-z0-9~_-]+$")


class ApifyIngestRequest(BaseModel):
    dataset_id: Optional[str] = None
    run_id: Optional[str] = None
    max_items: int = Field(default=1000, ge=1, le=5000)

    @model_validator(mode="after")
    def check_ids(self):
        if bool(self.dataset_id) == bool(self.run_id):
            raise ValueError("Provide exactly one of dataset_id or run_id")
        for value in (self.dataset_id, self.run_id):
            if value and not _ID_PATTERN.match(value):
                raise ValueError("Invalid Apify ID format")
        return self


@router.post("/ingest/apify")
def ingest_apify(request: ApifyIngestRequest):
    try:
        dataset_id = request.dataset_id or get_run_dataset_id(request.run_id)
        items = fetch_dataset_items(dataset_id, request.max_items)
    except ApifyConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except ApifyRunNotReady as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except ApifyError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    summary = ingest_items(items)
    return {"dataset_id": dataset_id, **summary}
