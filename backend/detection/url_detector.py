"""
TrustLens AI - URL Detector Module
Detects phishing URLs and suspicious domain patterns.
"""

import re
from urllib.parse import urlparse
from typing import List, Dict, Optional
from .utils import extract_domain, is_typosquat, load_json_dataset, get_dataset_path


SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.work', '.buzz',
    '.icu', '.vip', '.win', '.loan', '.download', '.racing', '.date', '.stream',
    '.accountant', '.bid', '.webcam', '.science', '.cricket', '.party', '.review',
    '.faith', '.choice', '.trade', '.dynamic', '.predict', '.click'
]

LEGITIMATE_BANKING = [
    'sbi.co.in', 'hdfcbank.com', 'icicibank.com', 'axisbank.com', 'yesbank.in',
    'kotak.com', 'pnbindia.com', 'bankofbaroda.com', 'canarabank.com',
    'unionbankofindia.co.in', 'idbibank.in', 'indianbank.in', 'centralbankofindia.co.in',
    'ucobank.co.in', 'bankofindia.co.in', 'finobank.com', 'airtelbank.in',
    'paytmbank.com', 'jio.com', 'indiapost.gov.in'
]

URL_SHORTENERS = [
    'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly',
    'adf.ly', 'bc.vc', 'tiny.cc', 'lnkd.in', 'rb.gy', 'cutt.ly', 'v.gd',
    'tr.im', 'url.to', 'snipurl.com', 'short.to', 'po.st', 'cli.gs'
]

PHISHING_KEYWORDS = [
    'login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm',
    'validate', 'credential', 'suspend', 'restrict', 'urgent', 'immediate',
    'alert', 'notification', 'portal', 'auth', 'signin', 'signup', 'unlock',
    'kyc', 'refund', 'reversal', 'claim', 'prize', 'reward', 'lucky', 'winner'
]


