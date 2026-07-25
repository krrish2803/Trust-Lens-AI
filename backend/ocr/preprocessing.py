"""
TrustLens AI - Image Preprocessing Module
Prepares screenshots for OCR text extraction (contrast adjustment, resizing, noise reduction).
"""

import cv2
import numpy as np
from PIL import Image
import io


class ImagePreprocessor:
    @staticmethod
    def preprocess_bytes(image_bytes: bytes) -> bytes:
        """
        Enhances image contrast and binarization for higher OCR accuracy.
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return image_bytes

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply adaptive thresholding / contrast scaling
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)

            # Encode back to PNG bytes
            _, encoded_img = cv2.imencode('.png', enhanced)
            return encoded_img.tobytes()
        except Exception:
            return image_bytes


image_preprocessor = ImagePreprocessor()
