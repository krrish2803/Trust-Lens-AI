"""Risk engine that combines all detection layers into a final assessment."""
from typing import Dict, List, Optional


RISK_LEVELS = {
    "critical": {"min": 0.85, "max": 1.0, "color": "red", "action": "BLOCK immediately"},
    "high": {"min": 0.65, "max": 0.85, "color": "orange", "action": "WARN user strongly"},
    "medium": {"min": 0.45, "max": 0.65, "color": "yellow", "action": "CAUTION advised"},
    "low": {"min": 0.20, "max": 0.45, "color": "blue", "action": "MONITOR recommended"},
    "safe": {"min": 0.0, "max": 0.20, "color": "green", "action": "APPROVED - no threats detected"},
}

LAYER_WEIGHTS = {
    "phrase_match": 0.35,
    "rule_engine": 0.30,
    "url_detector": 0.25,
    "scam_classifier": 0.10,
}

RISK_LEVEL_TO_NUMERIC = {
    "critical": 0.95,
    "high": 0.75,
    "medium": 0.55,
    "low": 0.30,
    "safe": 0.0,
}


class RiskEngine:
    """Combines all detection layer results into a final risk assessment."""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or LAYER_WEIGHTS
        self.risk_levels = RISK_LEVELS

    def assess(
        self,
        phrase_match_results: dict,
        rule_engine_results: dict,
        url_detector_results: dict,
        scam_classifier_results: dict,
    ) -> dict:
        scores = {
            "phrase": self._extract_phrase_score(phrase_match_results),
            "rules": self._extract_rule_score(rule_engine_results),
            "url": self._extract_url_score(url_detector_results),
            "pattern": self._extract_pattern_score(scam_classifier_results),
        }

        layers_triggered = sum(1 for s in scores.values() if s > 0.0)
        weighted_score = self._calculate_weighted_score(scores)
        risk_level = self._determine_risk_level(weighted_score)
        confidence = self._calculate_confidence(scores, layers_triggered)
        verdict = self._generate_verdict(risk_level, layers_triggered)
        action = self._generate_action(risk_level)

        return {
            "risk_score": round(weighted_score, 4),
            "risk_level": risk_level,
            "confidence": round(confidence, 4),
            "detection_layers_triggered": layers_triggered,
            "weighted_breakdown": {
                "phrase": round(scores["phrase"], 4),
                "rules": round(scores["rules"], 4),
                "url": round(scores["url"], 4),
                "pattern": round(scores["pattern"], 4),
            },
            "verdict": verdict,
            "recommended_action": action,
        }

    # ------------------------------------------------------------------
    # Score extraction helpers
    # ------------------------------------------------------------------

    def _extract_phrase_score(self, results: dict) -> float:
        if not results:
            return 0.0

        if not results.get("detected", False):
            return 0.0

        phrases = results.get("phrases", [])
        if not phrases:
            return 0.0

        risk_level = results.get("risk_level", "safe")
        base = RISK_LEVEL_TO_NUMERIC.get(risk_level, 0.0)

        # Blend base level with per-phrase confidence average
        confidences = [p.get("confidence", 0.5) for p in phrases]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        # Weighted combination: 60% risk-level-derived, 40% confidence average
        score = 0.6 * base + 0.4 * avg_conf

        # Amplify if multiple high-confidence matches
        high_conf_count = sum(1 for c in confidences if c >= 0.85)
        if high_conf_count >= 3:
            score = min(1.0, score * 1.15)
        elif high_conf_count >= 2:
            score = min(1.0, score * 1.08)

        return min(1.0, max(0.0, score))

    def _extract_rule_score(self, results: dict) -> float:
        if not results:
            return 0.0

        # Handle rule_engine output format: {rules_triggered: [...], total_risk_from_rules: float}
        if "total_risk_from_rules" in results:
            return min(1.0, max(0.0, results["total_risk_from_rules"]))

        # If the rule engine exposes a numeric risk_score, use it directly
        if "risk_score" in results:
            return min(1.0, max(0.0, results["risk_score"]))

        if not results.get("triggered", False):
            return 0.0

        rules = results.get("rules", [])
        if not rules:
            return 0.0

        severity_map = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
        scores = []
        for rule in rules:
            sev = rule.get("severity", "low")
            conf = rule.get("confidence", 0.5)
            base = severity_map.get(sev, 0.25)
            scores.append(base * conf)

        if not scores:
            return 0.0

        # Use max severity weighted by the number of triggered rules
        max_score = max(scores)
        count_factor = min(1.0, len(scores) * 0.15)
        return min(1.0, max_score + count_factor * (1.0 - max_score))

    def _extract_url_score(self, results: dict) -> float:
        if not results:
            return 0.0

        # Handle url_detector output format: {final_url_risk: float, verdict: str}
        if "final_url_risk" in results:
            return min(1.0, max(0.0, results["final_url_risk"]))

        # Direct risk_score passthrough
        if "risk_score" in results:
            return min(1.0, max(0.0, results["risk_score"]))

        if not results.get("suspicious", False):
            return 0.0

        urls = results.get("urls", [])
        if not urls:
            return 0.0

        risk_level = results.get("risk_level", "safe")
        base = RISK_LEVEL_TO_NUMERIC.get(risk_level, 0.0)

        confidences = [u.get("confidence", 0.5) for u in urls]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        # More suspicious URLs raise the score
        url_count_factor = min(1.0, len(urls) * 0.2)
        score = 0.5 * base + 0.3 * avg_conf + 0.2 * url_count_factor

        return min(1.0, max(0.0, score))

    def _extract_pattern_score(self, results: dict) -> float:
        if not results:
            return 0.0

        # Handle scam_classifier output format: {scam_category: str, confidence: float}
        if "scam_category" in results:
            category = results.get("scam_category", "unknown")
            confidence = results.get("confidence", 0.0)
            if category != "unknown":
                return min(1.0, confidence)
            return min(1.0, confidence * 0.3)

        # Direct risk_score passthrough
        if "risk_score" in results:
            return min(1.0, max(0.0, results["risk_score"]))

        # Model confidence with prediction label
        confidence = results.get("confidence", 0.0)
        prediction = results.get("prediction", "safe")

        # Only count towards risk if model predicts scam
        scam_keywords = {"scam", "fraud", "phishing", "malicious", "spam", "dangerous", "high"}
        if prediction.lower() not in scam_keywords:
            # If prediction isn't explicitly scam, dampen the confidence
            return min(1.0, confidence * 0.3)

        return min(1.0, max(0.0, confidence))

    # ------------------------------------------------------------------
    # Weighted scoring
    # ------------------------------------------------------------------

    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        layer_weights = {
            "phrase": self.weights.get("phrase_match", 0.35),
            "rules": self.weights.get("rule_engine", 0.30),
            "url": self.weights.get("url_detector", 0.25),
            "pattern": self.weights.get("scam_classifier", 0.10),
        }

        total_weight = 0.0
        weighted_sum = 0.0
        for key, weight in layer_weights.items():
            if scores.get(key, 0.0) > 0.0:
                weighted_sum += scores[key] * weight
                total_weight += weight

        if total_weight == 0.0:
            return 0.0

        # Normalize by total weight of triggered layers
        return weighted_sum / total_weight

    # ------------------------------------------------------------------
    # Risk level determination
    # ------------------------------------------------------------------

    def _determine_risk_level(self, score: float) -> str:
        for level, spec in self.risk_levels.items():
            if spec["min"] <= score < spec["max"]:
                return level
        # Edge case: score == 1.0 falls outside [0.85, 1.0) closed-open range
        if score >= self.risk_levels["critical"]["min"]:
            return "critical"
        return "safe"

    # ------------------------------------------------------------------
    # Confidence calculation
    # ------------------------------------------------------------------

    def _calculate_confidence(self, scores: Dict[str, float], layers_triggered: int) -> float:
        active_scores = [s for s in scores.values() if s > 0.0]
        if not active_scores:
            return 0.95  # High confidence in "nothing detected"

        # Consistency: how much agreement exists between layers
        mean_score = sum(active_scores) / len(active_scores)
        variance = sum((s - mean_score) ** 2 for s in active_scores) / len(active_scores)
        consistency = 1.0 - min(1.0, variance * 4)  # lower variance = higher consistency

        # Coverage: more layers agreeing raises confidence
        coverage = min(1.0, layers_triggered / len(scores))

        # Average magnitude: higher scores are easier to be confident about
        magnitude = sum(active_scores) / len(active_scores)

        confidence = 0.4 * consistency + 0.35 * coverage + 0.25 * magnitude
        return min(1.0, max(0.0, confidence))

    # ------------------------------------------------------------------
    # Verdict and action generation
    # ------------------------------------------------------------------

    def _generate_verdict(self, risk_level: str, layers_triggered: int) -> str:
        verdicts = {
            "critical": (
                f"CRITICAL RISK: {layers_triggered} detection layer(s) flagged this "
                "message as highly dangerous. Immediate blocking recommended."
            ),
            "high": (
                f"HIGH RISK: {layers_triggered} detection layer(s) flagged this message "
                "as likely malicious. Strong warning advised."
            ),
            "medium": (
                f"MEDIUM RISK: {layers_triggered} detection layer(s) flagged suspicious "
                "patterns in this message. Proceed with caution."
            ),
            "low": (
                f"LOW RISK: {layers_triggered} detection layer(s) detected minor "
                "indicators. Monitoring recommended."
            ),
            "safe": (
                "SAFE: No significant threats detected across all detection layers."
            ),
        }
        return verdicts.get(risk_level, "Unable to determine risk.")

    def _generate_action(self, risk_level: str) -> str:
        return self.risk_levels.get(risk_level, {}).get("action", "Review manually")

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get_risk_level_info(self, level: str) -> dict:
        return self.risk_levels.get(level, {})
