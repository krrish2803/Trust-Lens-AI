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
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.startswith("nvapi-"))

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def generate_chat_completion(
        self,
        messages: list,
        temperature: float = None,
        max_tokens: int = None,
    ) -> Optional[str]:
        if not self.is_configured:
            logger.info("NVIDIA NIM API key not configured. Using rule-based fallback.")
            return None

        temperature = temperature or settings.AI_TEMPERATURE
        max_tokens = max_tokens or settings.AI_MAX_TOKENS

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
            "top_p": 0.95,
        }

        try:
            client = self._get_client()
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )

            if response.status_code == 200:
                data = response.json()
                choices = data.get("choices", [])
                if choices and "message" in choices[0]:
                    return choices[0]["message"].get("content", "").strip()
            else:
                logger.warning(
                    "NVIDIA NIM API returned status %d", response.status_code
                )
                return None
        except Exception as e:
            logger.error("Error calling NVIDIA NIM API: %s", type(e).__name__)
            return None


nvidia_client = NvidiaNimClient()
