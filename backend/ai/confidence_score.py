"""
TrustLens AI - Confidence Score Calculator
Calculates overall confidence metric based on multi-layer signal alignment.
"""

from typing import List, Dict, Any


class ConfidenceScoreCalculator:
    @staticmethod
    def calculate(
        rule_score: float,
        phrase_score: float,
        url_score: float,
        ai_confidence: float = None,
        layer_count: int = 5
    ) -> float:
        """
        Calculates a confidence score between 0.00 and 1.00 based on signal agreement.
        """
        scores = [s for s in [rule_score, phrase_score, url_score] if s > 0]

        if not scores:
            return 0.85  # Default baseline for clear non-scams

        # Higher consensus across multiple layers yields higher confidence
        variance = max(scores) - min(scores) if len(scores) > 1 else 0.0
        consensus_factor = 1.0 - (variance / 100.0)

        base_confidence = 0.80 + (0.15 * consensus_factor)

        if ai_confidence is not None:
            base_confidence = (base_confidence * 0.5) + (ai_confidence * 0.5)

        return round(min(max(base_confidence, 0.65), 0.99), 2)


confidence_calculator = ConfidenceScoreCalculator()
