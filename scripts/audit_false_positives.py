#!/usr/bin/env python3
"""Audit false positives in detection system."""
import json
import os
import sys
import argparse
from typing import List, Dict
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from detection.phrase_matcher import PhraseMatcher
from detection.rule_engine import RuleEngine
from detection.risk_engine import RiskEngine


# Known legitimate content that might trigger false positives
LEGITIMATE_CONTENT = [
    "Dear Customer, your account has been updated successfully.",
    "Your OTP for login is 123456. Do not share with anyone.",
    "Congratulations on your purchase! Your order is confirmed.",
    "Your monthly account statement is ready for download.",
    "Thank you for banking with us. Your feedback is valuable.",
    "Your KYC has been verified. Thank you for your patience.",
    "Meeting scheduled for tomorrow at 3pm. Please confirm attendance.",
    "Happy Diwali! Wishing you and your family a prosperous year.",
    "Your password was changed successfully. If this wasn't you, contact us.",
    "Welcome to our platform. Here's how to get started.",
    "Your subscription has been renewed. Next billing date: 15/08/2026.",
    "We've received your application. We'll get back to you in 2-3 business days.",
    "Your account balance is Rs. 25,000. Last transaction: Rs. 500 credited.",
    "Important: Update your profile to continue using our services.",
    "Your transaction of Rs. 1,500 was successful. UPI Ref: 1234567890",
    "Dear user, your OTP for transaction verification is 654321.",
    "Your EMI of Rs. 5,000 has been debited from your account.",
    "Account alert: Credit of Rs. 50,000 on 25/07/2026.",
    "Your request for account statement has been processed.",
    "Thank you for visiting our branch. How may we help you?"
]


def analyze_false_positives(threshold: float = 0.85) -> dict:
    """Find legitimate content that triggers scam detection."""
    phrase_matcher = PhraseMatcher()
    rule_engine = RuleEngine()
    risk_engine = RiskEngine()
    
    false_positives = []
    
    for content in LEGITIMATE_CONTENT:
        phrase_results = phrase_matcher.detect(content)
        rule_results = rule_engine.evaluate(content)
        
        risk_assessment = risk_engine.assess(
            phrase_results, rule_results, {}, {}
        )
        
        risk_score = risk_assessment.get("risk_score", 0)
        
        if risk_score >= threshold:
            false_positives.append({
                "content": content,
                "risk_score": risk_score,
                "risk_level": risk_assessment.get("risk_level", "unknown"),
                "triggered_phrases": phrase_results.get("phrases", []),
                "triggered_rules": rule_results.get("rules_triggered", [])
            })
    
    return {
        "threshold": threshold,
        "total_legitimate": len(LEGITIMATE_CONTENT),
        "false_positives": false_positives,
        "fp_count": len(false_positives),
        "fp_rate": len(false_positives) / len(LEGITIMATE_CONTENT) * 100 if LEGITIMATE_CONTENT else 0
    }


def identify_problematic_rules(results: dict) -> List[dict]:
    """Find rules that trigger too often on legitimate content."""
    rule_frequency = defaultdict(int)
    
    for fp in results["false_positives"]:
        for rule in fp.get("triggered_rules", []):
            rule_id = rule.get("rule_id", "")
            rule_frequency[rule_id] += 1
    
    problematic = []
    for rule_id, count in sorted(rule_frequency.items(), key=lambda x: -x[1]):
        if count >= 2:
            problematic.append({
                "rule_id": rule_id,
                "trigger_count": count,
                "recommendation": f"Consider adjusting threshold for {rule_id}"
            })
    
    return problematic


def identify_problematic_phrases(results: dict) -> List[dict]:
    """Find phrases that trigger on legitimate content."""
    phrase_frequency = defaultdict(int)
    
    for fp in results["false_positives"]:
        for phrase in fp.get("triggered_phrases", []):
            phrase_text = phrase.get("phrase", "")
            phrase_frequency[phrase_text] += 1
    
    problematic = []
    for phrase, count in sorted(phrase_frequency.items(), key=lambda x: -x[1]):
        if count >= 1:
            problematic.append({
                "phrase": phrase,
                "trigger_count": count,
                "recommendation": f"Review phrase '{phrase}' for false positive risk"
            })
    
    return problematic


