"""
TrustLens AI - Configuration Module
Manages application settings, environment variables, and default configuration values using Pydantic Settings.
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App Information
    APP_NAME: str = "TrustLens AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = "trustlens-super-secret-key-change-in-production-2026"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://trustlens-ai.vercel.app",
        "*"
    ]

    # Database Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "trustlens_db"

    # NVIDIA NIM AI Configuration
    NVIDIA_NIM_API_KEY: str = os.getenv("NVIDIA_NIM_API_KEY", "")
    NVIDIA_NIM_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL_NAME: str = "meta/llama-3.3-70b-instruct"

    # OCR Settings
    OCR_GPU: bool = False
    OCR_LANGUAGES: List[str] = ["en", "hi"]

    # Datasets Directory
    DATASETS_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "datasets")
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
