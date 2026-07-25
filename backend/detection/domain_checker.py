"""Domain reputation checker for detecting fraudulent domains."""
import re
from typing import List, Dict, Optional, Tuple
from .utils import extract_domain, is_typosquat, levenshtein_distance, load_json_dataset, get_dataset_path


# Character confusion map (similar looking characters)
CHAR_CONFUSION = {
    '0': ['o', 'O'], 'O': ['0', 'o'],
    '1': ['l', 'I', '|'], 'l': ['1', 'I', '|'], 'I': ['1', 'l', '|'],
    '5': ['S', 's'], 'S': ['5', 's'],
    '8': ['B'], 'B': ['8'],
    '6': ['G'], 'G': ['6'],
    '2': ['Z', 'z'], 'Z': ['2', 'z'],
    'rn': ['m'], 'm': ['rn'],
    'cl': ['d'], 'd': ['cl'],
    'vv': ['w'], 'w': ['vv'],
}

SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.work', '.buzz', '.icu']


class DomainChecker:
    """Check domain reputation and detect impersonation patterns."""

    def __init__(self):
        self.trusted_domains = self._load_trusted_domains()
        self.suspicious_domains = self._load_suspicious_domains()
        self.bank_data = self._load_bank_data()

    def _load_trusted_domains(self) -> List[dict]:
        """Load trusted domains from dataset."""
        try:
            data = load_json_dataset(get_dataset_path('trusted_domains.json'))
            return data.get('domains', [])
        except Exception:
            return []

    def _load_suspicious_domains(self) -> List[dict]:
        """Load suspicious domains from dataset."""
        try:
            data = load_json_dataset(get_dataset_path('suspicious_domains.json'))
            return data.get('domains', [])
        except Exception:
            return []

    def _load_bank_data(self) -> List[dict]:
        """Load bank names data from dataset."""
        try:
            data = load_json_dataset(get_dataset_path('bank_names.json'))
            return data.get('banks', [])
        except Exception:
            return []

    def check(self, domain: str) -> dict:
        """
        Check domain reputation.

        Input: domain (str)
        Output: {
            "domain": str,
            "status": str (trusted|suspicious|unknown|malicious),
            "reputation_score": float (0-1),
            "reasons": [str],
            "similar_legitimate": str or None
        }
        """
        domain = extract_domain(domain).lower()
        reasons = []
        checks = {
            'trusted': False,
            'suspicious': False,
            'character_confusion': False,
            'hyphen_abuse': False,
            'suspicious_tld': False,
            'threat_level': None,
        }

        trusted_match = self._check_trusted(domain)
        if trusted_match:
            checks['trusted'] = True
            reasons.append(f"Verified trusted domain: {trusted_match['entity']}")

        suspicious_match = None if checks['trusted'] else self._check_suspicious(domain)
        if suspicious_match:
            checks['suspicious'] = True
            checks['threat_level'] = suspicious_match.get('threat_level', 'unknown')
            reasons.append(f"Known malicious domain impersonating: {suspicious_match.get('impersonates', 'unknown')}")

        if not checks['trusted']:
            confusion_flags = self._check_character_confusion(domain)
            if confusion_flags:
                checks['character_confusion'] = True
                reasons.extend(confusion_flags)

            if self._check_hyphen_abuse(domain):
                checks['hyphen_abuse'] = True
                reasons.append("Excessive hyphens detected — common in phishing domains")

            if self._check_suspicious_tld(domain):
                checks['suspicious_tld'] = True
                reasons.append("Suspicious TLD detected")

        score = self._calculate_reputation_score(checks)
        status = self._determine_status(score, checks)
        similar = self._find_similar_legitimate(domain) if not checks['trusted'] else None

        if similar and not checks['trusted']:
            reasons.append(f"Possible impersonation of {similar}")

        return {
            "domain": domain,
            "status": status,
            "reputation_score": score,
            "reasons": reasons,
            "similar_legitimate": similar,
        }

    def _check_trusted(self, domain: str) -> Optional[dict]:
        """Check if domain is in trusted list."""
        for entry in self.trusted_domains:
            trusted_domain = entry.get('domain', '').lower()
            if domain == trusted_domain or domain.endswith('.' + trusted_domain):
                return entry
        for entry in self.bank_data:
            for legit_domain in entry.get('legitimate_domains', []):
                if domain == legit_domain.lower() or domain.endswith('.' + legit_domain.lower()):
                    return {
                        'domain': legit_domain,
                        'entity': entry['name'],
                        'category': 'banking',
                        'verified': True,
                    }
        return None

    def _check_suspicious(self, domain: str) -> Optional[dict]:
        """Check if domain is in suspicious list."""
        for entry in self.suspicious_domains:
            suspicious_domain = entry.get('domain', '').lower()
            if domain == suspicious_domain or is_typosquat(domain, suspicious_domain, threshold=0.9):
                return entry
        for entry in self.bank_data:
            for typo in entry.get('common_typos', []):
                if domain == typo.lower() or is_typosquat(domain, typo, threshold=0.9):
                    return {
                        'domain': typo,
                        'impersonates': entry['name'],
                        'threat_level': 'high',
                    }
        return None

    def _check_character_confusion(self, domain: str) -> List[str]:
        """Check for character confusion patterns."""
        flags = []
        name_part = domain.split('.')[0]

        for pattern, confusables in CHAR_CONFUSION.items():
            if pattern in name_part:
                for confusable in confusables:
                    replaced = name_part.replace(pattern, confusable)
                    for entry in self.trusted_domains:
                        legit_name = entry.get('domain', '').split('.')[0].lower()
                        if replaced == legit_name:
                            flags.append(
                                f"Character confusion: '{pattern}' looks like '{confusable}' "
                                f"(may impersonate {entry['entity']})"
                            )
                            break
                    for entry in self.bank_data:
                        for alias in entry.get('aliases', []):
                            if replaced == alias.lower():
                                flags.append(
                                    f"Character confusion: '{pattern}' looks like '{confusable}' "
                                    f"(may impersonate {entry['name']})"
                                )
                                break

        for seq, confusable_char in [('rn', 'm'), ('cl', 'd'), ('vv', 'w')]:
            if seq in name_part:
                normalized = name_part.replace(seq, confusable_char)
                for entry in self.trusted_domains:
                    legit_name = entry.get('domain', '').split('.')[0].lower()
                    if normalized == legit_name:
                        flags.append(
                            f"Confusable sequence: '{seq}' looks like '{confusable_char}' "
                            f"(may impersonate {entry['entity']})"
                        )
                        break

        return flags

    def _check_hyphen_abuse(self, domain: str) -> bool:
        """Check for excessive hyphens (icici-bank vs icicibank)."""
        name_part = domain.split('.')[0]
        hyphen_count = name_part.count('-')
        if hyphen_count >= 2:
            return True
        if hyphen_count == 1:
            for entry in self.bank_data:
                for alias in entry.get('aliases', []):
                    alias_no_hyphen = alias.lower().replace('-', '')
                    name_no_hyphen = name_part.replace('-', '')
                    if name_no_hyphen == alias_no_hyphen:
                        return True
            for entry in self.trusted_domains:
                legit_name = entry.get('domain', '').split('.')[0].lower()
                name_no_hyphen = name_part.replace('-', '')
                if legit_name.replace('-', '') == name_no_hyphen and name_no_hyphen != legit_name:
                    return True
        return False

    def _check_suspicious_tld(self, domain: str) -> bool:
        """Check for suspicious TLD usage."""
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                for entry in self.bank_data:
                    for alias in entry.get('aliases', []):
                        if alias.lower() in domain:
                            return True
                for entry in self.trusted_domains:
                    legit_name = entry.get('domain', '').split('.')[0].lower()
                    if legit_name in domain:
                        return True
        return False

    def _find_similar_legitimate(self, domain: str) -> Optional[str]:
        """Find the most similar legitimate domain."""
        name_part = domain.split('.')[0]
        best_match = None
        best_distance = float('inf')

        for entry in self.trusted_domains:
            legit_domain = entry.get('domain', '')
            legit_name = legit_domain.split('.')[0].lower()
            dist = levenshtein_distance(name_part, legit_name)
            if dist < best_distance and dist <= 3:
                best_distance = dist
                best_match = legit_domain

        for entry in self.bank_data:
            for alias in entry.get('aliases', []):
                dist = levenshtein_distance(name_part, alias.lower())
                if dist < best_distance and dist <= 3:
                    best_distance = dist
                    best_match = entry.get('legitimate_domains', [None])[0]
            for typo in entry.get('common_typos', []):
                if domain == typo.lower():
                    return entry.get('legitimate_domains', [None])[0]

        if best_distance <= 2 and best_match:
            return best_match
        return None

    def _calculate_reputation_score(self, checks: dict) -> float:
        """Calculate overall reputation score."""
        if checks['trusted']:
            return 0.95

        score = 0.5

        if checks['suspicious']:
            threat = checks.get('threat_level', 'medium')
            threat_penalty = {'critical': 0.45, 'high': 0.35, 'medium': 0.25, 'low': 0.15}
            score -= threat_penalty.get(threat, 0.25)

        if checks['character_confusion']:
            score -= 0.2
        if checks['hyphen_abuse']:
            score -= 0.1
        if checks['suspicious_tld']:
            score -= 0.15

        return max(0.0, min(1.0, score))

    def _determine_status(self, score: float, checks: dict) -> str:
        """Determine domain status based on checks."""
        if checks['trusted']:
            return 'trusted'
        if checks['suspicious'] and checks.get('threat_level') in ('critical', 'high'):
            return 'malicious'
        if checks['suspicious']:
            return 'suspicious'
        if score < 0.3:
            return 'malicious'
        if score < 0.6:
            return 'suspicious'
        if score >= 0.8:
            return 'trusted'
        return 'unknown'
