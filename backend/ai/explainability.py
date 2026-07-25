"""
TrustLens AI - Explainability Engine
Generates clear, human-understandable explanations for detected threats and assigns context-aware recommendations.
"""

from typing import List, Dict, Any


class ExplainabilityEngine:
    @staticmethod
    def generate_explanation(
        risk_score: int,
        verdict: str,
        scam_category: str,
        reasons: List[str],
        matched_phrases: List[str],
        detected_urls: List[str],
        ai_explanation: str = None
    ) -> str:
        """
        Synthesizes AI and rule findings into a clear human-readable narrative.
        """
        if ai_explanation and len(ai_explanation.strip()) > 10:
            return ai_explanation.strip()

        if verdict == "Safe":
            return (
                "Our multi-layer analysis found no known phishing links, scam phrases, "
                "or deceptive patterns in this submission. The content appears safe."
            )

        explanation = f"This content has been flagged as **{verdict}** (Risk Score: {risk_score}/100) under category **{scam_category}**."

        if matched_phrases:
            explanation += f" High-risk Hinglish scam phrases were detected ({', '.join(matched_phrases[:3])})."

        if detected_urls:
            explanation += f" Suspicious domain or link structure found in ({', '.join(detected_urls[:2])})."

        if reasons:
            explanation += f" Key indicators: {'; '.join(reasons[:3])}."

        return explanation

    @staticmethod
    def generate_recommendations(
        verdict: str,
        scam_category: str,
        has_url: bool = False,
        has_otp_request: bool = False,
        has_financial_request: bool = False
    ) -> List[str]:
        """
        Generates actionable recommendations based on threat verdict and risk triggers.
        """
        actions = []

        if verdict in ["High Risk", "Critical"]:
            actions.append("⛔ DO NOT click on any links or download any files attached to this message.")
            actions.append("🔒 NEVER share your OTP, UPI PIN, ATM PIN, or passwords with anyone.")
            actions.append("🚫 Block the sender immediately on WhatsApp/SMS/Email.")
            actions.append("📢 Report this scam on the National Cyber Crime Reporting Portal (cybercrime.gov.in) or call 1930.")

        elif verdict == "Medium Risk":
            actions.append("⚠️ Verify the sender's identity through official website or customer support line.")
            actions.append("🔍 Do not enter personal details or bank credentials on unknown websites.")
            actions.append("📱 Avoid dialing phone numbers provided directly inside suspicious messages.")

        elif verdict == "Low Risk":
            actions.append("ℹ️ Proceed with caution. Cross-check domain names for minor spelling variations.")
            actions.append("🛡️ Enable 2-Factor Authentication (2FA) on all financial and social accounts.")

        else:
            actions.append("✅ Content appears legitimate, but always stay vigilant against unverified requests.")
            actions.append("💡 Remember: Banks, RBI, and Police NEVER ask for OTPs or PINs via call or message.")

        if has_url:
            actions.append("🔗 Inspect domain name carefully (e.g. check for '.top', '.online', or misspelled brand names).")

        if has_otp_request or has_financial_request:
            actions.append("🚨 Emergency Action: If money was already sent, immediately contact your bank to block the transaction & dial 1930.")

        return actions


explainability_engine = ExplainabilityEngine()
