#!/usr/bin/env python3
"""Evaluate detection pipeline accuracy against test cases."""
import json
import os
import sys
import argparse
from typing import List, Dict, Tuple
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from detection.phrase_matcher import PhraseMatcher
from detection.rule_engine import RuleEngine
from detection.url_detector import URLDetector
from detection.scam_classifier import ScamClassifier
from detection.risk_engine import RiskEngine
from detection.pattern_analyzer import PatternAnalyzer


# Default test cases
DEFAULT_TEST_CASES = [
    {
        "id": "TC001",
        "text": "URGENT: Aapka SBI account band hoga 24 ghante mein. KYC update karein: https://sbi-verify.tk",
        "expected_category": "fake_kyc",
        "expected_risk": "critical",
        "is_scam": True
    },
    {
        "id": "TC002",
        "text": "Aapko Amazon ka Rs. 10,000 gift card mila hai! Claim karein: https://amazon-prize.xyz",
        "expected_category": "job_internship_scam",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC003",
        "text": "OTP share karein verification ke liye. Hum bank se bol rahe hain.",
        "expected_category": "otp_theft",
        "expected_risk": "critical",
        "is_scam": True
    },
    {
        "id": "TC004",
        "text": "Dear customer, your account has been compromised. Click here to verify: http://192.168.1.1/verify",
        "expected_category": "phishing",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC005",
        "text": "Congratulations! Aapko iPhone 15 Pro mila hai. Tax pay karein Rs. 999 lene ke liye.",
        "expected_category": "job_internship_scam",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC006",
        "text": "Aapka loan Rs. 5,00,000 approved hai. Processing fee Rs. 5,000 pay karein.",
        "expected_category": "loan_scam",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC007",
        "text": "Police verification hai. Documents courier karein turant.",
        "expected_category": "social_engineering",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC008",
        "text": "Aapka mutual fund mature ho gaya hai. Payout lene ke liye UPI PIN share karein.",
        "expected_category": "investment_fraud",
        "expected_risk": "critical",
        "is_scam": True
    },
    {
        "id": "TC009",
        "text": "Hi, just wanted to confirm our meeting tomorrow at 3pm. See you then!",
        "expected_category": "unknown",
        "expected_risk": "safe",
        "is_scam": False
    },
    {
        "id": "TC010",
        "text": "Your order #12345 has been shipped. Track your package at amazon.in/track",
        "expected_category": "unknown",
        "expected_risk": "safe",
        "is_scam": False
    },
    {
        "id": "TC011",
        "text": "Digital arrest hai. Video call pe aaiye turant warna arrest hoga.",
        "expected_category": "social_engineering",
        "expected_risk": "critical",
        "is_scam": True
    },
    {
        "id": "TC012",
        "text": "Work from home job. Rs. 30,000 monthly. Registration fee Rs. 500 pay karein.",
        "expected_category": "job_internship_scam",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC013",
        "text": "Aapka UPI fraud ho gaya hai. Turant block karein. Hum ICICI bank se bol rahe hain.",
        "expected_category": "upi_fraud",
        "expected_risk": "critical",
        "is_scam": True
    },
    {
        "id": "TC014",
        "text": "Package deliver ho gaya. Rs. 99 delivery charge pay karein.",
        "expected_category": "fake_delivery",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC015",
        "text": "Crypto investment. Guaranteed profit. Rs. 5,000 se start karein. Double hoga 30 din mein.",
        "expected_category": "investment_fraud",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC016",
        "text": "Happy birthday! Wishing you a wonderful day ahead.",
        "expected_category": "unknown",
        "expected_risk": "safe",
        "is_scam": False
    },
    {
        "id": "TC017",
        "text": "Meeting rescheduled to 4pm. Please update your calendar.",
        "expected_category": "unknown",
        "expected_risk": "safe",
        "is_scam": False
    },
    {
        "id": "TC018",
        "text": "CBI investigation mein aapka naam hai. Call karein 9876543210 pe.",
        "expected_category": "social_engineering",
        "expected_risk": "critical",
        "is_scam": True
    },
    {
        "id": "TC019",
        "text": "Screen share karein problem solve karne ke liye. Remote access dijiye.",
        "expected_category": "customer_support_scam",
        "expected_risk": "high",
        "is_scam": True
    },
    {
        "id": "TC020",
        "text": "Income tax refund Rs. 15,000 aaya hai. Bank details confirm karein.",
        "expected_category": "phishing",
        "expected_risk": "high",
        "is_scam": True
    }
]


def load_test_cases(filepath: str = None) -> List[dict]:
    """Load test cases from file or use defaults."""
    if filepath and os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_TEST_CASES


def run_detection_pipeline(test_cases: List[dict]) -> List[dict]:
    """Run full detection pipeline on test cases."""
    phrase_matcher = PhraseMatcher()
    rule_engine = RuleEngine()
    url_detector = URLDetector()
    scam_classifier = ScamClassifier()
    risk_engine = RiskEngine()
    pattern_analyzer = PatternAnalyzer()

    results = []
    for tc in test_cases:
        text = tc["text"]

        # Run each detection layer
        phrase_results = phrase_matcher.detect(text)
        rule_results = rule_engine.evaluate(text)
        url_results = url_detector.detect(text)
        pattern_results = pattern_analyzer.analyze(text)

        # Classify
        classification = scam_classifier.classify(text, {
            "phrases_detected": phrase_results,
            "rules_triggered": rule_results,
            "url_risk": url_results
        })

        # Risk assessment
        risk_assessment = risk_engine.assess(
            phrase_results, rule_results, url_results, classification
        )

        results.append({
            "id": tc["id"],
            "text": text,
            "expected": tc,
            "detected_category": classification.get("scam_category", "unknown"),
            "detected_risk": risk_assessment.get("risk_level", "unknown"),
            "risk_score": risk_assessment.get("risk_score", 0),
            "confidence": risk_assessment.get("confidence", 0),
            "is_scam_detected": risk_assessment.get("risk_level", "safe") not in ["safe", "low"]
        })

    return results


