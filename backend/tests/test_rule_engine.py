"""
TrustLens AI - Rule Engine Unit Tests
Tests multi-category scam rule detection.
"""

import pytest
from backend.detection.rule_engine import RuleEngine


@pytest.fixture
def rule_engine_instance():
    return RuleEngine()


def test_otp_scam_detection(rule_engine_instance):
    text = "Dear customer, please tell me your OTP to verify SBI netbanking transaction."
    result = rule_engine_instance.evaluate(text)
    assert "OTP Scam" in result["categories_triggered"]
    assert result["rule_risk_score"] >= 30


def test_kyc_scam_detection(rule_engine_instance):
    text = "Your SIM card KYC is pending. Upload Aadhaar immediately to prevent SIM block."
    result = rule_engine_instance.evaluate(text)
    assert "KYC Scam" in result["categories_triggered"]


def test_bank_impersonation_detection(rule_engine_instance):
    text = "Dear HDFC user, your account has been blocked due to suspicious activity."
    result = rule_engine_instance.evaluate(text)
    assert "Bank Impersonation" in result["categories_triggered"]


def test_delivery_scam_detection(rule_engine_instance):
    text = "India Post parcel stuck due to invalid address. Pay Rs 25 delivery fee now."
    result = rule_engine_instance.evaluate(text)
    assert "Delivery Scam" in result["categories_triggered"]


def test_lottery_scam_detection(rule_engine_instance):
    text = "Congratulations! You have won Rs 25 Lakh in KBC Lucky Draw."
    result = rule_engine_instance.evaluate(text)
    assert "Lottery & Prize Scam" in result["categories_triggered"]


def test_safe_content(rule_engine_instance):
    text = "Hey, let's meet tomorrow for coffee at 5 PM."
    result = rule_engine_instance.evaluate(text)
    assert len(result["categories_triggered"]) == 0
    assert result["rule_risk_score"] == 0
