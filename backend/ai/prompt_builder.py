"""
TrustLens AI - Prompt Builder Module
Constructs system and user prompts for NVIDIA NIM AI analysis tailored to Indian cybersecurity threats.
"""

from typing import Dict, Any, List


class PromptBuilder:
    @staticmethod
    def build_system_prompt() -> str:
        return """You are TrustLens AI, a World-Class Cybersecurity Analyst and Fraud Detection Expert specialized in Indian scams (Hinglish/Hindi/English).
Your goal is to analyze suspicious text, messages, URLs, or OCR extracted content and provide an objective JSON assessment.

Scam Categories to detect:
1. OTP Scam (Requesting OTP, PIN, password, CVV)
2. KYC Scam (Bank, SIM, Aadhaar, PAN KYC update urgency)
3. Bank Impersonation (Fake SBI, HDFC, ICICI, Axis alerts)
4. Delivery Scam (India Post, Courier, Parcel stuck fee)
5. Lottery & Prize Scam (KBC, WhatsApp lottery, Rewards)
6. UPI Fraud (Scan QR to receive money, Send Rs 1 to win)
7. Investment & Crypto Scam (Guaranteed high return, Work from Home crypto)
8. Job & Work From Home Scam (Task complete pay money, Telegram job)
9. Fake Loan Scam (Instant loan approval with processing fee)
10. Government & Law Enforcement Scam (Digital arrest, CBI, Customs, Electricity bill disconnect)
11. Phishing URL / Fake Site (Suspicious links, typosquatted brand URLs)
12. Safe Content (Legitimate message or URL)

Output JSON Format ONLY:
{
    "verdict": "Safe" | "Low Risk" | "Medium Risk" | "High Risk" | "Critical",
    "risk_score": <number 0 to 100>,
    "scam_category": "<category name>",
    "explanation": "<2-3 sentence clear human-friendly explanation>",
    "key_reasons": ["<reason 1>", "<reason 2>", "<reason 3>"],
    "recommended_actions": ["<action 1>", "<action 2>", "<action 3>"]
}
"""

    @staticmethod
    def build_analysis_prompt(
        text: str,
        detected_urls: List[str] = None,
        matched_phrases: List[str] = None,
        rule_findings: List[Dict[str, Any]] = None
    ) -> str:
        detected_urls = detected_urls or []
        matched_phrases = matched_phrases or []
        rule_findings = rule_findings or []

        prompt = f"Analyze the following suspicious content for fraud or scam risk:\n\n"
        prompt += f"--- SUSPICIOUS CONTENT ---\n{text}\n-------------------------\n\n"

        if detected_urls:
            prompt += f"Detected URLs: {', '.join(detected_urls)}\n"
        if matched_phrases:
            prompt += f"Matched Hinglish/Scam Phrases: {', '.join(matched_phrases)}\n"
        if rule_findings:
            prompt += "Rule Engine Triggers:\n"
            for find in rule_findings:
                prompt += f" - [{find.get('layer')}] {find.get('finding')}\n"

        prompt += "\nProvide the JSON evaluation now."
        return prompt


prompt_builder = PromptBuilder()
