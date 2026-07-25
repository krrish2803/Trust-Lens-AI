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

    @staticmethod
    def normalize_ocr_text(text: str) -> str:
        """Fix common OCR misreads for Indian scam detection context."""
        replacements = [
            (r'0TP', 'OTP'),
            (r'\b0tp\b', 'OTP'),
            (r'UPl', 'UPI'),
            (r'\bupl\b', 'UPI'),
            (r'Fs\s*(\d)', r'Rs \1'),
            (r'\bDDD\b', '000'),
            (r'5DDD', '5000'),
            (r'1DDD', '1000'),
            (r'2DDD', '2000'),
            (r'3DDD', '3000'),
            (r'4DDD', '4000'),
            (r'6DDD', '6000'),
            (r'7DDD', '7000'),
            (r'8DDD', '8000'),
            (r'9DDD', '9000'),
            (r'\bla\b', 'be'),
            (r'\bLa\b', 'be'),
            (r'\bwill\s+be\s+La\b', 'will be'),
            (r'\bwill\s+La\b', 'will be'),
            (r'accountwill', 'account will'),
            (r'\b1098', ' to 98'),
            (r'OTP10', 'OTP to '),
            (r'OTP1', 'OTP to '),
            (r'\bhttp\s*I\b', 'http://'),
            (r'\bhttp\s*l\b', 'http://'),
            (r'\bhttp\s*:\s*/\s*/', 'http://'),
            (r'\bkyc\s+kyc\b', 'kyc'),
            (r'\bupdate\s+online\b', 'update.com'),
            (r'\bupdate\s+com\b', 'update.com'),
            (r'KYC\s+update', 'KYC update'),
            (r'sbi\s*kyc\s*update', 'sbi-kyc-update'),
            (r'accountwill', 'account will'),
            (r'willbe', 'will be'),
            (r'cant', "can't"),
            (r'\bBLOCKED\b', 'BLOCKED'),
            (r'\bBLOCKED1\b', 'BLOCKED'),
            (r'\bIMMEDIATELY\b', 'IMMEDIATELY'),
            (r'\bIMMEDIATE\b', 'IMMEDIATELY'),
            (r'\bSUSPENSION\b', 'SUSPENSION'),
            (r'\bSUSPEN510N\b', 'SUSPENSION'),
            (r'\bBLOCK510N\b', 'BLOCKED'),
            (r'\baccount\s+will\s+be\s+BLOCKED\b', 'account will be BLOCKED'),
        ]
        normalized = text
        for pattern, replacement in replacements:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        return normalized

    def parse_screenshot_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Processes screenshot image, extracts text via OCR, and parses entities.
        """
        enhanced_bytes = self.preprocessor.preprocess_bytes(image_bytes)
        ocr_result = self.reader.extract_text_from_bytes(enhanced_bytes)

        raw_text = ocr_result.get("text", "")

        # Fix common OCR misreads
        raw_text = self.normalize_ocr_text(raw_text)

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
