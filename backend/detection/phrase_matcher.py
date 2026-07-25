"""Phrase matching module for detecting scam phrases in Hinglish/English text."""
import re
import json
import os
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
from .utils import normalize_text, remove_special_chars, load_json_dataset, get_dataset_path


class PhraseMatcher:
    """Detects scam phrases in text using dataset matching with fuzzy tolerance."""

    FUZZY_THRESHOLD = 0.8
    WINDOW_SIZES = [3, 4, 5, 6, 7, 8]

    HIGH_CONFIDENCE_THRESHOLD = 0.85
    CRITICAL_MATCH_COUNT = 3
    HIGH_MATCH_COUNT = 2
    MEDIUM_MATCH_COUNT = 1

    def __init__(self):
        self.phrases: List[dict] = []
        self._load_phrases()

    def _load_phrases(self):
        """Load phrases from hinglish_phrases.json dataset."""
        try:
            dataset_path = get_dataset_path("hinglish_phrases.json")
            data = load_json_dataset(dataset_path)
            self.phrases = data.get("phrases", [])
        except FileNotFoundError:
            self.phrases = []
        except (json.JSONDecodeError, KeyError):
            self.phrases = []

    def detect(self, text: str, language: str = "auto") -> dict:
        """
        Detect scam phrases in text.

        Args:
            text: Input text to analyze.
            language: Language hint - "auto", "hinglish", or "english".

        Returns:
            Dictionary with detection results including detected phrases,
            risk level, and explanation.
        """
        if not text or not text.strip():
            return {
                "detected": False,
                "phrases": [],
                "risk_level": "safe",
                "explanation": "No text provided for analysis."
            }

        normalized = normalize_text(text)
        cleaned = remove_special_chars(normalized)

        matches: List[dict] = []
        seen_phrases: set = set()

        for phrase_entry in self.phrases:
            phrase_text = phrase_entry.get("phrase", "")
            phrase_lower = phrase_text.lower()

            if phrase_lower in seen_phrases:
                continue

            position = self._find_position(cleaned, phrase_lower)
            if position >= 0:
                seen_phrases.add(phrase_lower)
                matches.append({
                    "phrase": phrase_text,
                    "type": phrase_entry.get("type", "unknown"),
                    "confidence": phrase_entry.get("confidence", 0.5),
                    "position": position,
                    "match_type": "exact",
                    "scam_category": phrase_entry.get("scam_category", "unknown")
                })
                continue

            variations = phrase_entry.get("variations", [])
            for variation in variations:
                var_lower = variation.lower()
                if var_lower in seen_phrases:
                    continue

                var_position = self._find_position(cleaned, var_lower)
                if var_position >= 0:
                    seen_phrases.add(var_lower)
                    matches.append({
                        "phrase": variation,
                        "type": phrase_entry.get("type", "unknown"),
                        "confidence": phrase_entry.get("confidence", 0.5) * 0.95,
                        "position": var_position,
                        "match_type": "variation",
                        "scam_category": phrase_entry.get("scam_category", "unknown")
                    })
                    break

        for phrase_entry in self.phrases:
            phrase_text = phrase_entry.get("phrase", "")
            phrase_lower = phrase_text.lower()

            if phrase_lower in seen_phrases:
                continue

            matched, conf = self._fuzzy_match(cleaned, phrase_lower, self.FUZZY_THRESHOLD)
            if matched:
                seen_phrases.add(phrase_lower)
                matches.append({
                    "phrase": phrase_text,
                    "type": phrase_entry.get("type", "unknown"),
                    "confidence": conf * phrase_entry.get("confidence", 0.5),
                    "position": -1,
                    "match_type": "fuzzy",
                    "scam_category": phrase_entry.get("scam_category", "unknown")
                })
                continue

            variations = phrase_entry.get("variations", [])
            for variation in variations:
                var_lower = variation.lower()
                if var_lower in seen_phrases:
                    continue

                var_matched, var_conf = self._fuzzy_match(cleaned, var_lower, self.FUZZY_THRESHOLD)
                if var_matched:
                    seen_phrases.add(var_lower)
                    matches.append({
                        "phrase": variation,
                        "type": phrase_entry.get("type", "unknown"),
                        "confidence": var_conf * phrase_entry.get("confidence", 0.5) * 0.9,
                        "position": -1,
                        "match_type": "fuzzy_variation",
                        "scam_category": phrase_entry.get("scam_category", "unknown")
                    })
                    break

        matches.sort(key=lambda m: m["confidence"], reverse=True)

        risk_level = self._calculate_risk_level(matches)
        explanation = self._generate_explanation(matches, risk_level)

        return {
            "detected": len(matches) > 0,
            "phrases": matches,
            "risk_level": risk_level,
            "explanation": explanation
        }

    def _fuzzy_match(self, text: str, phrase: str, threshold: float = 0.8) -> Tuple[bool, float]:
        """Check if text contains a fuzzy match of phrase using sliding window."""
        text_words = text.split()
        phrase_words = phrase.split()
        phrase_len = len(phrase_words)

        if phrase_len == 0:
            return False, 0.0

        if phrase_len <= len(text_words):
            for i in range(len(text_words) - phrase_len + 1):
                window = " ".join(text_words[i:i + phrase_len])
                ratio = SequenceMatcher(None, window, phrase).ratio()
                if ratio >= threshold:
                    return True, ratio

        for window_size in self.WINDOW_SIZES:
            if window_size < phrase_len:
                continue
            for i in range(len(text_words) - window_size + 1):
                window = " ".join(text_words[i:i + window_size])
                ratio = SequenceMatcher(None, window, phrase).ratio()
                if ratio >= threshold:
                    return True, ratio

        full_ratio = SequenceMatcher(None, text, phrase).ratio()
        if full_ratio >= threshold:
            return True, full_ratio

        return False, 0.0

    def _find_position(self, text: str, phrase: str) -> int:
        """Find the starting position of phrase in text. Returns -1 if not found."""
        idx = text.find(phrase)
        if idx >= 0:
            return idx

        text_no_space = re.sub(r'\s+', ' ', text)
        phrase_no_space = re.sub(r'\s+', ' ', phrase)
        idx = text_no_space.find(phrase_no_space)
        if idx >= 0:
            return idx

        return -1

    def _calculate_risk_level(self, matches: List[dict]) -> str:
        """Calculate risk level based on matched phrases."""
        if not matches:
            return "safe"

        high_conf_matches = [
            m for m in matches
            if m["confidence"] >= self.HIGH_CONFIDENCE_THRESHOLD
        ]

        if len(high_conf_matches) >= self.CRITICAL_MATCH_COUNT:
            return "critical"

        if len(high_conf_matches) >= self.HIGH_MATCH_COUNT:
            return "high"

        if len(high_conf_matches) >= self.MEDIUM_MATCH_COUNT:
            return "medium"

        if len(matches) > 0:
            return "low"

        return "safe"

    def _generate_explanation(self, matches: List[dict], risk_level: str) -> str:
        """Generate human-readable explanation of detection."""
        if not matches:
            return "No scam phrases detected in the provided text."

        type_counts: Dict[str, int] = {}
        category_counts: Dict[str, int] = {}
        for m in matches:
            t = m.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
            cat = m.get("scam_category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        type_labels = {
            "threat": "threatening language",
            "payment_request": "payment/fee requests",
            "reward": "too-good-to-be-true rewards",
            "credential_request": "credential/OTP sharing requests",
            "urgency": "artificial urgency/pressure tactics",
            "authority_impersonation": "authority impersonation",
            "social_engineering": "social engineering tactics"
        }

        parts = []
        parts.append(f"Detected {len(matches)} scam-related phrase(s).")

        type_parts = []
        for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            label = type_labels.get(t, t)
            type_parts.append(f"{count} instance(s) of {label}")
        if type_parts:
            parts.append("Patterns found: " + ", ".join(type_parts) + ".")

        cat_parts = []
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            cat_parts.append(f"{cat} ({count})")
        if cat_parts:
            parts.append("Scam categories: " + ", ".join(cat_parts) + ".")

        risk_descriptions = {
            "critical": "This message exhibits multiple high-confidence scam indicators and is very likely fraudulent.",
            "high": "This message contains multiple strong scam signals and is likely fraudulent.",
            "medium": "This message contains at least one strong scam indicator and should be treated with caution.",
            "low": "This message contains patterns similar to known scams but with lower confidence.",
            "safe": "No significant scam indicators detected."
        }
        parts.append(risk_descriptions.get(risk_level, ""))

        top_matches = sorted(matches, key=lambda m: m["confidence"], reverse=True)[:3]
        if top_matches:
            quote_parts = []
            for m in top_matches:
                conf_pct = int(m["confidence"] * 100)
                quote_parts.append(f'"{m["phrase"]}" ({conf_pct}% confidence)')
            parts.append("Top matched phrases: " + "; ".join(quote_parts) + ".")

        return " ".join(parts)
