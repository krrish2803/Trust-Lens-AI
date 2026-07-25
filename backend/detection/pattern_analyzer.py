"""Pattern analyzer for detecting scam patterns in text."""
import re
from typing import List, Dict, Optional


# Known brands to detect
BRANDS = {
    "banking": ["SBI", "HDFC", "ICICI", "Axis", "Yes Bank", "Kotak", "PNB", "BOB", "Canara", "Union Bank", "IDBI", "Indian Bank", "Central Bank", "UCO", "Bank of India", "Bandhan", "Federal"],
    "payment": ["Paytm", "PhonePe", "Google Pay", "GPay", "BHIM", "Amazon Pay", "Mobikwik", "Freecharge", "CRED"],
    "ecommerce": ["Amazon", "Flipkart", "Myntra", "Snapdeal", "Meesho", "JioMart", "BigBasket", "Grofers", "Swiggy", "Zomato"],
    "government": ["UIDAI", "Aadhaar", "PAN", "Income Tax", "RBI", "SEBI", "IRDAI", "TRAI", "NSDL", "UTIITSL", "EPFO", "GST"],
    "telecom": ["Airtel", "Jio", "Vi", "BSNL", "MTNL"]
}

# Urgency patterns
URGENCY_PATTERNS = [
    (r'urgent|immediately|right now|asap|jaldi|turant|abhi', "high"),
    (r'24 hours|24 ghante|kal tak|aaj|today', "high"),
    (r'last chance|final warning|aakhri mauka', "critical"),
    (r'expire|expiring|khatam|band', "high"),
    (r'before|pehle|usse pehle', "medium"),
    (r'hurry up|jaldi karein|deri mat', "high"),
    (r'now or never|abhi ya kabhi nahi', "critical"),
]

# Social engineering tactics
SOCIAL_ENGINEERING = {
    "authority": [
        (r'police|CBI|cyber crime|FIR|court|judge|warrant', "authority_threat"),
        (r'RBI|SEBI|government|ministry|sarkar', "government_impersonation"),
        (r'bank se|bank representative|bank official|bank department', "bank_impersonation"),
        (r'cyber cell|digital crime|investigation', "law_enforcement"),
    ],
    "fear": [
        (r'account (band|block|suspend|freeze|close)', "account_threat"),
        (r'(FIR|complaint|case) (darj|filed|hoga)', "legal_threat"),
        (r'(jail|arrest|prison)', "imprisonment_threat"),
        (r'(property|asset) (attach|seize|freeze)', "asset_threat"),
        (r'(credit score|CIBIL) (zero|kharab|destroy)', "credit_threat"),
        (r'(passport|SIM|driving license) (cancel|block|suspend)', "document_threat"),
        (r'(electricity|water|gas|internet|DTH) (band|cut|disconnect)', "utility_threat"),
    ],
    "time_pressure": [
        (r'within \d+ hours?|next \d+ hours?', "time_limit"),
        (r'last (warning|chance|mauka)', "ultimatum"),
        (r'before (date|deadline|expiry)', "deadline"),
        (r'(aaj|abhi|turant|jaldi)', "immediate_action"),
    ],
    "greed": [
        (r'(prize|lottery|winner|gift|reward)', "prize_offer"),
        (r'(cashback|refund|bonus)', "financial_reward"),
        (r'(double|100%|guaranteed|assured)', "unrealistic_promise"),
        (r'(free|muft|mukht)', "free_offer"),
        (r'(iPhone|car|gold|laptop|TV|AC|bike)', "luxury_prize"),
    ]
}

