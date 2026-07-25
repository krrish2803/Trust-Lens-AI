"""Scam classification module for categorizing detected threats."""
import re
from typing import List, Dict, Optional


# 13 scam categories with descriptions
SCAM_CATEGORIES = {
    "fake_kyc": {
        "name": "Fake KYC Scam",
        "description": "Scams impersonating banks/government for KYC updates",
        "keywords": ["kyc", "aadhaar", "pan", "verify", "update", "link"],
        "risk_base": 0.85
    },
    "fake_bank_alert": {
        "name": "Fake Bank Alert",
        "description": "Scams impersonating banks with fake alerts",
        "keywords": ["bank", "account", "suspend", "block", "freeze", "verify"],
        "risk_base": 0.88
    },
    "otp_theft": {
        "name": "OTP Theft",
        "description": "Scams attempting to steal OTPs",
        "keywords": ["otp", "code", "share", "batao", "send"],
        "risk_base": 0.95
    },
    "upi_fraud": {
        "name": "UPI Fraud",
        "description": "Scams targeting UPI payments",
        "keywords": ["upi", "pin", "qr", "request", "approve", "gpay", "phonepe", "paytm"],
        "risk_base": 0.92
    },
    "fake_delivery": {
        "name": "Fake Delivery Scam",
        "description": "Scams about fake package deliveries",
        "keywords": ["delivery", "package", "courier", "parcel", "charge", "fee"],
        "risk_base": 0.78
    },
    "customer_support_scam": {
        "name": "Customer Support Scam",
        "description": "Fake customer support impersonation",
        "keywords": ["support", "help", "technician", "screen share", "remote access"],
        "risk_base": 0.85
    },
    "job_internship_scam": {
        "name": "Job/Internship Scam",
        "description": "Fake job/internship offers",
        "keywords": ["job", "work", "salary", "internship", "stipend", "registration fee"],
        "risk_base": 0.80
    },
    "investment_fraud": {
        "name": "Investment Fraud",
        "description": "Fake investment opportunities",
        "keywords": ["invest", "return", "profit", "crypto", "stock", "mutual fund", "guaranteed"],
        "risk_base": 0.88
    },
    "loan_scam": {
        "name": "Loan Scam",
        "description": "Fake loan offers",
        "keywords": ["loan", "emi", "credit", "approved", "processing fee"],
        "risk_base": 0.82
    },
    "phishing": {
        "name": "Phishing",
        "description": "General phishing attempts",
        "keywords": ["click", "link", "verify", "confirm", "update", "login"],
        "risk_base": 0.85
    },
    "social_engineering": {
        "name": "Social Engineering",
        "description": "Social engineering manipulation tactics",
        "keywords": ["police", "court", "fir", "warning", "threat", "arrest"],
        "risk_base": 0.87
    },
    "ransomware": {
        "name": "Ransomware",
        "description": "Ransomware/extortion attempts",
        "keywords": ["hack", "compromise", "data", "pay", "decrypt", "unlock"],
        "risk_base": 0.90
    },
    "unknown": {
        "name": "Unknown",
        "description": "Unclassified suspicious content",
        "keywords": [],
        "risk_base": 0.50
    }
}


