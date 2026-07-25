"""
TrustLens AI - Unified Scan Endpoint
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from backend.api.url import scan_url
from backend.api.message import scan_message
from backend.models.schemas import URLScanRequest, MessageScanRequest, ScanResultResponse

router = APIRouter()


class GenericScanRequest(BaseModel):
    input_text: str = Field(..., description="URL, Message, SMS, Email or text input")


@router.post("/", response_model=ScanResultResponse)
async def auto_scan(payload: GenericScanRequest):
    """
    Automatically detects input type (URL vs Text) and routes to appropriate analysis pipeline.
    """
    text = payload.input_text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scan input cannot be empty."
        )

    if text.startswith("http://") or text.startswith("https://") or text.startswith("www."):
        return await scan_url(URLScanRequest(url=text))
    else:
        return await scan_message(MessageScanRequest(text=text))
