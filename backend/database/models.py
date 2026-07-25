"""
TrustLens AI - Database Document Schemas
Defines database collection structures for history, users, and reports.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class HistoryDocument(BaseModel):
    id: str
    scan_type: str
    input_summary: str
    risk_score: int
    confidence_score: float
    verdict: str
    scam_category: str
    matched_phrases: List[str] = []
    detected_urls: List[str] = []
    reasons: List[str] = []
    recommended_actions: List[str] = []
    extracted_text: Optional[str] = None
    ai_explanation: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class UserDocument(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ReportDocument(BaseModel):
    id: str
    scan_id: str
    reporter_notes: Optional[str] = None
    scam_url_or_number: Optional[str] = None
    reported_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
