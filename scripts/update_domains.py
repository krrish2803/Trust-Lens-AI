#!/usr/bin/env python3
"""Update suspicious domains dataset from external sources."""
import json
import os
import sys
import argparse
import hashlib
from datetime import datetime
from typing import List, Dict, Set


DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets')


def load_current_domains() -> List[dict]:
    """Load current suspicious domains."""
    filepath = os.path.join(DATASETS_DIR, "suspicious_domains.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("domains", [])
    return []


def fetch_phishtank_domains() -> List[dict]:
    """Fetch latest phishing domains from PhishTank (placeholder)."""
    # In production, this would call PhishTank API
    # For now, return sample domains
    print("  PhishTank: Would fetch from API (placeholder)")
    return [
        {"domain": "sbi-secure-login.tk", "impersonates": "SBI", "threat_level": "critical", "first_seen": "2026-07-20", "category": "banking"},
        {"domain": "icici-verify.ml", "impersonates": "ICICI", "threat_level": "critical", "first_seen": "2026-07-19", "category": "banking"},
        {"domain": "hdfc-kyc-update.ga", "impersonates": "HDFC", "threat_level": "critical", "first_seen": "2026-07-18", "category": "banking"},
    ]


def fetch_urlhaus_domains() -> List[dict]:
    """Fetch latest phishing domains from URLhaus (placeholder)."""
    print("  URLhaus: Would fetch from API (placeholder)")
    return [
        {"domain": "paytm-cashback.xyz", "impersonates": "Paytm", "threat_level": "high", "first_seen": "2026-07-21", "category": "payment"},
        {"domain": "phonepe-offer.top", "impersonates": "PhonePe", "threat_level": "high", "first_seen": "2026-07-20", "category": "payment"},
    ]


def fetch_google_safe_browsing() -> List[dict]:
    """Fetch from Google Safe Browsing API (placeholder)."""
    print("  Google Safe Browsing: Would fetch from API (placeholder)")
    return []


def merge_sources(domains: List[List[dict]]) -> List[dict]:
    """Merge and deduplicate domain lists."""
    seen = set()
    merged = []
    
    for source in domains:
        for domain in source:
            key = domain.get("domain", "").lower()
            if key and key not in seen:
                seen.add(key)
                merged.append(domain)
    
    return merged


def update_dataset(current: List[dict], new_domains: List[dict]) -> tuple:
    """Update dataset with new domains. Returns (updated_list, changelog)."""
    current_set = {d.get("domain", "").lower() for d in current}
    changelog = []
    
    updated = list(current)
    for domain in new_domains:
        domain_key = domain.get("domain", "").lower()
        if domain_key not in current_set:
            updated.append(domain)
            changelog.append({
                "action": "added",
                "domain": domain.get("domain"),
                "impersonates": domain.get("impersonates"),
                "threat_level": domain.get("threat_level"),
                "date": datetime.now().isoformat()
            })
    
    return updated, changelog


def save_dataset(domains: List[dict], output_dir: str):
    """Save updated domains dataset."""
    data = {
        "version": "1.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_domains": len(domains),
        "domains": domains
    }
    
    filepath = os.path.join(output_dir, "suspicious_domains.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(domains)} domains to {filepath}")


def generate_changelog(changelog: List[dict], output_dir: str):
    """Save changelog of domain updates."""
    filepath = os.path.join(output_dir, "domain_changelog.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "last_update": datetime.now().isoformat(),
            "changes": changelog
        }, f, indent=2)
    
    print(f"✓ Changelog saved to {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Update TrustLens AI suspicious domains")
    parser.add_argument("--source", choices=["phishtank", "urlhaus", "google", "all"], default="all")
    parser.add_argument("--output", type=str, default=DATASETS_DIR)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving")
    args = parser.parse_args()
    
    print("Loading current domains...")
    current = load_current_domains()
    print(f"Current: {len(current)} domains")
    
    print("\nFetching new domains...")
    sources = []
    if args.source in ["phishtank", "all"]:
        sources.append(fetch_phishtank_domains())
    if args.source in ["urlhaus", "all"]:
        sources.append(fetch_urlhaus_domains())
    if args.source in ["google", "all"]:
        sources.append(fetch_google_safe_browsing())
    
    new_domains = merge_sources(sources)
    print(f"Fetched: {len(new_domains)} new domains")
    
    updated, changelog = update_dataset(current, new_domains)
    print(f"After merge: {len(updated)} total domains")
    print(f"New additions: {len(changelog)}")
    
    if args.dry_run:
        print("\n[DRY RUN] Changes preview:")
        for change in changelog[:10]:
            print(f"  + {change['domain']} (impersonates: {change['impersonates']}, threat: {change['threat_level']})")
    else:
        save_dataset(updated, args.output)
        generate_changelog(changelog, args.output)
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
