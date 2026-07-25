#!/usr/bin/env python3
"""Dataset import and validation script for TrustLens AI."""
import json
import os
import sys
import argparse
from typing import Dict, List, Any


DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets')

DATASET_SCHEMAS = {
    "hinglish_phrases": {
        "required_fields": ["version", "phrases"],
        "phrase_fields": ["phrase", "type", "language", "variations", "confidence", "scam_category", "example_context"],
        "valid_types": ["threat", "urgency", "reward", "credential_request", "payment_request", "authority_impersonation"]
    },
    "scam_templates": {
        "required_fields": ["version", "templates"],
        "template_fields": ["id", "template", "scam_type", "language", "risk_score", "detection_trigger", "red_flags"]
    },
    "phishing_keywords": {
        "required_fields": ["version", "keywords"]
    },
    "bank_names": {
        "required_fields": ["version", "banks"],
        "bank_fields": ["name", "aliases", "legitimate_domains", "common_typos"]
    },
    "upi_patterns": {
        "required_fields": ["version", "patterns"]
    },
    "trusted_domains": {
        "required_fields": ["version", "domains"],
        "domain_fields": ["domain", "entity", "category", "verified"]
    },
    "suspicious_domains": {
        "required_fields": ["version", "domains"],
        "domain_fields": ["domain", "impersonates", "threat_level"]
    },
    "fake_brand_patterns": {
        "required_fields": ["version", "patterns"],
        "pattern_fields": ["legitimate_brand", "impostor_patterns", "keywords"]
    }
}


def load_dataset(name: str) -> dict:
    """Load a dataset JSON file."""
    filepath = os.path.join(DATASETS_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_schema(data: dict, schema: dict) -> tuple:
    """Validate dataset against schema. Returns (is_valid, errors)."""
    errors = []
    for field in schema.get("required_fields", []):
        if field not in data:
            errors.append(f"Missing required field: {field}")
    return (len(errors) == 0, errors)


def check_duplicates(data: dict, dataset_name: str) -> List[str]:
    """Check for duplicate entries in dataset."""
    duplicates = []
    if dataset_name == "hinglish_phrases" and "phrases" in data:
        seen = set()
        for i, phrase in enumerate(data["phrases"]):
            key = phrase.get("phrase", "").lower().strip()
            if key in seen:
                duplicates.append(f"Duplicate phrase at index {i}: {key}")
            seen.add(key)
    return duplicates


def report_quality(data: dict, dataset_name: str) -> dict:
    """Generate quality metrics for dataset."""
    metrics = {"total_entries": 0, "fields_present": 0, "fields_missing": 0, "quality_score": 0.0}
    
    if dataset_name == "hinglish_phrases" and "phrases" in data:
        phrases = data["phrases"]
        metrics["total_entries"] = len(phrases)
        valid_confidence = sum(1 for p in phrases if 0 <= p.get("confidence", 0) <= 1)
        metrics["valid_confidence_scores"] = valid_confidence
        metrics["confidence_score"] = valid_confidence / len(phrases) * 100 if phrases else 0
        
        valid_types = sum(1 for p in phrases if p.get("type") in DATASET_SCHEMAS["hinglish_phrases"]["valid_types"])
        metrics["valid_types"] = valid_types
        metrics["type_score"] = valid_types / len(phrases) * 100 if phrases else 0
        
        metrics["quality_score"] = (metrics["confidence_score"] + metrics["type_score"]) / 2
    
    elif dataset_name == "suspicious_domains" and "domains" in data:
        metrics["total_entries"] = len(data["domains"])
        metrics["quality_score"] = 100.0 if metrics["total_entries"] > 0 else 0.0
    
    elif dataset_name == "trusted_domains" and "domains" in data:
        metrics["total_entries"] = len(data["domains"])
        metrics["quality_score"] = 100.0 if metrics["total_entries"] > 0 else 0.0
    
    else:
        metrics["quality_score"] = 100.0
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Import and validate TrustLens AI datasets")
    parser.add_argument("--dataset", type=str, help="Dataset name to validate")
    parser.add_argument("--validate", action="store_true", help="Run schema validation")
    parser.add_argument("--check-duplicates", action="store_true", help="Check for duplicates")
    parser.add_argument("--quality", action="store_true", help="Generate quality report")
    parser.add_argument("--all", action="store_true", help="Validate all datasets")
    args = parser.parse_args()
    
    datasets_to_check = []
    if args.all:
        datasets_to_check = list(DATASET_SCHEMAS.keys())
    elif args.dataset:
        datasets_to_check = [args.dataset]
    else:
        print("Please specify --dataset or --all")
        sys.exit(1)
    
    for name in datasets_to_check:
        print(f"\n{'='*60}")
        print(f"Validating: {name}")
        print(f"{'='*60}")
        
        try:
            data = load_dataset(name)
            print(f"✓ Loaded {name}")
        except FileNotFoundError as e:
            print(f"✗ {e}")
            continue
        
        if args.validate or args.all:
            schema = DATASET_SCHEMAS.get(name, {})
            is_valid, errors = validate_schema(data, schema)
            if is_valid:
                print(f"✓ Schema validation: PASSED")
            else:
                print(f"✗ Schema validation: FAILED")
                for error in errors:
                    print(f"  - {error}")
        
        if args.check_duplicates or args.all:
            duplicates = check_duplicates(data, name)
            if duplicates:
                print(f"⚠ Found {len(duplicates)} duplicates:")
                for dup in duplicates[:10]:
                    print(f"  - {dup}")
            else:
                print(f"✓ No duplicates found")
        
        if args.quality or args.all:
            metrics = report_quality(data, name)
            print(f"Quality: {metrics['quality_score']:.1f}%")
            print(f"Total entries: {metrics['total_entries']}")


if __name__ == "__main__":
    main()
