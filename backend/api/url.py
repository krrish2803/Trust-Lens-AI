"""
TrustLens AI - URL Scan API Endpoint
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import URLScanRequest, ScanResultResponse, ScanType, RiskLevel
from backend.detection.url_detector import URLDetector
from backend.detection.rule_engine import rule_engine
from backend.ai.classifier import ai_classifier
from backend.ai.explainability import explainability_engine
from backend.ai.confidence_score import confidence_calculator
from backend.database.history import history_repo

router = APIRouter()
url_detector_instance = URLDetector()


@router.post("/url", response_model=ScanResultResponse)
async def scan_url(payload: URLScanRequest):
    """
    Analyzes submitted URL for phishing, brand spoofing, fake domains, IP links, and suspicious TLDs.
    """
    url_str = payload.url.strip()
    if not url_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL parameter cannot be empty."
        )

    # Layer 3: URL & Domain Analysis
    url_findings = url_detector_instance.detect(url_str)

    # Layer 2: Rule Engine
    rule_results = rule_engine.evaluate(url_str)

    # Threat aggregation
    is_phishing = url_findings.get("is_phishing", False)
    phishing_score = float(url_findings.get("risk_score", 0.0)) * 100.0
    rule_score = float(rule_results.get("rule_risk_score", 0.0))

    combined_risk = int(min(max(phishing_score * 0.7 + rule_score * 0.3, 0), 100))

    if combined_risk >= 85:
        verdict = RiskLevel.CRITICAL
    elif combined_risk >= 65:
        verdict = RiskLevel.HIGH_RISK
    elif combined_risk >= 40:
        verdict = RiskLevel.MEDIUM_RISK
    elif combined_risk >= 15:
        verdict = RiskLevel.LOW_RISK
    else:
        verdict = RiskLevel.SAFE

    scam_category = "Phishing URL / Fake Site" if combined_risk > 30 else "Safe Content"

    reasons = url_findings.get("findings", [])
    if not reasons and rule_results.get("findings"):
        reasons = [f.get("finding") for f in rule_results.get("findings")]

    # Layer 5: NVIDIA AI Analysis (Optional deep check)
    ai_result = await ai_classifier.classify_content(
        text=url_str,
        detected_urls=[url_str]
    )

    ai_explanation = None
    if ai_result:
        ai_explanation = ai_result.get("explanation")
        if "risk_score" in ai_result:
            combined_risk = int((combined_risk + ai_result["risk_score"]) / 2)

    confidence = confidence_calculator.calculate(
        rule_score=rule_score,
        phrase_score=0.0,
        url_score=phishing_score
    )

    explanation = explainability_engine.generate_explanation(
        risk_score=combined_risk,
        verdict=verdict.value,
        scam_category=scam_category,
        reasons=reasons,
        matched_phrases=[],
        detected_urls=[url_str],
        ai_explanation=ai_explanation
    )

    actions = explainability_engine.generate_recommendations(
        verdict=verdict.value,
        scam_category=scam_category,
        has_url=True
    )

    scan_id = f"url-{uuid.uuid4().hex[:8]}"

    response_data = {
        "id": scan_id,
        "scan_type": ScanType.URL,
        "input_summary": url_str,
        "risk_score": combined_risk,
        "confidence_score": confidence,
        "verdict": verdict,
        "scam_category": scam_category,
        "matched_phrases": [],
        "detected_urls": [url_str],
        "reasons": reasons,
        "recommended_actions": actions,
        "extracted_text": None,
        "ai_explanation": explanation,
        "threat_breakdown": [
            {
                "layer": "URL Analysis",
                "finding": f"Phishing risk score: {url_findings.get('risk_score', 0)}",
                "severity": verdict.value,
                "weight": 0.7
            }
        ],
        "created_at": datetime.utcnow().isoformat()
    }

    # Save to history DB asynchronously
    await history_repo.save_scan(response_data)

    return ScanResultResponse(**response_data)
