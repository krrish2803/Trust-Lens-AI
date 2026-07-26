"""
TrustLens AI - Configuration Module
Manages application settings, environment variables, and default configuration values using Pydantic Settings.
"""

import os
import secrets
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App Information
    APP_NAME: str = "TrustLens AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = ""

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://trustlens-ai.vercel.app",
        "https://trustlens-ai-frontend.onrender.com",
        "https://trustlens-ai.onrender.com",
        "https://trust-lens-ai.netlify.app",
    ]

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 30
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # Input Limits
    MAX_TEXT_LENGTH: int = 50000
    MAX_URL_LENGTH: int = 2048
    MAX_IMAGE_SIZE_MB: int = 10

    # Database Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "trustlens_db"

    # NVIDIA NIM AI Configuration
    NVIDIA_NIM_API_KEY: str = ""
    NVIDIA_NIM_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL_NAME: str = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
    AI_TEMPERATURE: float = 0.1
    AI_MAX_TOKENS: int = 600

    # Detection Thresholds (unified across all endpoints)
    RISK_THRESHOLD_CRITICAL: int = 80
    RISK_THRESHOLD_HIGH: int = 60
    RISK_THRESHOLD_MEDIUM: int = 35
    RISK_THRESHOLD_LOW: int = 15

    # AI Blending Weight
    AI_BLEND_WEIGHT: float = 0.4

    # OCR Settings
    OCR_GPU: bool = False
    OCR_LANGUAGES: List[str] = ["en", "hi"]

    # Datasets Directory
    DATASETS_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "datasets")
    )

    def model_post_init(self, __context):
        if not self.SECRET_KEY:
            self.SECRET_KEY = secrets.token_hex(32)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
