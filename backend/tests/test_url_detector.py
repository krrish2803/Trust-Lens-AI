"""
TrustLens AI - URL Detector Unit Tests
"""

import pytest
from backend.detection.url_detector import URLDetector


@pytest.fixture
def url_detector():
    return URLDetector()


def test_ip_address_url(url_detector):
    res = url_detector.detect("http://192.168.1.1/login.php")
    assert res["is_phishing"] is True
    assert res["risk_score"] > 0.5


def test_suspicious_tld_url(url_detector):
    res = url_detector.detect("http://sbi-verify-kyc.xyz")
    assert res["is_phishing"] is True


def test_legitimate_url(url_detector):
    res = url_detector.detect("https://www.sbi.co.in")
    assert res["is_phishing"] is False
    assert res["risk_score"] < 0.3
