"""
TrustLens AI - Screenshot Parser Module
Parses screenshot text output into structured entities (URLs, Phone numbers, Amounts, UPI IDs, App types).
"""

import re
from typing import Dict, Any, List
from backend.ocr.image_reader import ocr_reader
from backend.ocr.preprocessing import image_preprocessor


class ScreenshotParser:
    def __init__(self):
        self.reader = ocr_reader
        self.preprocessor = image_preprocessor

    def parse_screenshot_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Processes screenshot image, extracts text via OCR, and parses entities.
        """
        enhanced_bytes = self.preprocessor.preprocess_bytes(image_bytes)
        ocr_result = self.reader.extract_text_from_bytes(enhanced_bytes)

        raw_text = ocr_result.get("text", "")

        # Entity Extraction
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', raw_text)
        phones = re.findall(r'\+?\d{10,12}', raw_text)
        upi_ids = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z]{2,}', raw_text)
        amounts = re.findall(r'(?:Rs\.?|\u20b9|INR)\s*[\d,]+', raw_text, re.IGNORECASE)

        # Detect app screenshot context
        text_lower = raw_text.lower()
        screenshot_context = "General Image"
        if "whatsapp" in text_lower or "chat" in text_lower:
            screenshot_context = "WhatsApp Chat"
        elif "messages" in text_lower or "sms" in text_lower:
            screenshot_context = "SMS Message"
        elif "paytm" in text_lower or "phonepe" in text_lower or "gpay" in text_lower:
            screenshot_context = "UPI / Payment App"
        elif "sbi" in text_lower or "hdfc" in text_lower or "icici" in text_lower:
            screenshot_context = "Banking App"

        return {
            "raw_text": raw_text,
            "ocr_confidence": ocr_result.get("confidence", 0.0),
            "detected_urls": list(set(urls)),
            "detected_phones": list(set(phones)),
            "detected_upi_ids": list(set(upi_ids)),
            "detected_amounts": list(set(amounts)),
            "screenshot_context": screenshot_context
        }


screenshot_parser = ScreenshotParser()
