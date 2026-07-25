"""
TrustLens AI - EasyOCR Image Reader Module
Extracts text from screenshots (SMS, WhatsApp, Banking app, UPI receipts, Web pages) using EasyOCR.
Supports Hindi and English languages with graceful fallbacks.
"""

import io
import logging
import numpy as np
from PIL import Image
from typing import Optional, List, Dict, Any
from backend.config import settings

logger = logging.getLogger("trustlens.ocr.reader")

# Lazy-loaded EasyOCR reader instance
_easyocr_reader = None


def get_ocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            logger.info("Initializing EasyOCR reader (Languages: en, hi)...")
            _easyocr_reader = easyocr.Reader(
                settings.OCR_LANGUAGES,
                gpu=settings.OCR_GPU
            )
        except Exception as e:
            logger.warning(f"EasyOCR initialization failed: {e}. OCR will operate in fallback mode.")
            _easyocr_reader = False
    return _easyocr_reader


class OCRImageReader:
    def __init__(self):
        pass

    def extract_text_from_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Processes image bytes using EasyOCR.
        Returns extracted text, confidence list, and bounding boxes.
        """
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img_np = np.array(image)
        except Exception as e:
            logger.error(f"Invalid image file: {e}")
            return {"text": "", "confidence": 0.0, "lines": []}

        reader = get_ocr_reader()

        if reader:
            try:
                results = reader.readtext(img_np)
                extracted_lines = []
                confidences = []

                for bbox, text, conf in results:
                    if text and text.strip():
                        extracted_lines.append(text.strip())
                        confidences.append(float(conf))

                full_text = "\n".join(extracted_lines)
                avg_confidence = float(np.mean(confidences)) if confidences else 0.0

                return {
                    "text": full_text,
                    "confidence": round(avg_confidence, 2),
                    "lines": extracted_lines
                }
            except Exception as e:
                logger.error(f"Error during EasyOCR execution: {e}")

        # Fallback if EasyOCR fails or is unconfigured
        return {
            "text": "",
            "confidence": 0.0,
            "lines": []
        }


ocr_reader = OCRImageReader()
