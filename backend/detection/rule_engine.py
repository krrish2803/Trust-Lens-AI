"""
TrustLens AI - Rule Engine Module
Multi-category rule engine covering 10 distinct Indian scam types:
1. OTP Scams
2. KYC Scams
3. Bank Impersonation Scams
4. Delivery & Parcel Scams
5. Lottery & Reward Scams
6. UPI Fraud Scams
7. Investment & Crypto Scams
8. Job & Work From Home Scams
9. Instant Loan Scams
10. Government & CBI/Police Arrest Scams
"""

import re
from typing import List, Dict, Any, Tuple


class RuleEngine:
    def __init__(self):
        # 1. OTP Scam Patterns
        self.otp_patterns = [
            r"\b(?:otp|one time password|cvv|pin|passcode|atm pin)\b",
            r"(?:share|tell|send|enter|verify|provide)\s+(?:your|the)?\s*(?:otp|pin|cvv)",
            r"\b(?:otp|pin)\s+(?:mat share karo|bhejo|diya|chahiye)\b",
            r"bank officer.*(?:otp|pin)",
            r"verification code.*(?:share|send)"
        ]

        # 2. KYC Scam Patterns
        self.kyc_patterns = [
            r"\b(?:kyc|know your customer|aadhaar|pan card|sim block)\b",
            r"(?:kyc|account|sim)\s+(?:update|verify|suspend|deactivate|expire|complete)",
            r"kyc\s+(?:nondone|pending|overdue|mandatory)",
            r"update\s+your\s+(?:kyc|pan|aadhaar|bank details)",
            r"document.*(?:upload|verify|submit).*(?:kyc|bank)"
        ]

        # 3. Bank Impersonation Patterns
        self.bank_patterns = [
            r"\b(?:sbi|hdfc|icici|axis|pnb|bob|kotak|canara|union bank|rbi)\b",
            r"(?:account|netbanking|debit card|credit card)\s+(?:blocked|suspended|frozen|locked)",
            r"dear\s+customer.*(?:bank|account|card)",
            r"reward\s+points.*(?:expire|redeem|cashback)",
            r"unauthorized\s+transaction.*(?:click|verify)"
        ]

        # 4. Delivery & Parcel Scam Patterns
        self.delivery_patterns = [
            r"\b(?:india post|courier|fedex|bluedart|dtdc|amazon parcel|delhivery)\b",
            r"(?:parcel|package|delivery|shipment)\s+(?:stuck|failed|delayed|held|returned)",
            r"address\s+(?:incorrect|update|invalid|missing)",
            r"pay\s+(?:rs|rupees|\u20b9)?\s*\d+\s*(?:delivery fee|customs|custom duty|redelivery)"
        ]

        # 5. Lottery & Reward Scam Patterns
        self.lottery_patterns = [
            r"\b(?:kbc|kaun banega crorepati|lucky draw|winner|lottery|spin & win)\b",
            r"(?:won|jeet gaya|jeeta|claim)\s+(?:rs|rupees|\u20b9)?\s*[\d,]+\s*(?:lakh|crore|prize|cash)",
            r"congratulations.*(?:winner|lucky|selected|reward)",
            r"whatsapp\s+(?:lottery|lucky draw)",
            r"claim\s+your\s+(?:prize|gift|reward|car|iphone)"
        ]

        # 6. UPI Fraud Patterns
        self.upi_patterns = [
            r"\b(?:upi|gpay|google pay|phonepe|paytm|bhim)\b",
            r"(?:scan|enter)\s+(?:qr code|upi pin)\s+to\s+(?:receive|get|claim)\s+(?:money|cashback)",
            r"send\s+(?:rs|rupees|\u20b9)?\s*1\s+to\s+(?:verify|claim|receive)",
            r"request\s+money.*(?:accept|enter pin)",
            r"cashback.*(?:credited|pending|claim now)"
        ]

        # 7. Investment & Crypto Scam Patterns
        self.investment_patterns = [
            r"\b(?:guaranteed return|daily income|crypto mining|double money|forex trading)\b",
            r"invest\s+(?:rs|rupees|\u20b9)?\s*\d+\s*(?:and get|earn|return)",
            r"earn\s+(?:rs|rupees|\u20b9)?\s*[\d,]+\s*(?:per day|daily|per month)",
            r"(?:100%|risk free|zero risk)\s+(?:profit|return)",
            r"telegram\s+(?:investment|trading|signals|vip group)"
        ]

        # 8. Job & Work From Home Scam Patterns
        self.job_patterns = [
            r"\b(?:work from home|part time job|youtube like job|telegram job|data entry)\b",
            r"earn\s+(?:rs|rupees|\u20b9)?\s*\d+-\d+\s*(?:daily|per day)",
            r"like\s+(?:videos|posts|youtube)\s+and\s+earn",
            r"no\s+(?:experience|qualification)\s+required",
            r"task\s+completion.*(?:pay|prepaid|commission)"
        ]

        # 9. Fake Loan Scam Patterns
        self.loan_patterns = [
            r"\b(?:instant loan|pre-approved loan|zero cibil|no document loan)\b",
            r"loan\s+of\s+(?:rs|rupees|\u20b9)?\s*[\d,]+\s*sanctioned",
            r"pay\s+(?:processing fee|file charge|insurance|noc fee)\s+first",
            r"low\s+interest\s+rate\s+loan\s+approval",
            r"instant\s+credit\s+without\s+verification"
        ]

        # 10. Government & Law Enforcement Scam Patterns
        self.govt_patterns = [
            r"\b(?:cbi|customs|cyber crime|police|mha|digital arrest|trai|electricity bill)\b",
            r"electricity\s+power\s+will\s+be\s+disconnected",
            r"illegal\s+(?:parcel|drugs|passport|sim|money laundering)",
            r"court\s+(?:notice|warrant|summons|fir|arrest)",
            r"pay\s+fine\s+(?:immediately|online|to avoid arrest)"
        ]

    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Evaluates text against all 10 rule categories.
        Returns triggered categories, matching rules, risk points, and evidence.
        """
        text_lower = text.lower()
        findings = []
        categories_triggered = set()
        total_risk_score = 0

        rule_groups = [
            ("OTP Scam", self.otp_patterns, 35, "Requests OTP, PIN, password, or security credentials."),
            ("KYC Scam", self.kyc_patterns, 30, "Pushes urgent KYC update or account suspension threat."),
            ("Bank Impersonation", self.bank_patterns, 25, "Impersonates bank alerts or account blocking."),
            ("Delivery Scam", self.delivery_patterns, 20, "Fake parcel delivery hold or address fee request."),
            ("Lottery & Prize Scam", self.lottery_patterns, 25, "Unrealistic lottery, reward, or KBC prize claim."),
            ("UPI Fraud", self.upi_patterns, 30, "Deceptive UPI PIN entry or scan QR to receive money tactic."),
            ("Investment Scam", self.investment_patterns, 25, "Guaranteed high returns or crypto trading scam."),
            ("Job Scam", self.job_patterns, 20, "Work from home task scam or pay money for tasks."),
            ("Fake Loan Scam", self.loan_patterns, 20, "Instant loan approval with advance processing fee demand."),
            ("Government & Law Enforcement Scam", self.govt_patterns, 35, "Digital arrest threat, CBI/Police impersonation, or electricity disconnect.")
        ]

        for cat_name, patterns, weight, desc in rule_groups:
            matched_evidence = []
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    matched_evidence.append(matches[0] if isinstance(matches[0], str) else matches[0][0])

            if matched_evidence:
                categories_triggered.add(cat_name)
                total_risk_score += weight
                findings.append({
                    "category": cat_name,
                    "finding": desc,
                    "weight": weight,
                    "matches": list(set(matched_evidence))
                })

        return {
            "categories_triggered": list(categories_triggered),
            "findings": findings,
            "rule_risk_score": min(total_risk_score, 100),
            "triggered_count": len(findings)
        }


rule_engine = RuleEngine()
