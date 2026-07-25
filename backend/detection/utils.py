"""Utility functions for TrustLens AI detection layer."""
import re
import unicodedata
from urllib.parse import urlparse
from difflib import SequenceMatcher
from typing import List, Dict, Optional, Tuple


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, strip, normalize unicode, remove extra spaces."""
    text = text.strip()
    text = unicodedata.normalize('NFKD', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\u0964\u0965\u093c\u094d\u0902\u0940\u0948\u0942\u094c]', '', text)
    return text.strip()


def remove_special_chars(text: str) -> str:
    """Remove special characters while keeping alphanumeric and spaces."""
    text = re.sub(r'[^\w\s.,!?;:\'"-/()₹$%@#&+]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text."""
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2})|[^\s])+'
    urls = re.findall(url_pattern, text)
    no_protocol_pattern = r'(?<![/\w])(?:www\.)?(?:[-\w.]|(?:%[\da-fA-F]{2})|[^\s])+\.(?:com|in|org|net|gov|edu|co|io|info|biz|xyz|top|club|online|site|tech|store)\b(?:/[^\s]*)?'
    bare_urls = re.findall(no_protocol_pattern, text)
    for u in bare_urls:
        if not u.startswith('http') and u not in urls:
            if not any(u in existing for existing in urls):
                urls.append(u)
    return urls


def extract_numbers(text: str) -> List[str]:
    """Extract all numbers from text (including Indian number formats)."""
    indian_comma_pattern = r'\b\d{1,3}(?:,\d{2})*\b'
    western_comma_pattern = r'\b\d{1,3}(?:,\d{3})+\b'
    plain_pattern = r'\b\d+(?:\.\d+)?\b'
    indian_numbers = re.findall(indian_comma_pattern, text)
    western_numbers = re.findall(western_comma_pattern, text)
    plain_numbers = re.findall(plain_pattern, text)
    all_numbers = set()
    for n in western_numbers:
        all_numbers.add(n)
    for n in indian_numbers:
        if n not in all_numbers:
            all_numbers.add(n)
    for n in plain_numbers:
        if n not in all_numbers:
            all_numbers.add(n)
    return sorted(all_numbers, key=lambda x: text.index(x))


def fuzzy_match(text: str, target: str, threshold: float = 0.8) -> bool:
    """Check if text fuzzy matches target above threshold."""
    ratio = SequenceMatcher(None, text.lower(), target.lower()).ratio()
    return ratio >= threshold


def regex_match(text: str, pattern: str) -> List[re.Match]:
    """Find all regex matches in text."""
    compiled = re.compile(pattern, re.IGNORECASE)
    return list(compiled.finditer(text))


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def extract_domain(url: str) -> str:
    """Extract domain from URL, handling subdomains."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    if ':' in domain:
        domain = domain.split(':')[0]
    domain = domain.lower().strip('.')
    return domain


def is_typosquat(domain: str, legitimate: str, threshold: float = 0.85) -> bool:
    """Check if domain is a typosquat of a legitimate domain."""
    domain = extract_domain(domain).lower()
    legit_parts = legitimate.lower().split('.')
    domain_parts = domain.split('.')
    legit_name = legit_parts[0] if legit_parts else legitimate.lower()
    domain_name = domain_parts[0] if domain_parts else domain.lower()
    if domain_name == legit_name:
        return False
    ratio = SequenceMatcher(None, domain_name, legit_name).ratio()
    if ratio >= threshold and ratio < 1.0:
        return True
    if len(domain_name) == len(legit_name):
        swaps = sum(1 for a, b in zip(domain_name, legit_name) if a != b)
        if swaps <= 2:
            return True
    char_map = {'0': 'o', 'o': '0', '1': 'l', 'l': '1', 'i': '1', '1': 'i',
                '5': 's', 's': '5', '8': 'b', 'b': '8', '@': 'a', 'a': '@'}
    substituted = ''
    for c in domain_name:
        substituted += char_map.get(c, c)
    sub_ratio = SequenceMatcher(None, substituted, legit_name).ratio()
    if sub_ratio >= threshold:
        return True
    if len(domain_parts) > len(legit_parts):
        possible_tld = domain_parts[-1]
        known_tlds = {'com', 'in', 'org', 'net', 'gov', 'edu', 'co', 'io',
                       'info', 'biz', 'xyz', 'top', 'club', 'online', 'site'}
        if possible_tld not in known_tlds and len(possible_tld) <= 3:
            reconstructed = '.'.join(domain_parts[:-1])
            if SequenceMatcher(None, reconstructed, legitimate.lower()).ratio() >= threshold:
                return True
    if '-' in domain_name and legit_name.replace('-', '') == domain_name.replace('-', ''):
        return True
    return False


def get_domain_age(domain: str) -> Optional[int]:
    """Get domain age in days (placeholder - returns None without WHOIS)."""
    return None


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Normalize score to 0-1 range."""
    return max(min_val, min(max_val, score))


def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """Calculate weighted average of scores."""
    total_weight = sum(weights.get(k, 0) for k in scores)
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(scores[k] * weights.get(k, 0) for k in scores)
    return weighted_sum / total_weight


def load_json_dataset(filepath: str) -> dict:
    """Load a JSON dataset file."""
    import json
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_dataset_path(filename: str) -> str:
    """Get full path to a dataset file."""
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'datasets', filename)
