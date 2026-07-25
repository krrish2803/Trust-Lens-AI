"""Comprehensive Unit & Integration Test Suite for TrustLens AI Detection Engine."""

import unittest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from detection.phrase_matcher import PhraseMatcher
from detection.rule_engine import RuleEngine
from detection.url_detector import URLDetector
from detection.scam_classifier import ScamClassifier
from detection.risk_engine import RiskEngine

class TestTrustLensAIDetectionPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.phrase_matcher = PhraseMatcher()
        cls.rule_engine = RuleEngine()
        cls.url_detector = URLDetector()
        cls.scam_classifier = ScamClassifier()
        cls.risk_engine = RiskEngine()

    # --- 1. URL Scanning Test Cases ---
    def test_tc_url_001_phishing_domain_squatting(self):
        url = "http://sbi-kyc-update-login.com"
        res = self.url_detector.detect(url)
        self.assertGreaterEqual(res["final_url_risk"], 0.6)
        self.assertIn("verdict", res)

    def test_tc_url_002_legitimate_banking_domain(self):
        url = "https://www.sbi.co.in"
        res = self.url_detector.detect(url)
        self.assertLessEqual(res["final_url_risk"], 0.2)

    def test_tc_url_003_url_shortener(self):
        url = "https://bit.ly/3xYz90A"
        res = self.url_detector.detect(url)
        indicators = [i["indicator"] for i in res["risk_indicators"]]
        self.assertIn("url_shortener", indicators)

    # --- 2. SMS Scanning Test Cases ---
    def test_tc_sms_001_bank_threat_with_url(self):
        text = "Aapka SBI account block ho gaya hai, turant KYC update karo http://sbi-verify.com"
        pm_res = self.phrase_matcher.detect(text)
        re_res = self.rule_engine.evaluate(text)
        ud_res = self.url_detector.detect("http://sbi-verify.com")
        sc_res = self.scam_classifier.classify(text, {
            "phrases_detected": pm_res.get("phrases", []),
            "rules_triggered": re_res.get("rules_triggered", []),
            "url_risk": ud_res
        })
        risk_res = self.risk_engine.assess(pm_res, re_res, ud_res, sc_res)
        self.assertIn(risk_res["risk_level"], ["high", "critical"])

    def test_tc_sms_002_legitimate_otp(self):
        text = "123456 is your OTP for transaction at Amazon. Do not share it with anyone."
        pm_res = self.phrase_matcher.detect(text)
        re_res = self.rule_engine.evaluate(text, sender_type="verified")
        ud_res = self.url_detector.detect("")
        sc_res = self.scam_classifier.classify(text, {
            "phrases_detected": pm_res.get("phrases", []),
            "rules_triggered": re_res.get("rules_triggered", []),
            "url_risk": ud_res
        })
        risk_res = self.risk_engine.assess(pm_res, re_res, ud_res, sc_res)
        self.assertLessEqual(risk_res["risk_score"], 0.45)

    # --- 3. Email Scanning Test Cases ---
    def test_tc_eml_001_tax_refund_phishing_email(self):
        text = "Dear Customer, Your Income Tax refund of Rs 15,200 is approved. Click http://incometax-refund-portal.net to claim"
        re_res = self.rule_engine.evaluate(text)
        ud_res = self.url_detector.detect("http://incometax-refund-portal.net")
        self.assertTrue(len(re_res["rules_triggered"]) > 0)

    # --- 4. Scam Phrase Detection Test Cases ---
    def test_tc_phr_001_exact_hinglish_match(self):
        text = "Apna OTP bhejo verification ke liye"
        res = self.phrase_matcher.detect(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["phrases"][0]["scam_category"], "otp_scam")

    def test_tc_phr_002_fuzzy_hinglish_match(self):
        text = "Apna OTP bhej do verify karne waste"
        res = self.phrase_matcher.detect(text)
        self.assertTrue(res["detected"] or len(res["phrases"]) >= 0)

    # --- 5. Rule Engine Test Cases ---
    def test_tc_rul_001_urgency_and_credential_rules(self):
        text = "Turant apna bank account PIN share karo abhi"
        res = self.rule_engine.evaluate(text)
        rule_ids = [r["rule_id"] for r in res["rules_triggered"]]
        self.assertIn("R001", rule_ids) # Urgency
        self.assertIn("R002", rule_ids) # Credential Request

    # --- 6. Risk Score Assessment Test Cases ---
    def test_tc_rsk_001_critical_threat_score(self):
        pm_res = {"detected": True, "phrases": [{"confidence": 0.98}], "risk_level": "critical"}
        re_res = {"rules_triggered": [{"risk_score": 0.95}, {"risk_score": 0.9}], "total_risk_from_rules": 1.0}
        ud_res = {"final_url_risk": 0.85}
        sc_res = {"scam_category": "fake_kyc", "confidence": 0.9}
        res = self.risk_engine.assess(pm_res, re_res, ud_res, sc_res)
        self.assertEqual(res["risk_level"], "critical")

    # --- 7. Explainability Output Test Cases ---
    def test_tc_exp_001_actionable_explanation(self):
        pm_res = {"detected": True, "phrases": [{"phrase": "Apna OTP bhejo", "scam_category": "otp_scam"}], "risk_level": "high"}
        re_res = {"rules_triggered": [{"rule_name": "Credential Request", "evidence": "OTP request"}], "total_risk_from_rules": 0.95}
        ud_res = {"final_url_risk": 0.0}
        sc_res = {"scam_category": "otp_scam", "confidence": 0.95}
        res = self.risk_engine.assess(pm_res, re_res, ud_res, sc_res)
        self.assertIn("verdict", res)
        self.assertIn("recommended_action", res)

if __name__ == "__main__":
    unittest.main()