class URLDetector:
    """Detects phishing URLs and suspicious domain patterns."""

    def __init__(self):
        self.trusted_domains = self._load_trusted_domains()
        self.suspicious_domains = self._load_suspicious_domains()
        self.bank_names = self._load_bank_names()

    def _load_trusted_domains(self) -> List[str]:
        try:
            data = load_json_dataset(get_dataset_path('trusted_domains.json'))
            return [d['domain'].lower() for d in data.get('domains', [])]
        except (FileNotFoundError, KeyError):
            return []

    def _load_suspicious_domains(self) -> List[dict]:
        try:
            data = load_json_dataset(get_dataset_path('suspicious_domains.json'))
            return data.get('domains', [])
        except (FileNotFoundError, KeyError):
            return []

    def _load_bank_names(self) -> List[dict]:
        try:
            data = load_json_dataset(get_dataset_path('bank_names.json'))
            return data.get('banks', [])
        except (FileNotFoundError, KeyError):
            return []

    def detect(self, url: str) -> dict:
        indicators = []
        domain = extract_domain(url)

        checks = [
            self._check_suspicious_tld(domain),
            self._check_domain_squatting(domain),
            self._check_typosquatting(domain),
            self._check_subdomain_abuse(url),
            self._check_ip_address(domain),
            self._check_url_shortener(url),
            self._check_https(url),
            self._check_suspicious_patterns(domain),
            self._check_known_suspicious(domain),
        ]

        for result in checks:
            if result is not None:
                indicators.append(result)

        final_risk = self._calculate_final_risk(indicators)
        verdict = self._generate_verdict(final_risk)
        recommendation = self._generate_recommendation(verdict, indicators)

        is_phishing = bool(final_risk >= 0.40 or len(indicators) > 0)
        findings = [i.get("evidence", i.get("indicator", "")) for i in indicators]

        return {
            "url": url,
            "is_phishing": is_phishing,
            "risk_score": final_risk,
            "findings": findings,
            "risk_indicators": indicators,
            "final_url_risk": final_risk,
            "verdict": verdict,
            "recommendation": recommendation,
        }

    def _check_suspicious_tld(self, domain: str) -> Optional[dict]:
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                return {
                    "indicator": "suspicious_tld",
                    "evidence": f"Domain uses suspicious TLD: {tld}",
                    "risk_score": 0.6,
                }
        return None

    def _check_domain_squatting(self, domain: str) -> Optional[dict]:
        domain_name = domain.split('.')[0] if '.' in domain else domain

        for bank in self.bank_names:
            for alias in bank.get('aliases', []):
                alias_lower = alias.lower()
                if alias_lower in domain and alias_lower != domain_name:
                    return {
                        "indicator": "domain_squatting",
                        "evidence": f"Domain contains bank name '{alias}' but is not an official domain",
                        "risk_score": 0.85,
                    }

            legit_domains = bank.get('legitimate_domains', [])
            for legit in legit_domains:
                legit_name = legit.split('.')[0].lower()
                if domain != legit and domain_name == legit_name:
                    return {
                        "indicator": "domain_squatting",
                        "evidence": f"Domain mimics '{bank['name']}' with exact name match on non-official domain",
                        "risk_score": 0.9,
                    }

        for brand in ['paytm', 'phonepe', 'gpay', 'googlepe', 'amazon', 'flipkart',
                       'myntra', 'snapdeal', 'swiggy', 'zomato', 'olx', 'meesho',
                       'cred', 'slice', 'jupiter', 'mobikwik', 'freecharge']:
            if brand in domain and domain not in self.trusted_domains:
                return {
                    "indicator": "domain_squatting",
                    "evidence": f"Domain contains brand name '{brand}' but is not a trusted domain",
                    "risk_score": 0.8,
                }

        return None

    def _check_typosquatting(self, domain: str) -> Optional[dict]:
        domain_name = domain.split('.')[0] if '.' in domain else domain

        for trusted in self.trusted_domains:
            trusted_name = trusted.split('.')[0]
            if domain == trusted:
                continue
            if is_typosquat(domain, trusted, threshold=0.85):
                return {
                    "indicator": "typosquatting",
                    "evidence": f"Domain is a likely typo of '{trusted}'",
                    "risk_score": 0.85,
                }

        for bank in self.bank_names:
            for typo in bank.get('common_typos', []):
                if domain == typo.lower():
                    return {
                        "indicator": "typosquatting",
                        "evidence": f"Domain matches known typo for '{bank['name']}': {typo}",
                        "risk_score": 0.9,
                    }

        return None

    def _check_subdomain_abuse(self, url: str) -> Optional[dict]:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        parsed = urlparse(url)
        hostname = parsed.hostname or ''

        parts = hostname.split('.')
        if len(parts) > 3:
            subdomain_part = '.'.join(parts[:-2])
            for bank in self.bank_names:
                for alias in bank.get('aliases', []):
                    if alias.lower() in subdomain_part.lower():
                        return {
                            "indicator": "subdomain_abuse",
                            "evidence": f"Bank name '{alias}' found in subdomain: {hostname}",
                            "risk_score": 0.8,
                        }

            for keyword in PHISHING_KEYWORDS:
                if keyword in hostname.lower():
                    for alias in [b['short_name'] for b in self.bank_names if 'short_name' in b]:
                        if alias.lower() in hostname.lower():
                            return {
                                "indicator": "subdomain_abuse",
                                "evidence": f"Suspicious subdomain with phishing keyword and bank name: {hostname}",
                                "risk_score": 0.85,
                            }

        return None

    def _check_ip_address(self, domain: str) -> Optional[dict]:
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, domain):
            return {
                "indicator": "ip_address_url",
                "evidence": f"Domain is an IP address: {domain}",
                "risk_score": 0.9,
            }
        return None

    def _check_url_shortener(self, url: str) -> Optional[dict]:
        domain = extract_domain(url)
        for shortener in URL_SHORTENERS:
            if domain == shortener or domain.endswith('.' + shortener):
                return {
                    "indicator": "url_shortener",
                    "evidence": f"URL uses shortener service: {shortener}",
                    "risk_score": 0.5,
                }
        return None

    def _check_https(self, url: str) -> Optional[dict]:
        if not url.startswith(('http://', 'https://')):
            return {
                "indicator": "no_https",
                "evidence": "URL does not specify a protocol (defaults to HTTP)",
                "risk_score": 0.4,
            }
        if url.startswith('http://'):
            return {
                "indicator": "no_https",
                "evidence": "URL uses HTTP instead of HTTPS",
                "risk_score": 0.5,
            }
        return None

    def _check_suspicious_patterns(self, domain: str) -> Optional[dict]:
        domain_name = domain.split('.')[0] if '.' in domain else domain

        hyphen_count = domain_name.count('-')
        if hyphen_count >= 3:
            return {
                "indicator": "suspicious_pattern",
                "evidence": f"Domain has excessive hyphens ({hyphen_count}): {domain_name}",
                "risk_score": 0.6,
            }

        digit_count = sum(c.isdigit() for c in domain_name)
        if len(domain_name) > 0 and digit_count / len(domain_name) > 0.5:
            return {
                "indicator": "suspicious_pattern",
                "evidence": f"Domain contains excessive numbers ({digit_count}/{len(domain_name)}): {domain_name}",
                "risk_score": 0.6,
            }

        if len(domain_name) > 8:
            unique_chars = set(domain_name)
            if len(unique_chars) / len(domain_name) < 0.3:
                return {
                    "indicator": "suspicious_pattern",
                    "evidence": f"Domain has low character diversity: {domain_name}",
                    "risk_score": 0.5,
                }

        if re.search(r'(.)\1{3,}', domain_name):
            return {
                "indicator": "suspicious_pattern",
                "evidence": f"Domain contains excessive character repetition: {domain_name}",
                "risk_score": 0.5,
            }

        if len(domain_name) >= 6 and re.match(r'^[a-z]+\d+$', domain_name):
            return {
                "indicator": "suspicious_pattern",
                "evidence": f"Domain matches common phishing pattern (word+numbers): {domain_name}",
                "risk_score": 0.5,
            }

        return None

    def _check_known_suspicious(self, domain: str) -> Optional[dict]:
        for entry in self.suspicious_domains:
            if entry.get('domain', '').lower() == domain.lower():
                threat = entry.get('threat_level', 'unknown')
                score_map = {'critical': 0.95, 'high': 0.85, 'medium': 0.7, 'low': 0.5}
                return {
                    "indicator": "known_suspicious",
                    "evidence": f"Domain is in known suspicious list (threat: {threat}, impersonates: {entry.get('impersonates', 'unknown')})",
                    "risk_score": score_map.get(threat, 0.7),
                }

        return None

    def _calculate_final_risk(self, indicators: List[dict]) -> float:
        if not indicators:
            return 0.0

        max_score = max(i['risk_score'] for i in indicators)
        avg_score = sum(i['risk_score'] for i in indicators) / len(indicators)
        count_bonus = min(len(indicators) * 0.05, 0.2)

        final = 0.6 * max_score + 0.4 * avg_score + count_bonus
        return round(min(final, 1.0), 3)

    def _generate_verdict(self, risk_score: float) -> str:
        if risk_score >= 0.7:
            return "malicious"
        elif risk_score >= 0.4:
            return "suspicious"
        return "safe"

    def _generate_recommendation(self, verdict: str, indicators: List[dict]) -> str:
        if verdict == "safe":
            return "This URL appears safe. No significant risk indicators detected."

        indicator_types = [i['indicator'] for i in indicators]

        if 'known_suspicious' in indicator_types:
            entry = next(
                (i for i in indicators if i['indicator'] == 'known_suspicious'), None
            )
            return (
                f"BLOCK: This domain is confirmed malicious. {entry['evidence'] if entry else ''} "
                "Do not visit or enter any personal information."
            )

        if 'ip_address_url' in indicator_types:
            return (
                "BLOCK: This URL uses an IP address instead of a domain name, which is a "
                "strong phishing indicator. Legitimate services use proper domain names."
            )

        if 'typosquatting' in indicator_types or 'domain_squatting' in indicator_types:
            return (
                "BLOCK: This domain appears to impersonate a legitimate service. "
                "It is likely a phishing attempt. Do not enter credentials or personal data."
            )

        if 'subdomain_abuse' in indicator_types:
            return (
                "CAUTION: This URL uses suspicious subdomain tricks to appear legitimate. "
                "Verify the actual domain before entering any information."
            )

        if verdict == "malicious":
            return (
                "HIGH RISK: Multiple suspicious indicators detected. "
                "This URL is likely malicious. Avoid visiting or sharing any personal information."
            )

        return (
            "CAUTION: Some suspicious patterns detected. "
            "Verify this URL through official channels before entering personal information."
        )
