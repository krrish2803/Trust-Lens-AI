#!/usr/bin/env python3
"""Phrase validation script for TrustLens AI datasets."""
import json
import os
import sys
import argparse
from collections import Counter
from typing import List, Dict


DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets')


def load_phrases() -> List[dict]:
    """Load phrases from dataset."""
    filepath = os.path.join(DATASETS_DIR, "hinglish_phrases.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("phrases", [])


def check_coverage(phrases: List[dict]) -> dict:
    """Check that all scam types are represented."""
    type_counts = Counter(p.get("type", "unknown") for p in phrases)
    category_counts = Counter(p.get("scam_category", "unknown") for p in phrases)

    expected_types = {"threat", "urgency", "reward", "credential_request", "payment_request", "authority_impersonation"}
    missing_types = expected_types - set(type_counts.keys())

    return {
        "type_distribution": dict(type_counts),
        "category_distribution": dict(category_counts),
        "missing_types": list(missing_types),
        "coverage_score": len(set(type_counts.keys())) / len(expected_types) * 100
    }


def check_variations(phrases: List[dict]) -> dict:
    """Ensure multiple variations per phrase."""
    no_variations = []
    single_variation = []
    good_variations = []

    for p in phrases:
        variations = p.get("variations", [])
        if len(variations) == 0:
            no_variations.append(p.get("phrase", ""))
        elif len(variations) == 1:
            single_variation.append(p.get("phrase", ""))
        else:
            good_variations.append(p.get("phrase", ""))

    total = len(phrases)
    return {
        "total_phrases": total,
        "no_variations": len(no_variations),
        "single_variation": len(single_variation),
        "good_variations": len(good_variations),
        "variation_score": len(good_variations) / total * 100 if total > 0 else 0,
        "phrases_without_variations": no_variations[:10]
    }


def check_confidence_scores(phrases: List[dict]) -> dict:
    """Validate confidence scores are in 0-1 range."""
    invalid = []
    scores = []

    for p in phrases:
        conf = p.get("confidence", -1)
        scores.append(conf)
        if conf < 0 or conf > 1:
            invalid.append({"phrase": p.get("phrase", ""), "confidence": conf})

    return {
        "total": len(phrases),
        "invalid_count": len(invalid),
        "min_score": min(scores) if scores else 0,
        "max_score": max(scores) if scores else 0,
        "avg_score": sum(scores) / len(scores) if scores else 0,
        "invalid_scores": invalid[:10]
    }


def detect_false_positives(phrases: List[dict]) -> dict:
    """Find phrases that might match legitimate content."""
    legitimate_keywords = [
        "thank you", "welcome", "congratulations on", "account update",
        "profile update", "verify email", "confirm subscription"
    ]

    potential_fps = []
    for p in phrases:
        phrase_text = p.get("phrase", "").lower()
        for keyword in legitimate_keywords:
            if keyword in phrase_text:
                potential_fps.append({
                    "phrase": p.get("phrase", ""),
                    "reason": f"Contains legitimate keyword: '{keyword}'",
                    "confidence": p.get("confidence", 0)
                })
                break

    return {
        "total_potential_fps": len(potential_fps),
        "potential_false_positives": potential_fps,
        "fp_risk_level": "high" if len(potential_fps) > 10 else "medium" if len(potential_fps) > 5 else "low"
    }


def generate_report(phrases: List[dict]) -> dict:
    """Generate full quality report."""
    coverage = check_coverage(phrases)
    variations = check_variations(phrases)
    confidence = check_confidence_scores(phrases)
    false_positives = detect_false_positives(phrases)

    overall_score = (
        coverage["coverage_score"] * 0.3 +
        variations["variation_score"] * 0.3 +
        (100 - false_positives["total_potential_fps"] * 2) * 0.2 +
        min(100, confidence["avg_score"] * 100) * 0.2
    )

    return {
        "total_phrases": len(phrases),
        "coverage": coverage,
        "variations": variations,
        "confidence_scores": confidence,
        "false_positives": false_positives,
        "overall_quality_score": round(overall_score, 2)
    }


def main():
    parser = argparse.ArgumentParser(description="Validate TrustLens AI phrases dataset")
    parser.add_argument("--check-coverage", action="store_true", help="Check type coverage")
    parser.add_argument("--check-variations", action="store_true", help="Check variation quality")
    parser.add_argument("--check-confidence", action="store_true", help="Check confidence scores")
    parser.add_argument("--check-fp", action="store_true", help="Check for false positives")
    parser.add_argument("--full-report", action="store_true", help="Generate full report")
    args = parser.parse_args()

    phrases = load_phrases()
    print(f"Loaded {len(phrases)} phrases\n")

    if args.full_report or not any([args.check_coverage, args.check_variations, args.check_confidence, args.check_fp]):
        report = generate_report(phrases)
        print("=" * 60)
        print("FULL VALIDATION REPORT")
        print("=" * 60)
        print(f"\nTotal phrases: {report['total_phrases']}")
        print(f"Overall quality score: {report['overall_quality_score']}%\n")

        print("COVERAGE:")
        print(f"  Types found: {len(report['coverage']['type_distribution'])}/6")
        print(f"  Coverage score: {report['coverage']['coverage_score']:.1f}%")
        if report['coverage']['missing_types']:
            print(f"  Missing types: {', '.join(report['coverage']['missing_types'])}")

        print("\nVARIATIONS:")
        print(f"  Good (2+ variations): {report['variations']['good_variations']}")
        print(f"  Single variation: {report['variations']['single_variation']}")
        print(f"  No variations: {report['variations']['no_variations']}")
        print(f"  Variation score: {report['variations']['variation_score']:.1f}%")

        print("\nCONFIDENCE SCORES:")
        print(f"  Average: {report['confidence_scores']['avg_score']:.3f}")
        print(f"  Range: {report['confidence_scores']['min_score']:.3f} - {report['confidence_scores']['max_score']:.3f}")
        print(f"  Invalid: {report['confidence_scores']['invalid_count']}")

        print("\nFALSE POSITIVE RISK:")
        print(f"  Risk level: {report['false_positives']['fp_risk_level']}")
        print(f"  Potential FP: {report['false_positives']['total_potential_fps']}")
    else:
        if args.check_coverage:
            result = check_coverage(phrases)
            print(f"Coverage score: {result['coverage_score']:.1f}%")
            print(f"Type distribution: {result['type_distribution']}")

        if args.check_variations:
            result = check_variations(phrases)
            print(f"Variation score: {result['variation_score']:.1f}%")

        if args.check_confidence:
            result = check_confidence_scores(phrases)
            print(f"Confidence avg: {result['avg_score']:.3f}")
            print(f"Invalid: {result['invalid_count']}")

        if args.check_fp:
            result = detect_false_positives(phrases)
            print(f"FP risk: {result['fp_risk_level']}")
            print(f"Potential FP: {result['total_potential_fps']}")


if __name__ == "__main__":
    main()
