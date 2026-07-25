"""
TrustLens AI - Message & Text Scan API Endpoint
Analyzes SMS, Email body, WhatsApp messages, or raw text for scams.
"""

import re
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from backend.config import settings
from backend.models.schemas import MessageScanRequest, ScanResultResponse, ScanType, RiskLevel
from backend.detection.phrase_matcher import PhraseMatcher
from backend.detection.rule_engine import rule_engine
from backend.detection.url_detector import URLDetector
from backend.detection.pattern_analyzer import PatternAnalyzer
from backend.detection.scam_classifier import ScamClassifier
from backend.detection.risk_engine import RiskEngine
from backend.ai.classifier import ai_classifier
from backend.ai.explainability import explainability_engine
from backend.ai.confidence_score import confidence_calculator
from backend.database.history import history_repo

router = APIRouter()
phrase_matcher_instance = PhraseMatcher()
url_detector_instance = URLDetector()
pattern_analyzer_instance = PatternAnalyzer()
scam_classifier_instance = ScamClassifier()
risk_engine_instance = RiskEngine()

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


@router.post("/message", response_model=ScanResultResponse)
async def scan_message(payload: MessageScanRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text content to scan cannot be empty.",
        )

    extracted_urls = _URL_RE.findall(text)

    phrase_result = phrase_matcher_instance.detect(text)
    matched_phrases = [p.get("phrase") for p in phrase_result.get("phrases", [])]

    rule_results = rule_engine.evaluate(text)

    # Deep pattern analysis (brand mentions, social engineering, emotional triggers)
    pattern_results = pattern_analyzer_instance.analyze(text)

    url_risk_scores = []
    for u in extracted_urls[:10]:
        det = url_detector_instance.detect(u)
        url_risk_scores.append(float(det.get("risk_score", det.get("final_url_risk", 0.0))) * 100.0)
    max_url_risk = max(url_risk_scores) if url_risk_scores else 0.0

    phrase_score = min(len(matched_phrases) * 35.0, 100.0)
    rule_score = float(rule_results.get("rule_risk_score", 0.0))

    # Boost score based on social engineering and urgency patterns
    se_count = len(pattern_results.get("social_engineering", []))
    urgency_count = len(pattern_results.get("urgency_indicators", []))
    emotional_count = len(pattern_results.get("emotional_triggers", []))
    pattern_boost = min(se_count * 8.0 + urgency_count * 5.0 + emotional_count * 3.0, 30.0)

    if extracted_urls:
        combined_risk = int(min(max(rule_score * 0.55 + phrase_score * 0.2 + max_url_risk * 0.15 + pattern_boost * 0.1, 0), 100))
    else:
        combined_risk = int(min(max(rule_score * 0.6 + phrase_score * 0.25 + pattern_boost * 0.15, 0), 100))

    # Floor rule: strong rule triggers should guarantee minimum risk
    if rule_score >= 70:
        combined_risk = max(combined_risk, 70)

    verdict = _classify_risk(combined_risk)

    # Use scam classifier for better category detection
    classifier_result = scam_classifier_instance.classify(
        text=text,
        detection_results={
            "phrases_detected": phrase_result.get("phrases", []),
            "rules_triggered": rule_results.get("findings", []),
            "url_risk": max_url_risk / 100.0,
        },
    )
    classifier_category = classifier_result.get("scam_category", "unknown")
    categories = rule_results.get("categories_triggered", [])

    # Prefer classifier category if it's more specific than "unknown"
    # and risk is not safe — safe content should not show scam categories
    if classifier_category != "unknown" and classifier_result.get("confidence", 0) > 0.3 and combined_risk > settings.RISK_THRESHOLD_LOW:
        scam_category = scam_classifier_instance.get_category_info(classifier_category).get("name", classifier_category)
    elif categories and combined_risk > settings.RISK_THRESHOLD_LOW:
        scam_category = categories[0]
    else:
        scam_category = "Safe Content"

    ai_result = await ai_classifier.classify_content(
        text=text,
        detected_urls=extracted_urls,
        matched_phrases=matched_phrases,
        rule_findings=rule_results.get("findings", []),
    )

    ai_explanation = None
    if ai_result:
        ai_explanation = ai_result.get("explanation")
        if "risk_score" in ai_result:
            w = settings.AI_BLEND_WEIGHT
            combined_risk = int((combined_risk * (1 - w)) + (ai_result["risk_score"] * w))

    reasons = [f.get("finding") for f in rule_results.get("findings", [])]
    if phrase_result.get("explanation") and phrase_result["explanation"] not in reasons:
        reasons.append(phrase_result["explanation"])

    # Add pattern analysis reasons
    if pattern_results.get("analysis_summary"):
        pattern_summary = pattern_results["analysis_summary"]
        if len(pattern_summary) > 20:
            reasons.append(f"Pattern analysis: {pattern_summary[:200]}")

    confidence = confidence_calculator.calculate(
        rule_score=rule_score,
        phrase_score=phrase_score,
        url_score=max_url_risk,
    )

    explanation = explainability_engine.generate_explanation(
        risk_score=combined_risk,
        verdict=verdict.value,
        scam_category=scam_category,
        reasons=reasons,
        matched_phrases=matched_phrases,
        detected_urls=extracted_urls,
        ai_explanation=ai_explanation,
    )

    actions = explainability_engine.generate_recommendations(
        verdict=verdict.value,
        scam_category=scam_category,
        has_url=bool(extracted_urls),
        has_otp_request="OTP" in scam_category or "otp" in text.lower(),
        has_financial_request="UPI" in scam_category or "Bank" in scam_category,
    )

    scan_id = f"msg-{uuid.uuid4().hex[:8]}"
    summary = text[:70] + "..." if len(text) > 70 else text

    # Build threat breakdown from all detection layers
    threat_breakdown = [
        {
            "layer": "Hinglish Phrase Library",
            "finding": f"Matched {len(matched_phrases)} scam phrases",
            "severity": verdict.value,
            "weight": 0.3,
        },
        {
            "layer": "Rule Engine",
            "finding": f"Triggered {len(categories)} threat categories",
            "severity": verdict.value,
            "weight": 0.3,
        },
    ]

    if se_count > 0 or urgency_count > 0 or emotional_count > 0:
        threat_breakdown.append({
            "layer": "Pattern Analysis",
            "finding": f"{se_count} social engineering, {urgency_count} urgency, {emotional_count} emotional triggers",
            "severity": verdict.value,
            "weight": 0.15,
        })

    if classifier_category != "unknown":
        threat_breakdown.append({
            "layer": "Scam Classifier",
            "finding": f"Category: {scam_category} (confidence: {classifier_result.get('confidence', 0):.2f})",
            "severity": verdict.value,
            "weight": 0.15,
        })

    if extracted_urls:
        threat_breakdown.append({
            "layer": "URL Analysis",
            "finding": f"Scanned {len(extracted_urls)} URLs, max risk: {max_url_risk:.1f}%",
            "severity": verdict.value,
            "weight": 0.1,
        })

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
        "threat_breakdown": threat_breakdown,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    await history_repo.save_scan(response_data)
    return ScanResultResponse(**response_data)