# Emotional triggers
EMOTIONAL_TRIGGERS = {
    "fear": ["darr", "khatra", "warning", "alert", "danger", "threat", "risk", "scared", "afraid"],
    "greed": ["prize", "jeeto", "kamao", "profit", "bonus", "cashback", "reward", "gift", "free"],
    "urgency": ["jaldi", "turant", "abhi", "now", "hurry", "fast", "quick", "asap", "urgent"],
    "trust": ["verified", "official", "genuine", "authentic", "real", "legitimate", "trusted"],
    "curiosity": ["click here", "dekh", "check", "verify", "confirm", "know more", "discover"],
    "authority": ["order", "directive", "notice", "compliance", "mandatory", "required", "compulsory"],
    "sympathy": ["help", "support", "emergency", "urgent need", "please", "request", "kindly"],
    "fomo": ["limited", "exclusive", "only today", "last chance", "few left", "hurry", "don't miss"]
}


class PatternAnalyzer:
    """Analyzes text for scam patterns including brand mentions, urgency, and social engineering."""

    def __init__(self):
        self.brands = BRANDS
        self.urgency_patterns = URGENCY_PATTERNS
        self.social_engineering = SOCIAL_ENGINEERING
        self.emotional_triggers = EMOTIONAL_TRIGGERS

    def analyze(self, text: str) -> dict:
        """
        Analyze text for scam patterns.

        Input: text (str)
        Output: {
            "brand_mentions": [{"brand": str, "category": str, "context": str}],
            "urgency_indicators": [{"pattern": str, "intensity": str, "evidence": str}],
            "social_engineering": [{"tactic": str, "subcategory": str, "evidence": str}],
            "emotional_triggers": [{"trigger": str, "words": [str], "intensity": float}],
            "overall_threat_level": str,
            "analysis_summary": str
        }
        """
        brand_mentions = self._detect_brand_mentions(text)
        urgency_indicators = self._detect_urgency(text)
        social_engineering = self._detect_social_engineering(text)
        emotional_triggers = self._detect_emotional_triggers(text)

        results = {
            "brand_mentions": brand_mentions,
            "urgency_indicators": urgency_indicators,
            "social_engineering": social_engineering,
            "emotional_triggers": emotional_triggers,
        }

        results["overall_threat_level"] = self._calculate_threat_level(results)
        results["analysis_summary"] = self._generate_summary(results)

        return results

    def _detect_brand_mentions(self, text: str) -> List[dict]:
        """Detect brand name mentions in text."""
        mentions = []
        text_lower = text.lower()

        for category, brands in self.brands.items():
            for brand in brands:
                pattern = re.compile(re.escape(brand), re.IGNORECASE)
                matches = pattern.finditer(text)

                for match in matches:
                    start = max(0, match.start() - 40)
                    end = min(len(text), match.end() + 40)
                    context = text[start:end].strip()

                    mentions.append({
                        "brand": brand,
                        "category": category,
                        "context": f"...{context}..."
                    })

        seen = set()
        unique_mentions = []
        for m in mentions:
            key = (m["brand"], m["category"], m["context"])
            if key not in seen:
                seen.add(key)
                unique_mentions.append(m)

        return unique_mentions

    def _detect_urgency(self, text: str) -> List[dict]:
        """Detect urgency indicators."""
        indicators = []
        text_lower = text.lower()

        for pattern, intensity in self.urgency_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                evidence = matches[0] if len(matches) == 1 else ", ".join(matches[:3])
                indicators.append({
                    "pattern": pattern,
                    "intensity": intensity,
                    "evidence": evidence
                })

        return indicators

    def _detect_social_engineering(self, text: str) -> List[dict]:
        """Detect social engineering tactics."""
        detections = []
        text_lower = text.lower()

        for tactic, rules in self.social_engineering.items():
            for pattern, subcategory in rules:
                matches = re.findall(pattern, text_lower)
                if matches:
                    evidence = matches[0] if len(matches) == 1 else ", ".join(matches[:3])
                    detections.append({
                        "tactic": tactic,
                        "subcategory": subcategory,
                        "evidence": evidence
                    })

        return detections

    def _detect_emotional_triggers(self, text: str) -> List[dict]:
        """Detect emotional manipulation triggers."""
        triggers = []
        text_lower = text.lower()
        word_count = len(text_lower.split())

        for trigger_type, words in self.emotional_triggers.items():
            found_words = []
            for word in words:
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                    found_words.append(word)

            if found_words:
                intensity = min(1.0, len(found_words) / max(len(words), 1))
                triggers.append({
                    "trigger": trigger_type,
                    "words": found_words,
                    "intensity": round(intensity, 2)
                })

        return triggers

    def _calculate_threat_level(self, results: dict) -> str:
        """Calculate overall threat level from analysis."""
        score = 0

        # Brand mentions in non-matching contexts are suspicious
        if results["brand_mentions"]:
            score += len(results["brand_mentions"]) * 5

        # Urgency indicators
        urgency_weights = {"medium": 5, "high": 10, "critical": 20}
        for indicator in results["urgency_indicators"]:
            score += urgency_weights.get(indicator["intensity"], 5)

        # Social engineering tactics (strongest signal)
        se_weights = {
            "authority_threat": 25,
            "government_impersonation": 30,
            "bank_impersonation": 25,
            "law_enforcement": 30,
            "account_threat": 20,
            "legal_threat": 25,
            "imprisonment_threat": 30,
            "asset_threat": 20,
            "credit_threat": 15,
            "document_threat": 15,
            "utility_threat": 10,
            "time_limit": 10,
            "ultimatum": 15,
            "deadline": 5,
            "immediate_action": 8,
            "prize_offer": 20,
            "financial_reward": 10,
            "unrealistic_promise": 15,
            "free_offer": 8,
            "luxury_prize": 15,
        }
        for se in results["social_engineering"]:
            score += se_weights.get(se["subcategory"], 10)

        # Emotional triggers
        for trigger in results["emotional_triggers"]:
            if trigger["intensity"] >= 0.5:
                score += int(trigger["intensity"] * 15)

        # Determine level
        if score >= 80:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 25:
            return "medium"
        elif score > 0:
            return "low"
        else:
            return "none"

    def _generate_summary(self, results: dict) -> str:
        """Generate human-readable analysis summary."""
        parts = []

        # Brand mentions
        if results["brand_mentions"]:
            brands_found = list(set(m["brand"] for m in results["brand_mentions"]))
            categories = list(set(m["category"] for m in results["brand_mentions"]))
            parts.append(
                f"Detected references to {len(brands_found)} brand(s) "
                f"({', '.join(brands_found[:5])}) across categories: {', '.join(categories)}. "
                f"Brand impersonation is a common scam tactic."
            )

        # Urgency
        if results["urgency_indicators"]:
            critical = [i for i in results["urgency_indicators"] if i["intensity"] == "critical"]
            high = [i for i in results["urgency_indicators"] if i["intensity"] == "high"]
            parts.append(
                f"Found {len(results['urgency_indicators'])} urgency indicators "
                f"({len(critical)} critical, {len(high)} high). "
                f"Urgency pressure is used to prevent careful thinking."
            )

        # Social engineering
        if results["social_engineering"]:
            tactics = list(set(se["tactic"] for se in results["social_engineering"]))
            parts.append(
                f"Identified {len(results['social_engineering'])} social engineering signals "
                f"using tactics: {', '.join(tactics)}. "
                f"These are designed to manipulate victims into compliance."
            )

        # Emotional triggers
        if results["emotional_triggers"]:
            triggers = [t["trigger"] for t in results["emotional_triggers"] if t["intensity"] >= 0.3]
            if triggers:
                parts.append(
                    f"Emotional manipulation detected via: {', '.join(triggers)}. "
                    f"Scammers exploit emotions to override rational judgment."
                )

        # Overall assessment
        level = results["overall_threat_level"]
        level_descriptions = {
            "critical": "CRITICAL: This message exhibits multiple strong scam indicators.",
            "high": "HIGH: This message shows several signs of fraudulent intent.",
            "medium": "MEDIUM: Some suspicious patterns detected. Proceed with caution.",
            "low": "LOW: Minor indicators found. Likely legitimate but stay alert.",
            "none": "NONE: No significant scam patterns detected."
        }
        parts.append(level_descriptions.get(level, "Analysis complete."))

        return " ".join(parts)
