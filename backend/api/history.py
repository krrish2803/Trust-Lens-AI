"""
TrustLens AI - Scan History API Router
"""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from backend.database.history import history_repo

router = APIRouter()


@router.get("/history")
async def get_scan_history(
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """
    Returns scan history records sorted by creation timestamp.
    """
    records = await history_repo.get_history(limit=limit, skip=skip)
    return {"status": "success", "count": len(records), "data": records}


@router.get("/history/{scan_id}")
async def get_scan_details(scan_id: str):
    """
    Retrieves detailed scan record by ID.
    """
    doc = await history_repo.get_scan_by_id(scan_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan record with ID {scan_id} not found."
        )
    return doc
