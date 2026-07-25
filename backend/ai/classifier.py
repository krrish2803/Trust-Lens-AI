"""
TrustLens AI - AI Scam Classifier Module
Orchestrates NVIDIA NIM LLM classification and fallback AI rule scoring.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from backend.ai.nvidia_client import nvidia_client
from backend.ai.prompt_builder import prompt_builder

logger = logging.getLogger("trustlens.ai.classifier")


class AIClassifier:
    def __init__(self):
        self.client = nvidia_client

    async def classify_content(
        self,
        text: str,
        detected_urls: List[str] = None,
        matched_phrases: List[str] = None,
        rule_findings: List[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Classifies input text using NVIDIA NIM model.
        Returns parsed JSON dict or None if API unavailable.
        """
        if not self.client.is_configured:
            return None

        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_analysis_prompt(
            text=text,
            detected_urls=detected_urls,
            matched_phrases=matched_phrases,
            rule_findings=rule_findings
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response_text = await self.client.generate_chat_completion(
            messages=messages,
            temperature=0.1,
            max_tokens=600
        )

        if not response_text:
            return None

        try:
            # Clean JSON markdown fences if present
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            parsed = json.loads(cleaned.strip())
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse NVIDIA NIM JSON response: {e}")
            return None


ai_classifier = AIClassifier()
