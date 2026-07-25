"""
TrustLens AI - Unified Scan Endpoint
"""

import re
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from backend.api.url import scan_url
from backend.api.message import scan_message
from backend.models.schemas import URLScanRequest, MessageScanRequest, ScanResultResponse

router = APIRouter()

_URL_PATTERN = re.compile(r'^(https?://|www\.)', re.IGNORECASE)


class GenericScanRequest(BaseModel):
    input_text: str = Field(
        ..., min_length=1, max_length=50000,
        description="URL, Message, SMS, Email or text input",
    )


@router.post("/", response_model=ScanResultResponse)
async def auto_scan(payload: GenericScanRequest):
    text = payload.input_text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scan input cannot be empty.",
        )

    if _URL_PATTERN.match(text):
        return await scan_url(URLScanRequest(url=text))
    else:
        return await scan_message(MessageScanRequest(text=text))
