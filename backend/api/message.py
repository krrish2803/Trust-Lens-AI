"""
TrustLens AI - Message & Text Scan API Endpoint
Analyzes SMS, Email body, WhatsApp messages, or raw text for scams.
"""

import re
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import MessageScanRequest, ScanResultResponse, ScanType, RiskLevel
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


@router.post("/message", response_model=ScanResultResponse)
async def scan_message(payload: MessageScanRequest):
    """
    Analyzes submitted SMS, WhatsApp message, email or text using Hinglish phrase library, 10-category rule engine, and NVIDIA AI.
    """
    text = payload.text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text content to scan cannot be empty."
        )

    # 1. Extract embedded URLs
    extracted_urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)

    # Layer 1: Hinglish Scam Phrase Library
    phrase_result = phrase_matcher_instance.detect(text)
    matched_phrases = [p.get("phrase") for p in phrase_result.get("phrases", [])]

    # Layer 2: Rule Engine
    rule_results = rule_engine.evaluate(text)

    # Layer 3: URL Analysis for extracted links
    url_risk_scores = []
    for u in extracted_urls:
        det = url_detector_instance.detect(u)
        url_risk_scores.append(float(det.get("risk_score", 0.0)) * 100.0)
    max_url_risk = max(url_risk_scores) if url_risk_scores else 0.0

    # Layer 6: Risk Scoring Engine
    phrase_score = len(matched_phrases) * 35.0
    rule_score = float(rule_results.get("rule_risk_score", 0.0))

    combined_risk = int(min(max(phrase_score * 0.4 + rule_score * 0.4 + max_url_risk * 0.2, 0), 100))

    # Determine Verdict
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

    # Scam Category
    categories = rule_results.get("categories_triggered", [])
    scam_category = categories[0] if categories else ("Phishing / Fraud Attempt" if combined_risk > 30 else "Safe Content")

    # Layer 5: NVIDIA AI Analysis
    ai_result = await ai_classifier.classify_content(
        text=text,
        detected_urls=extracted_urls,
        matched_phrases=matched_phrases,
        rule_findings=rule_results.get("findings", [])
    )

    ai_explanation = None
    if ai_result:
        ai_explanation = ai_result.get("explanation")
        if "risk_score" in ai_result:
            combined_risk = int((combined_risk * 0.6) + (ai_result["risk_score"] * 0.4))

    reasons = [f.get("finding") for f in rule_results.get("findings", [])]
    if phrase_result.get("explanation") and phrase_result["explanation"] not in reasons:
        reasons.append(phrase_result["explanation"])

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
        detected_urls=extracted_urls,
        ai_explanation=ai_explanation
    )

    actions = explainability_engine.generate_recommendations(
        verdict=verdict.value,
        scam_category=scam_category,
        has_url=bool(extracted_urls),
        has_otp_request="OTP" in scam_category or "otp" in text.lower(),
        has_financial_request="UPI" in scam_category or "Bank" in scam_category
    )

    scan_id = f"msg-{uuid.uuid4().hex[:8]}"
    summary = text[:70] + "..." if len(text) > 70 else text

    response_data = {
        "id": scan_id,
        "scan_type": ScanType.MESSAGE,
        "input_summary": summary,
        "risk_score": combined_risk,
        "confidence_score": confidence,
        "verdict": verdict,
        "scam_category": scam_category,
        "matched_phrases": matched_phrases,
        "detected_urls": extracted_urls,
        "reasons": reasons,
        "recommended_actions": actions,
        "extracted_text": text,
        "ai_explanation": explanation,
        "threat_breakdown": [
            {
                "layer": "Hinglish Phrase Library",
                "finding": f"Matched {len(matched_phrases)} scam phrases",
                "severity": verdict.value,
                "weight": 0.4
            },
            {
                "layer": "Rule Engine",
                "finding": f"Triggered {len(categories)} threat categories",
                "severity": verdict.value,
                "weight": 0.4
            }
        ],
        "created_at": datetime.utcnow().isoformat()
    }

    await history_repo.save_scan(response_data)

    return ScanResultResponse(**response_data)