def calculate_metrics(results: List[dict]) -> dict:
    """Calculate accuracy, precision, recall, F1."""
    tp = fp = tn = fn = 0
    correct_category = 0
    correct_risk = 0

    for r in results:
        expected_scam = r["expected"]["is_scam"]
        detected_scam = r["is_scam_detected"]

        if expected_scam and detected_scam:
            tp += 1
        elif not expected_scam and detected_scam:
            fp += 1
        elif not expected_scam and not detected_scam:
            tn += 1
        else:
            fn += 1

        if r["detected_category"] == r["expected"]["expected_category"]:
            correct_category += 1
        if r["detected_risk"] == r["expected"]["expected_risk"]:
            correct_risk += 1

    total = len(results)
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "total_cases": total,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "category_accuracy": correct_category / total if total > 0 else 0,
        "risk_accuracy": correct_risk / total if total > 0 else 0,
        "false_positive_rate": fp / (fp + tn) if (fp + tn) > 0 else 0
    }


def generate_confusion_matrix(results: List[dict]) -> dict:
    """Generate per-category confusion matrix."""
    matrix = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    for r in results:
        expected = r["expected"]["expected_category"]
        detected = r["detected_category"]

        if expected == detected:
            matrix[expected]["tp"] += 1
        else:
            matrix[expected]["fn"] += 1
            matrix[detected]["fp"] += 1

    return dict(matrix)


def identify_false_positives(results: List[dict]) -> List[dict]:
    """Find legitimate content flagged as scams."""
    fps = []
    for r in results:
        if not r["expected"]["is_scam"] and r["is_scam_detected"]:
            fps.append({
                "id": r["id"],
                "text": r["text"],
                "detected_category": r["detected_category"],
                "risk_score": r["risk_score"]
            })
    return fps


def identify_false_negatives(results: List[dict]) -> List[dict]:
    """Find scams not detected."""
    fns = []
    for r in results:
        if r["expected"]["is_scam"] and not r["is_scam_detected"]:
            fns.append({
                "id": r["id"],
                "text": r["text"],
                "expected_category": r["expected"]["expected_category"],
                "detected_risk": r["detected_risk"]
            })
    return fns


def main():
    parser = argparse.ArgumentParser(description="Evaluate TrustLens AI detection pipeline")
    parser.add_argument("--test-set", type=str, help="Path to test cases JSON")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print("Loading test cases...")
    test_cases = load_test_cases(args.test_set)
    print(f"Loaded {len(test_cases)} test cases")

    print("\nRunning detection pipeline...")
    results = run_detection_pipeline(test_cases)

    print("\nCalculating metrics...")
    metrics = calculate_metrics(results)

    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)

    print(f"\nOverall Metrics:")
    print(f"  Accuracy:       {metrics['accuracy']:.2%}")
    print(f"  Precision:      {metrics['precision']:.2%}")
    print(f"  Recall:         {metrics['recall']:.2%}")
    print(f"  F1 Score:       {metrics['f1_score']:.2%}")
    print(f"  Category Acc:   {metrics['category_accuracy']:.2%}")
    print(f"  Risk Accuracy:  {metrics['risk_accuracy']:.2%}")
    print(f"  FP Rate:        {metrics['false_positive_rate']:.2%}")

    print(f"\nConfusion:")
    print(f"  True Positives:  {metrics['true_positives']}")
    print(f"  False Positives: {metrics['false_positives']}")
    print(f"  True Negatives:  {metrics['true_negatives']}")
    print(f"  False Negatives: {metrics['false_negatives']}")

    # Per-category breakdown
    matrix = generate_confusion_matrix(results)
    print(f"\nPer-Category Breakdown:")
    for cat, counts in sorted(matrix.items()):
        total = counts["tp"] + counts["fn"]
        acc = counts["tp"] / total if total > 0 else 0
        print(f"  {cat}: TP={counts['tp']}, FP={counts['fp']}, FN={counts['fn']}, Acc={acc:.2%}")

    # False positives
    fps = identify_false_positives(results)
    if fps:
        print(f"\nFalse Positives (legitimate flagged as scam):")
        for fp in fps:
            print(f"  [{fp['id']}] {fp['text'][:80]}...")

    # False negatives
    fns = identify_false_negatives(results)
    if fns:
        print(f"\nFalse Negatives (scam not detected):")
        for fn in fns:
            print(f"  [{fn['id']}] {fn['text'][:80]}...")

    if args.verbose:
        print(f"\nDetailed Results:")
        for r in results:
            status = "✓" if r["is_scam_detected"] == r["expected"]["is_scam"] else "✗"
            print(f"  {status} [{r['id']}] Category: {r['detected_category']} (expected: {r['expected']['expected_category']}), Risk: {r['detected_risk']} (expected: {r['expected']['expected_risk']})")

    # Save results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluation_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"metrics": metrics, "results": results, "confusion_matrix": matrix}, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
