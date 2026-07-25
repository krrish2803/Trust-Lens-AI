"""
TrustLens AI - URL Scan API Endpoint
"""

import re
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from backend.config import settings
from backend.models.schemas import URLScanRequest, ScanResultResponse, ScanType, RiskLevel
from backend.detection.url_detector import URLDetector
from backend.detection.domain_checker import DomainChecker
from backend.detection.rule_engine import rule_engine
from backend.detection.scam_classifier import ScamClassifier
from backend.detection.risk_engine import RiskEngine
from backend.ai.classifier import ai_classifier
from backend.ai.explainability import explainability_engine
from backend.ai.confidence_score import confidence_calculator
from backend.database.history import history_repo

router = APIRouter()
url_detector_instance = URLDetector()
domain_checker_instance = DomainChecker()
scam_classifier_instance = ScamClassifier()
risk_engine_instance = RiskEngine()

# Pre-compile regex for URL extraction
_URL_RE = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')


def _classify_risk(score: int) -> RiskLevel:
    if score >= settings.RISK_THRESHOLD_CRITICAL:
        return RiskLevel.CRITICAL
    elif score >= settings.RISK_THRESHOLD_HIGH:
        return RiskLevel.HIGH_RISK
    elif score >= settings.RISK_THRESHOLD_MEDIUM:
        return RiskLevel.MEDIUM_RISK
    elif score >= settings.RISK_THRESHOLD_LOW:
        return RiskLevel.LOW_RISK
    return RiskLevel.SAFE


@router.post("/url", response_model=ScanResultResponse)
async def scan_url(payload: URLScanRequest):
    url_str = payload.url.strip()
    if not url_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL parameter cannot be empty.",
        )

    url_findings = url_detector_instance.detect(url_str)
    rule_results = rule_engine.evaluate(url_str)

    # Domain reputation check
    domain_check = domain_checker_instance.check(url_str)
    domain_status = domain_check.get("status", "unknown")
    domain_score = domain_check.get("reputation_score", 0.5)
    domain_reasons = domain_check.get("reasons", [])

    is_phishing = url_findings.get("is_phishing", False)
    phishing_score = float(url_findings.get("risk_score", 0.0)) * 100.0
    rule_score = float(rule_results.get("rule_risk_score", 0.0))

    # Adjust phishing score based on domain reputation
    if domain_status in ("malicious", "suspicious"):
        phishing_score = min(100.0, phishing_score + (1.0 - domain_score) * 30.0)

    combined_risk = int(min(max(phishing_score * 0.6 + rule_score * 0.25 + (1.0 - domain_score) * 15.0, 0), 100))
    verdict = _classify_risk(combined_risk)

    # Use scam classifier for better category detection
    classifier_result = scam_classifier_instance.classify(
        text=url_str,
        detection_results={"rules_triggered": rule_results.get("findings", [])},
    )
    scam_category = classifier_result.get("category_description", "Phishing URL / Fake Site") if combined_risk > 30 else "Safe Content"

    reasons = url_findings.get("findings", [])
    if not reasons and rule_results.get("findings"):
        reasons = [f.get("finding") for f in rule_results.get("findings")]
    reasons.extend(domain_reasons)

    ai_result = await ai_classifier.classify_content(
        text=url_str,
        detected_urls=[url_str],
    )

    ai_explanation = None
    if ai_result:
        ai_explanation = ai_result.get("explanation")
        if "risk_score" in ai_result:
            w = settings.AI_BLEND_WEIGHT
            combined_risk = int((combined_risk * (1 - w)) + (ai_result["risk_score"] * w))

    confidence = confidence_calculator.calculate(
        rule_score=rule_score,
        phrase_score=0.0,
        url_score=phishing_score,
    )

    explanation = explainability_engine.generate_explanation(
        risk_score=combined_risk,
        verdict=verdict.value,
        scam_category=scam_category,
        reasons=reasons,
        matched_phrases=[],
        detected_urls=[url_str],
        ai_explanation=ai_explanation,
    )

    actions = explainability_engine.generate_recommendations(
        verdict=verdict.value,
        scam_category=scam_category,
        has_url=True,
    )

    scan_id = f"url-{uuid.uuid4().hex[:8]}"

    response_data = {
        "id": scan_id,
        "scan_type": ScanType.URL,
        "input_summary": url_str[:200],
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
                "weight": 0.5,
            },
            {
                "layer": "Domain Reputation",
                "finding": f"Domain status: {domain_status} (score: {domain_score:.2f})",
                "severity": verdict.value,
                "weight": 0.25,
            },
            {
                "layer": "Rule Engine",
                "finding": f"Rule risk score: {rule_score:.2f}",
                "severity": verdict.value,
                "weight": 0.25,
            },
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    await history_repo.save_scan(response_data)
    return ScanResultResponse(**response_data)
