"""
TrustLens AI - Image & Screenshot Scan API Endpoint
"""

import base64
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, status
from typing import Optional
from backend.models.schemas import ScanResultResponse, ScanType, RiskLevel
from backend.ocr.screenshot_parser import screenshot_parser
from backend.detection.phrase_matcher import PhraseMatcher
from backend.detection.rule_engine import rule_engine
from backend.detection.url_detector import URLDetector
from backend.ai.classifier import ai_classifier
from backend.ai.explainability import explainability_engine
from backend.ai.confidence_score import confidence_calculator
from backend.database.history import history_repo

router = APIRouter()
phrase_matcher_instance = PhraseMatcher()
url_detector_instance = URLDetector()


@router.post("/image", response_model=ScanResultResponse)
async def scan_image(
    file: Optional[UploadFile] = File(None),
    image_base64: Optional[str] = Form(None)
):
    """
    Extracts text from uploaded screenshot (EasyOCR) and feeds extracted content through the 8-layer detection pipeline.
    """
    image_bytes = None

    if file:
        image_bytes = await file.read()
    elif image_base64:
        try:
            cleaned_b64 = image_base64.split(",")[-1]
            image_bytes = base64.b64decode(cleaned_b64)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Base64 image payload."
            )

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide an image file or base64 string."
        )

    # Layer 4: EasyOCR Extraction
    parsed_ocr = screenshot_parser.parse_screenshot_bytes(image_bytes)
    extracted_text = parsed_ocr.get("raw_text", "").strip()

    if not extracted_text:
        # Fallback response for unreadable image
        return ScanResultResponse(
            id=f"img-{uuid.uuid4().hex[:8]}",
            scan_type=ScanType.IMAGE,
            input_summary="Uploaded Image / Screenshot",
            risk_score=0,
            confidence_score=0.7,
            verdict=RiskLevel.SAFE,
            scam_category="No Clear Text Detected",
            matched_phrases=[],
            detected_urls=[],
            reasons=["OCR scan completed but no readable text was detected."],
            recommended_actions=["Ensure image is clear, unblurred, and well-lit."],
            extracted_text="",
            ai_explanation="No text could be extracted from the uploaded screenshot.",
            created_at=datetime.utcnow().isoformat()
        )

    # Pipeline detection over extracted OCR text
    phrase_result = phrase_matcher_instance.detect(extracted_text)
    matched_phrases = [p.get("phrase") for p in phrase_result.get("phrases", [])]

    rule_results = rule_engine.evaluate(extracted_text)

    detected_urls = parsed_ocr.get("detected_urls", [])
    url_risk_scores = [float(url_detector_instance.detect(u).get("risk_score", 0.0)) * 100.0 for u in detected_urls]
    max_url_risk = max(url_risk_scores) if url_risk_scores else 0.0

    phrase_score = len(matched_phrases) * 35.0
    rule_score = float(rule_results.get("rule_risk_score", 0.0))

    combined_risk = int(min(max(phrase_score * 0.4 + rule_score * 0.4 + max_url_risk * 0.2, 0), 100))

    if combined_risk >= 80:
        verdict = RiskLevel.CRITICAL
    elif combined_risk >= 60:
        verdict = RiskLevel.HIGH_RISK
    elif combined_risk >= 35:
        verdict = RiskLevel.MEDIUM_RISK
    elif combined_risk >= 15:
        verdict = RiskLevel.LOW_RISK
    else:
        verdict = RiskLevel.SAFE

    categories = rule_results.get("categories_triggered", [])
    scam_category = categories[0] if categories else ("Screenshot Scam Attempt" if combined_risk > 30 else "Safe Screenshot")

    ai_result = await ai_classifier.classify_content(
        text=extracted_text,
        detected_urls=detected_urls,
        matched_phrases=matched_phrases,
        rule_findings=rule_results.get("findings", [])
    )

    ai_explanation = ai_result.get("explanation") if ai_result else None
    if ai_result and "risk_score" in ai_result:
        combined_risk = int((combined_risk * 0.6) + (ai_result["risk_score"] * 0.4))

    reasons = [f.get("finding") for f in rule_results.get("findings", [])]
    reasons.append(f"OCR Context: {parsed_ocr.get('screenshot_context', 'Screenshot')}")

    confidence = confidence_calculator.calculate(
        rule_score=rule_score,
        phrase_score=phrase_score,
        url_score=max_url_risk
    )

    explanation = explainability_engine.generate_explanation(
        risk_score=combined_risk,
        verdict=verdict.value,
        scam_category=scam_category,
        reasons=reasons,
        matched_phrases=matched_phrases,
        detected_urls=detected_urls,
        ai_explanation=ai_explanation
    )

    actions = explainability_engine.generate_recommendations(
        verdict=verdict.value,
        scam_category=scam_category,
        has_url=bool(detected_urls)
    )

    scan_id = f"img-{uuid.uuid4().hex[:8]}"

    response_data = {
        "id": scan_id,
        "scan_type": ScanType.IMAGE,
        "input_summary": f"Screenshot ({parsed_ocr.get('screenshot_context')})",
        "risk_score": combined_risk,
        "confidence_score": confidence,
        "verdict": verdict,
        "scam_category": scam_category,
        "matched_phrases": matched_phrases,
        "detected_urls": detected_urls,
        "reasons": reasons,
        "recommended_actions": actions,
        "extracted_text": extracted_text,
        "ai_explanation": explanation,
        "threat_breakdown": [
            {
                "layer": "OCR Text Extraction",
                "finding": f"Extracted {len(extracted_text)} chars from {parsed_ocr.get('screenshot_context')}",
                "severity": verdict.value,
                "weight": 0.3
            }
        ],
        "created_at": datetime.utcnow().isoformat()
    }

    await history_repo.save_scan(response_data)

    return ScanResultResponse(**response_data)
