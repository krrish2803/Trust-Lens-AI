"""
TrustLens AI - Pydantic Request & Response Schemas
Defines request validation and structured API output formats.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ScanType(str, Enum):
    URL = "url"
    MESSAGE = "message"
    IMAGE = "image"


class RiskLevel(str, Enum):
    SAFE = "Safe"
    LOW_RISK = "Low Risk"
    MEDIUM_RISK = "Medium Risk"
    HIGH_RISK = "High Risk"
    CRITICAL = "Critical"


class ScamCategory(str, Enum):
    OTP_SCAM = "OTP Scam"
    KYC_SCAM = "KYC Scam"
    BANK_SCAM = "Bank Impersonation"
    DELIVERY_SCAM = "Delivery Scam"
    LOTTERY_SCAM = "Lottery & Prize Scam"
    UPI_SCAM = "UPI Fraud"
    INVESTMENT_SCAM = "Investment & Crypto Scam"
    JOB_SCAM = "Job & Work From Home Scam"
    LOAN_SCAM = "Fake Loan Scam"
    GOVT_SCAM = "Government & Law Enforcement Scam"
    PHISHING_URL = "Phishing URL / Fake Site"
    UNKNOWN = "Unknown / Suspicious"
    BENIGN = "Safe Content"


class ChannelType(str, Enum):
    AUTO = "auto"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    TEXT = "text"


# --- Request Models ---

class URLScanRequest(BaseModel):
    url: str = Field(
        ..., min_length=1, max_length=2048,
        description="The URL to scan for phishing or fraud",
        example="http://sbi-kyc-update.online",
    )


class MessageScanRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=50000,
        description="SMS, WhatsApp message, email body or text content to scan",
        example="Dear customer, your SBI account is blocked. Click here to update KYC immediately: http://bit.ly/fake-sbi",
    )
    channel: ChannelType = Field(
        ChannelType.AUTO,
        description="Communication channel: auto, sms, whatsapp, email, text",
    )


class ImageScanRequest(BaseModel):
    image_base64: Optional[str] = Field(None, description="Base64 encoded image string")


# --- Response Models ---

class ThreatDetail(BaseModel):
    layer: str
    finding: str
    severity: str
    weight: float


class ScanResultResponse(BaseModel):
    id: str = Field(..., description="Unique Scan ID")
    scan_type: ScanType
    input_summary: str
    risk_score: int = Field(..., ge=0, le=100, description="Risk Score from 0 (Safe) to 100 (Critical)")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Model confidence score")
    verdict: RiskLevel
    scam_category: str
    matched_phrases: List[str] = Field(default_factory=list)
    detected_urls: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    extracted_text: Optional[str] = None
    ai_explanation: Optional[str] = None
    threat_breakdown: List[ThreatDetail] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HistoryItem(BaseModel):
    id: str
    scan_type: str
    input_summary: str
    risk_score: int
    verdict: str
    scam_category: str
    created_at: str


class HealthCheckResponse(BaseModel):
    status: str
    app: str
    version: str
    timestamp: str
    components: Dict[str, str]