def suggest_fixes(rule_issues: List[dict], phrase_issues: List[dict]) -> List[dict]:
    """Suggest fixes for false positive issues."""
    suggestions = []
    
    for rule in rule_issues:
        suggestions.append({
            "type": "rule_adjustment",
            "target": rule["rule_id"],
            "suggestion": f"Increase risk score threshold for {rule['rule_id']} to reduce false positives",
            "priority": "high" if rule["trigger_count"] >= 3 else "medium"
        })
    
    for phrase in phrase_issues:
        suggestions.append({
            "type": "phrase_review",
            "target": phrase["phrase"],
            "suggestion": f"Consider adding '{phrase['phrase']}' to legitimate whitelist or reducing confidence",
            "priority": "high" if phrase["trigger_count"] >= 2 else "low"
        })
    
    return suggestions


def generate_audit_report(results: dict, rule_issues: List[dict], 
                          phrase_issues: List[dict], suggestions: List[dict]) -> dict:
    """Generate full audit report."""
    return {
        "audit_summary": {
            "total_legitimate_content": results["total_legitimate"],
            "false_positives_detected": results["fp_count"],
            "false_positive_rate": f"{results['fp_rate']:.1f}%",
            "threshold_used": results["threshold"],
            "grade": "A" if results["fp_rate"] < 5 else "B" if results["fp_rate"] < 10 else "C" if results["fp_rate"] < 20 else "D"
        },
        "false_positives": results["false_positives"],
        "problematic_rules": rule_issues,
        "problematic_phrases": phrase_issues,
        "suggestions": suggestions
    }


def main():
    parser = argparse.ArgumentParser(description="Audit false positives in TrustLens AI")
    parser.add_argument("--threshold", type=float, default=0.85, help="Risk score threshold for FP detection")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    print("Analyzing false positives...")
    results = analyze_false_positives(args.threshold)
    
    print(f"\n{'='*60}")
    print("FALSE POSITIVE AUDIT REPORT")
    print(f"{'='*60}")
    
    print(f"\nSummary:")
    print(f"  Legitimate content tested: {results['total_legitimate']}")
    print(f"  False positives detected:  {results['fp_count']}")
    print(f"  False positive rate:       {results['fp_rate']:.1f}%")
    
    # Identify issues
    rule_issues = identify_problematic_rules(results)
    phrase_issues = identify_problematic_phrases(results)
    suggestions = suggest_fixes(rule_issues, phrase_issues)
    
    if results["false_positives"]:
        print(f"\nFalse Positives:")
        for fp in results["false_positives"]:
            print(f"  [{fp['risk_level']}] Score: {fp['risk_score']:.3f}")
            print(f"    \"{fp['content'][:80]}...\"")
            if fp.get("triggered_phrases"):
                print(f"    Triggered phrases: {[p.get('phrase') for p in fp['triggered_phrases']]}")
            if fp.get("triggered_rules"):
                print(f"    Triggered rules: {[r.get('rule_id') for r in fp['triggered_rules']]}")
    
    if rule_issues:
        print(f"\nProblematic Rules:")
        for rule in rule_issues:
            print(f"  {rule['rule_id']}: triggered {rule['trigger_count']} times")
    
    if phrase_issues:
        print(f"\nProblematic Phrases:")
        for phrase in phrase_issues:
            print(f"  \"{phrase['phrase']}\": triggered {phrase['trigger_count']} times")
    
    if suggestions:
        print(f"\nSuggestions:")
        for s in suggestions:
            print(f"  [{s['priority'].upper()}] {s['suggestion']}")
    
    # Save report
    report = generate_audit_report(results, rule_issues, phrase_issues, suggestions)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fp_audit_report.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nReport saved to {output_path}")
    
    print(f"\nGrade: {report['audit_summary']['grade']}")


if __name__ == "__main__":
    main()
