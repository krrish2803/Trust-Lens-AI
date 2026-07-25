"""
TrustLens AI - NVIDIA NIM API Async Client
Handles async communication with NVIDIA NIM inference API (Llama-3.3-70B-Instruct).
Provides graceful fallback when API keys are missing or offline.
"""

import logging
import httpx
from typing import Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger("trustlens.ai.nvidia")


class NvidiaNimClient:
    def __init__(self):
        self.api_key = settings.NVIDIA_NIM_API_KEY
        self.base_url = settings.NVIDIA_NIM_BASE_URL
        self.model_name = settings.NVIDIA_MODEL_NAME
        self.timeout = 15.0

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.startswith("nvapi-"))

    async def generate_chat_completion(
        self,
        messages: list,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Sends chat completion request to NVIDIA NIM API.
        Returns the text response or None if request fails or is unconfigured.
        """
        if not self.is_configured:
            logger.info("NVIDIA NIM API key not configured. Using rule-based fallback.")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.95
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if choices and "message" in choices[0]:
                        return choices[0]["message"].get("content", "").strip()
                else:
                    logger.warning(
                        f"NVIDIA NIM API returned status {response.status_code}: {response.text}"
                    )
                    return None
        except Exception as e:
            logger.error(f"Error calling NVIDIA NIM API: {str(e)}")
            return None


nvidia_client = NvidiaNimClient()