class ScamClassifier:
    """Classifies detected threats into scam categories."""

    def __init__(self):
        self.categories = SCAM_CATEGORIES

    def classify(self, text: str, detection_results: dict) -> dict:
        """
        Classify the scam based on detection results.

        Args:
            text: Original input text.
            detection_results: Output from detection pipeline with keys:
                - phrases_detected: list of matched phrase dicts
                - rules_triggered: list of matched rule dicts
                - url_risk: float or dict with URL risk info

        Returns:
            {
                "scam_category": str,
                "category_description": str,
                "confidence": float,
                "matching_patterns": [str]
            }
        """
        if not text or not text.strip():
            return {
                "scam_category": "unknown",
                "category_description": self.categories["unknown"]["description"],
                "confidence": 0.0,
                "matching_patterns": []
            }

        phrases = detection_results.get("phrases_detected", [])
        rules = detection_results.get("rules_triggered", [])
        url_r = detection_results.get("url_risk", {})
        url_score = url_r.get("final_url_risk", 0.0) if isinstance(url_r, dict) else (url_r if isinstance(url_r, (int, float)) else 0.0)

        if not phrases and not rules and url_score <= 0.2:
            return {
                "scam_category": "unknown",
                "category_description": self.categories["unknown"]["description"],
                "confidence": 0.0,
                "matching_patterns": []
            }

        scores = self._score_categories(text, detection_results)
        total_score = sum(scores.values())

        if total_score == 0:
            return {
                "scam_category": "unknown",
                "category_description": self.categories["unknown"]["description"],
                "confidence": 0.0,
                "matching_patterns": []
            }

        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        confidence = self._calculate_confidence(best_category, best_score, total_score)
        matching_patterns = self._find_matching_patterns(text, best_category)

        return {
            "scam_category": best_category,
            "category_description": self.categories[best_category]["description"],
            "confidence": round(confidence, 4),
            "matching_patterns": matching_patterns
        }

    def _score_categories(self, text: str, detection_results: dict) -> Dict[str, float]:
        """Score each category based on evidence from text and detection layers."""
        scores: Dict[str, float] = {cat: 0.0 for cat in self.categories}

        # Layer 1: keyword matching against text
        text_lower = text.lower()
        for cat_key, cat_info in self.categories.items():
            if cat_key == "unknown":
                continue
            matched = self._match_keywords(text_lower, cat_info["keywords"])
            keyword_weight = len(matched) * 0.15
            scores[cat_key] += keyword_weight

        # Layer 2: boost from phrases_detected (phrase_matcher output)
        phrases_detected = detection_results.get("phrases_detected", [])
        if isinstance(phrases_detected, dict):
            phrases_detected = phrases_detected.get("phrases", [])
        if isinstance(phrases_detected, list):
            for phrase_entry in phrases_detected:
                if isinstance(phrase_entry, dict):
                    phrase_cat = phrase_entry.get("scam_category", "unknown")
                    if phrase_cat in scores:
                        phrase_conf = phrase_entry.get("confidence", 0.5)
                        scores[phrase_cat] += phrase_conf * 0.5

        # Layer 3: boost from rules_triggered (rule_engine output)
        rules_triggered = detection_results.get("rules_triggered", [])
        if isinstance(rules_triggered, dict):
            rules_triggered = rules_triggered.get("rules_triggered", [])
        if isinstance(rules_triggered, list):
            for rule_entry in rules_triggered:
                if isinstance(rule_entry, dict):
                    rule_cats = rule_entry.get("scam_categories", [])
                    rule_weight = rule_entry.get("weight", 0.3)
                    for rcat in rule_cats:
                        if rcat in scores:
                            scores[rcat] += rule_weight

        # Layer 4: URL risk contribution
        url_risk = detection_results.get("url_risk", 0)
        if isinstance(url_risk, dict):
            url_risk = url_risk.get("risk_score", 0)
        if isinstance(url_risk, (int, float)) and url_risk > 0:
            # URL risk most relevant to phishing and fake bank alerts
            scores["phishing"] += url_risk * 0.2
            scores["fake_bank_alert"] += url_risk * 0.15

        # Apply base risk floor: category cannot score below its base if any signal exists
        for cat_key, cat_info in self.categories.items():
            if cat_key == "unknown":
                continue
            if scores[cat_key] > 0:
                scores[cat_key] = max(scores[cat_key], cat_info["risk_base"] * 0.3)

        return scores

    def _match_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """Find matching keywords in text (case-insensitive word boundary match)."""
        matched = []
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                matched.append(kw)
        return matched

    def _calculate_confidence(self, category: str, score: float, total_score: float) -> float:
        """Calculate classification confidence as ratio of best score to total, capped to [0,1]."""
        if total_score == 0:
            return 0.0
        raw = score / total_score
        return max(0.0, min(1.0, raw))

    def _find_matching_patterns(self, text: str, category: str) -> List[str]:
        """Find specific keywords/patterns that matched the winning category."""
        if category not in self.categories:
            return []
        keywords = self.categories[category].get("keywords", [])
        text_lower = text.lower()
        return self._match_keywords(text_lower, keywords)

    def get_category_info(self, category: str) -> dict:
        """Get information about a scam category."""
        if category in self.categories:
            return {
                "key": category,
                "name": self.categories[category]["name"],
                "description": self.categories[category]["description"],
                "risk_base": self.categories[category]["risk_base"],
                "keywords": list(self.categories[category]["keywords"])
            }
        return {
            "key": "unknown",
            "name": self.categories["unknown"]["name"],
            "description": self.categories["unknown"]["description"],
            "risk_base": self.categories["unknown"]["risk_base"],
            "keywords": []
        }
