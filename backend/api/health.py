"""
TrustLens AI - Health Check API Endpoint
"""

from datetime import datetime
from fastapi import APIRouter
from backend.config import settings
from backend.database.mongodb import db_manager
from backend.ai.nvidia_client import nvidia_client
from backend.models.schemas import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def get_health():
    """
    Returns system status and connection state of DB, AI, and OCR modules.
    """
    db_status = "connected" if db_manager.is_connected else "degraded (in-memory)"
    ai_status = "configured (NVIDIA NIM)" if nvidia_client.is_configured else "rule-fallback"

    return HealthCheckResponse(
        status="healthy",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat(),
        components={
            "database": db_status,
            "ai_engine": ai_status,
            "ocr_engine": "ready"
        }
    )
