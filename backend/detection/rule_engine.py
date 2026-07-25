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
from typing import List, Dict, Optional


# Rule definitions with risk scores
RULES = {
    "R001": {"name": "Urgency Language", "risk_score": 0.7, "description": "Detects urgent language patterns"},
    "R002": {"name": "Credential Request", "risk_score": 0.95, "description": "Detects requests for credentials/OTP/PIN"},
    "R003": {"name": "Payment Request", "risk_score": 0.9, "description": "Detects requests for money transfer"},
    "R004": {"name": "Brand Impersonation", "risk_score": 0.85, "description": "Detects brand/company name usage in suspicious context"},
    "R005": {"name": "Account Threat", "risk_score": 0.8, "description": "Detects threats about account suspension/closure"},
    "R006": {"name": "Reward/Prize Offer", "risk_score": 0.75, "description": "Detects prize/reward/gift offers"},
    "R007": {"name": "Too Good To Be True", "risk_score": 0.7, "description": "Detects unrealistic promises"},
    "R008": {"name": "Unknown Sender", "risk_score": 0.6, "description": "Detects unknown/suspicious sender patterns"},
    "R009": {"name": "Generic Greeting", "risk_score": 0.4, "description": "Detects generic greetings like Dear Customer"},
    "R010": {"name": "Poor Grammar/Spelling", "risk_score": 0.5, "description": "Detects grammar/spelling errors"},
    "R011": {"name": "Redirect Links", "risk_score": 0.75, "description": "Detects suspicious redirect URLs"},
    "R012": {"name": "Time Pressure", "risk_score": 0.65, "description": "Detects time-limited pressure tactics"},
    "R013": {"name": "Authority Impersonation", "risk_score": 0.85, "description": "Detects government/bank authority impersonation"},
    "R014": {"name": "Mobile-Only Instruction", "risk_score": 0.7, "description": "Detects instructions to use only mobile"},
    "R015": {"name": "Document Request", "risk_score": 0.8, "description": "Detects requests for personal documents"},
}


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
        triggered_rules: List[dict] = []

        checks = [
            self._check_urgency(text),
            self._check_credential_request(text),
            self._check_payment_request(text),
            self._check_brand_impersonation(text, sender_type),
            self._check_account_threat(text),
            self._check_reward_prize(text),
            self._check_too_good(text),
            self._check_unknown_sender(sender_type),
            self._check_generic_greeting(text),
            self._check_grammar(text),
            self._check_redirect_links(text, url, has_link),
            self._check_time_pressure(text),
            self._check_authority_impersonation(text),
            self._check_mobile_only(text),
            self._check_document_request(text),
        ]

        for result in checks:
            if result is not None:
                triggered_rules.append(result)

        total_risk = self._calculate_total_risk(triggered_rules)
        explanation = self._generate_explanation(triggered_rules)

        return {
            "categories_triggered": list(categories_triggered),
            "findings": findings,
            "rule_risk_score": min(total_risk_score, 100),
            "triggered_count": len(findings)
        }

    def _check_urgency(self, text: str) -> Optional[dict]:
        """R001: Check for urgency language patterns."""
        urgency_patterns = [
            r'\burgent\b', r'\bimmediately\b', r'\bright now\b', r'\basap\b', r'\bhurry\b',
            r'\bjaldi\b', r'\bturant\b', r'\babhi\b', r'\bnow or never\b', r'\blast chance\b',
            r'\bexpir\w*\b', r'\b24\s*hours?\b', r'\b24\s*ghante\b', r'\bkal\s*tak\b',
            r'\baaj\b', r'\bact\s*now\b', r'\bdont\s*delay\b', r'\bdelay\s*will\b',
            r'\btime\s*sensitive\b', r'\bimmediate\s*action\b', r'\bfail\s*to\b.*\bresult',
            r'\bonly\s*today\b', r'\blast\s*warning\b', r'\bfinal\s*notice\b',
        ]
        text_lower = text.lower()
        matches = [p for p in urgency_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R001",
                "rule_name": RULES["R001"]["name"],
                "risk_score": RULES["R001"]["risk_score"],
                "evidence": f"Urgency patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_credential_request(self, text: str) -> Optional[dict]:
        """R002: Check for credential/OTP/PIN requests."""
        credential_patterns = [
            r'\bshare\s*(?:your\s*)?otp\b', r'\botp\s*(?:share|bhej|send|enter|provide)\b',
            r'\bupi\s*pin\b', r'\bpin\s*(?:share|bhej|send|enter|tell)\b',
            r'\bpassword\b', r'\bpasscode\b', r'\bcvv\b', r'\bcvv\s*number\b',
            r'\bcard\s*(?:number|details|no)\b', r'\bdebit\s*card\b', r'\bcredit\s*card\b',
            r'\baadhaar\s*(?:number|share|bhej)\b', r'\bpan\s*(?:number|share|card)\b',
            r'\bbank\s*(?:account|details|number)\b', r'\baccount\s*(?:number|details)\b',
            r'\bsign\s*in\s*(?:credentials|details)\b', r'\blogin\s*(?:details|credentials)\b',
            r'\buser\s*name\b.*\bpass', r'\bid\b.*\bpass\b',
            r'\bapna\s*(?:otp|pin|password|number)\b', r'\bkindly\s*share\b',
            r'\bplease\s*send\b.*\b(?:otp|pin|password|number|detail)',
            r'\bverification\s*(?:code|number|otp)\b',
        ]
        text_lower = text.lower()
        if re.search(r'\b(?:do\s*not|dont|don\'t|never)\s*(?:share|tell|disclose|give)\b', text_lower):
            return None
        matches = [p for p in credential_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R002",
                "rule_name": RULES["R002"]["name"],
                "risk_score": RULES["R002"]["risk_score"],
                "evidence": f"Credential request patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_payment_request(self, text: str) -> Optional[dict]:
        """R003: Check for money transfer requests."""
        payment_patterns = [
            r'\bpaisa\s*(?:bhej|send|transfer)\b', r'\bmoney\s*(?:transfer|send|bhej)\b',
            r'\bpay\s*now\b', r'\bupi\s*(?:request|pay|bhej)\b', r'\bqr\s*code\b',
            r'\bscan\s*(?:this|karo|the)\s*(?:qr|code)\b', r'\btransfer\s*(?:kar|do|now)\b',
            r'\bRs\.?\s*\d+', r'\b₹\s*\d+', r'\bamount\s*(?:bhej|send|pay|transfer)\b',
            r'\bpayment\s*(?:karein|bhej|send|make|complete)\b', r'\bbhej\s*(?:do|de|na)\b',
            r'\bsend\s*(?:money|payment|rs|inr)\b', r'\bdeposit\s*(?:kar|do|now)\b',
            r'\bwire\s*transfer\b', r'\bbank\s*transfer\b', r'\bneft\b', r'\bimps\b', r'\brtgs\b',
            r'\bupi\s*id\b', r'\bpay\s*(?:tm|phonepe|gpay|google\s*pay)\b',
        ]
        text_lower = text.lower()
        matches = [p for p in payment_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R003",
                "rule_name": RULES["R003"]["name"],
                "risk_score": RULES["R003"]["risk_score"],
                "evidence": f"Payment request patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_brand_impersonation(self, text: str, sender_type: str = "unknown") -> Optional[dict]:
        """R004: Check for brand name usage in suspicious context."""
        if sender_type == "verified":
            return None
        brand_patterns = [
            r'\b(?:hdfc|icici|sbi|axis|kotak|pnb|bob|canara|union\s*bank)\b',
            r'\b(?:paytm|phonepe|google\s*pay|gpay|amazon\s*pay|mobikwik)\b',
            r'\b(?:amazon|flipkart|meesho|snapdeal|ajio|myntra)\b',
            r'\b(?:whatsapp|instagram|facebook|telegram|truecaller)\b',
            r'\b(?:irctc|digilocker|uidai|npci)\b',
            r'\b(?:rbi|sebi|trai)\b',
            r'\bamazon\s*(?:prime|pay|order|delivery)\b',
            r'\bflipkart\s*(?:pay|order|delivery|plus)\b',
            r'\bpaytm\s*(?:wallet|upi|cashback|account)\b',
        ]
        text_lower = text.lower()
        matches = [p for p in brand_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R004",
                "rule_name": RULES["R004"]["name"],
                "risk_score": RULES["R004"]["risk_score"],
                "evidence": f"Brand references detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_account_threat(self, text: str) -> Optional[dict]:
        """R005: Check for account suspension/closure threats."""
        threat_patterns = [
            r'\baccount\s*(?:band|suspend|block|freeze|close|deactivate|disable)\b',
            r'\bsuspend(?:ed|ing)?\b.*\baccount\b', r'\bblock(?:ed)?\b.*\baccount\b',
            r'\bfreez(?:e|ing)\b.*\baccount\b', r'\bclos(?:e|ed|ing)\b.*\baccount\b',
            r'\baccount\s*(?:ko\s*)?(?:band|suspend|block|freeze|close)\b',
            r'\byour\s*account\s*will\s*be\b', r'\baccount\s*is\s*(?:not|no)\s*(?:verified|active|valid)\b',
            r'\bfail(?:ure)?\s*to\s*(?:verify|update|confirm)\b.*\baccount\b',
            r'\baccount\s*(?:terminated|revoked|locked)\b',
            r'\bdeactivat\w*\b.*\baccount\b', r'\bdisabl\w*\b.*\baccount\b',
        ]
        text_lower = text.lower()
        matches = [p for p in threat_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R005",
                "rule_name": RULES["R005"]["name"],
                "risk_score": RULES["R005"]["risk_score"],
                "evidence": f"Account threat patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_reward_prize(self, text: str) -> Optional[dict]:
        """R006: Check for prize/reward offers."""
        reward_patterns = [
            r'\bprize\b', r'\bwinner\b', r'\bgift\b', r'\bcashback\b', r'\blottery\b',
            r'\bcongratulations\b.*\bwon\b', r'\byou\s*have\s*won\b', r'\byou\s*are\s*(?:the\s*)?winner\b',
            r'\bfree\s*(?:gift|voucher|coupon|reward)\b', r'\bclaim\s*(?:your|now)\b',
            r'\breward\b.*\bclaim\b', r'\bjackpot\b', r'\bgrand\s*prize\b',
            r'\bspin\s*(?:the|a)\s*wheel\b', r'\blucky\s*(?:winner|draw|day)\b',
            r'\bselected\s*(?:winner|user|customer)\b', r'\bsurprise\s*(?:gift|reward|offer)\b',
            r'\bcash\s*prize\b', r'\bfree\s*money\b', r'\bbonus\s*(?:cash|reward|amount)\b',
        ]
        text_lower = text.lower()
        matches = [p for p in reward_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R006",
                "rule_name": RULES["R006"]["name"],
                "risk_score": RULES["R006"]["risk_score"],
                "evidence": f"Reward/prize patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_too_good(self, text: str) -> Optional[dict]:
        """R007: Check for unrealistic promises."""
        tgbt_patterns = [
            r'\b100\s*%\s*(?:profit|return|guaranteed|success)\b',
            r'\bdouble\s*(?:your\s*)?money\b', r'\btriple\s*(?:your\s*)?money\b',
            r'\bguaranteed\s*(?:returns?|profit|income|earn)\b',
            r'\bno\s*risk\b', r'\brisk\s*free\b', r'\bzero\s*risk\b',
            r'\b\d+x\s*(?:return|profit|money)\b', r'\b\d+%\s*(?:return|profit|interest)\b',
            r'\bget\s*(?:rich|wealthy)\b', r'\bfinancial\s*freedom\b.*\binstant',
            r'\binstant\s*(?:profit|return|earning|income)\b',
            r'\beasy\s*money\b', r'\bfree\s*money\b', r'\bmake\s*money\s*(?:fast|quick|easy)\b',
            r'\bpassive\s*income\b.*\b\d+%\b', r'\bdaily\s*earning\b',
            r'\b1\s*crore\b', r'\blakhs?\s*(?:per|in|every)\b.*\bmonth\b',
        ]
        text_lower = text.lower()
        matches = [p for p in tgbt_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R007",
                "rule_name": RULES["R007"]["name"],
                "risk_score": RULES["R007"]["risk_score"],
                "evidence": f"Unrealistic promise patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_unknown_sender(self, sender_type: str) -> Optional[dict]:
        """R008: Check for unknown sender."""
        if sender_type.lower() in ("unknown", "untrusted", "external"):
            return {
                "rule_id": "R008",
                "rule_name": RULES["R008"]["name"],
                "risk_score": RULES["R008"]["risk_score"],
                "evidence": f"Sender type is '{sender_type}'",
            }
        return None

    def _check_generic_greeting(self, text: str) -> Optional[dict]:
        """R009: Check for generic greetings."""
        greeting_patterns = [
            r'\bdear\s*(?:customer|user|member|sir|madam|valued|trusted|esteemed)\b',
            r'\bdear\s*(?:account\s*holder|subscriber|client)\b',
            r'\bhi\s*(?:there|dear|friend|user|customer)\b',
            r'\bhello\s*(?:there|dear|friend|user|customer)\b',
            r'\bvalued\s*(?:customer|user|member|client)\b',
            r'\btrusted\s*(?:customer|user|member|client)\b',
            r'\besteemed\s*(?:customer|user|member|client)\b',
            r'\brespected\s*(?:customer|user|member|client)\b',
            r'\bdear\s*(?:sir|madam)\b',
            r'\bto\s*whom\s*it\s*may\s*concern\b',
        ]
        text_lower = text.lower()
        matches = [p for p in greeting_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R009",
                "rule_name": RULES["R009"]["name"],
                "risk_score": RULES["R009"]["risk_score"],
                "evidence": f"Generic greeting patterns detected: {', '.join(matches[:2])}",
            }
        return None

    def _check_grammar(self, text: str) -> Optional[dict]:
        """R010: Check for poor grammar/spelling."""
        grammar_issues = []
        text_lower = text.lower()

        spelling_errors = [
            (r'\bdear\s*custmer\b', 'custmer'),
            (r'\bdear\s*costumer\b', 'costumer'),
            (r'\bacount\b', 'acount'),
            (r'\bacconut\b', 'acconut'),
            (r'\bsuspened\b', 'suspened'),
            (r'\bverfication\b', 'verfication'),
            (r'\bimediately\b', 'imediately'),
            (r'\btransation\b', 'transation'),
            (r'\brecieve\b', 'recieve'),
            (r'\boccured\b', 'occured'),
            (r'\bneccessary\b', 'neccessary'),
            (r'\bsucessful\b', 'sucessful'),
            (r'\bavailabe\b', 'availabe'),
            (r'\bexperied\b', 'experied'),
            (r'\bconfrim\b', 'confrim'),
            (r'\bwithdral\b', 'withdral'),
            (r'\bbalace\b', 'balace'),
            (r'\btrafer\b', 'trafer'),
            (r'\bproccess\b', 'proccess'),
            (r'\bregistred\b', 'registred'),
        ]

        for pattern, word in spelling_errors:
            if re.search(pattern, text_lower):
                grammar_issues.append(f"misspelling: '{word}'")

        repeated_words = re.findall(r'\b(\w+)\s+\1\b', text_lower)
        if repeated_words:
            grammar_issues.append(f"repeated word: '{repeated_words[0]}'")

        multiple_punct = re.findall(r'[!?]{3,}', text)
        if multiple_punct:
            grammar_issues.append("excessive punctuation")

        if len(grammar_issues) >= 2:
            return {
                "rule_id": "R010",
                "rule_name": RULES["R010"]["name"],
                "risk_score": RULES["R010"]["risk_score"],
                "evidence": f"Grammar/spelling issues detected: {'; '.join(grammar_issues[:3])}",
            }
        return None

    def _check_redirect_links(self, text: str, url: str, has_link: bool) -> Optional[dict]:
        """R011: Check for suspicious redirect URLs."""
        redirect_patterns = [
            r'bit\.ly/', r'tinyurl\.com/', r't\.co/', r'goo\.gl/',
            r'ow\.ly/', r'is\.gd/', r'buff\.ly/', r'dub\.sh/',
            r'cutt\.ly/', r'rb\.gy/', r'tiny\.cc/',
            r'bl\.ink/', r'shr\.ink/', r'shorturl\.at/',
        ]
        url_shortener_hits = [p for p in redirect_patterns if p in text.lower() or p in url.lower()]

        redirect_kw = [
            r'\bredirect\b', r'\bclick\s*here\b', r'\bredirecting\s*you\b',
            r'\blogin\s*page\b.*\blink', r'\bverify\s*(?:here|now|account)\b.*\blink',
            r'\bhttp[s]?://[^\s]*\b.*\bhttp[s]?://[^\s]*\b',
        ]
        text_lower = text.lower()
        redirect_kw_hits = [p for p in redirect_kw if re.search(p, text_lower)]

        has_multiple_urls = len(re.findall(r'https?://\S+', text)) > 1

        if url_shortener_hits or redirect_kw_hits or (has_link and has_multiple_urls):
            evidence_parts = []
            if url_shortener_hits:
                evidence_parts.append(f"URL shortener detected: {url_shortener_hits[0]}")
            if redirect_kw_hits:
                evidence_parts.append("redirect language detected")
            if has_link and has_multiple_urls:
                evidence_parts.append("multiple URLs present")
            return {
                "rule_id": "R011",
                "rule_name": RULES["R011"]["name"],
                "risk_score": RULES["R011"]["risk_score"],
                "evidence": "; ".join(evidence_parts),
            }
        return None

    def _check_time_pressure(self, text: str) -> Optional[dict]:
        """R012: Check for time pressure tactics."""
        time_pressure_patterns = [
            r'\bwithin\s*(?:24|48|72)\s*hours?\b', r'\bbefore\s*(?:\d{1,2}[/-]\d{1,2})\b',
            r'\blimited\s*time\b', r'\bact\s*before\b', r'\bexpire\w*\s*(?:today|soon|midnight)\b',
            r'\bonly\s*(?:\d+|few)\s*(?:hours?|minutes?|days?)\s*(?:left|remaining)\b',
            r'\bdeadline\b.*\b(?:today|tomorrow|soon|midnight)\b',
            r'\bby\s*(?:today|tomorrow|midnight|tonight)\b',
            r'\bkal\s*(?:tak|before|tak)\b', r'\baaj\s*(?:raat|sham|before)\b',
            r'\bfail\s*to\s*(?:respond|reply|act|verify)\b.*\b(?:within|before|by)\b',
            r'\bimmediate\s*response\s*required\b', r'\brespond\s*(?:now|immediately|within)\b',
            r'\bonly\s*today\b', r'\btonight\s*only\b', r'\bmidnight\s*deadline\b',
            r'\bhours?\s*(?:left|remaining|only)\b',
        ]
        text_lower = text.lower()
        matches = [p for p in time_pressure_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R012",
                "rule_name": RULES["R012"]["name"],
                "risk_score": RULES["R012"]["risk_score"],
                "evidence": f"Time pressure patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_authority_impersonation(self, text: str) -> Optional[dict]:
        """R013: Check for authority impersonation."""
        authority_patterns = [
            r'\brbi\b', r'\breserve\s*bank\b', r'\bpolice\b', r'\bcbi\b',
            r'\bministry\b', r'\bcustoms\b', r'\bincome\s*tax\b',
            r'\bgovernment\b', r'\bgovt\.?\b', r'\bofficial\s*(?:notice|letter|circular)\b',
            r'\bsebi\b', r'\btrai\b', r'\bdept\.?\s*of\b',
            r'\bcyber\s*(?:crime|cell|police)\b', r'\bcrime\s*(?:branch|investigation)\b',
            r'\bfir\b', r'\bfirst\s*information\s*report\b',
            r'\blegal\s*(?:notice|action|department)\b', r'\bcourt\s*(?:notice|order)\b',
            r'\bnational\s*investigation\b', r'\benforcement\s*directorate\b',
            r'\bed\b', r'\bfema\b', r'\banti\s*corruption\b',
            r'\bbanking\s*(?:fraud|regulatory)\b', r'\bfinancial\s*(?:fraud|intelligence)\b',
            r'\bfiu\b', r'\bfinancial\s*intelligence\s*unit\b',
        ]
        text_lower = text.lower()
        matches = [p for p in authority_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R013",
                "rule_name": RULES["R013"]["name"],
                "risk_score": RULES["R013"]["risk_score"],
                "evidence": f"Authority impersonation patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_mobile_only(self, text: str) -> Optional[dict]:
        """R014: Check for mobile-only instructions."""
        mobile_patterns = [
            r'\bphone\s*pe\b', r'\bmobile\s*se\b', r'\bapp\s*download\b',
            r'\bplay\s*store\b', r'\bapp\s*store\b', r'\bapp\s*install\b',
            r'\bmobile\s*(?:par|per|mein|pe)\b', r'\bonly\s*on\s*mobile\b',
            r'\bsirf\s*mobile\s*(?:par|pe|se)\b', r'\bphone\s*(?:par|per|mein)\b',
            r'\binstall\s*(?:our|the|this)\s*app\b', r'\bdownload\s*(?:our|the|this)\s*app\b',
            r'\buse\s*(?:mobile|phone)\s*only\b', r'\bmobile\s*(?:app|application)\b',
            r'\bsmartphone\s*required\b', r'\bandroid\b.*\bios\b',
            r'\bwhatsapp\s*(?:only|par|pe)\b',
        ]
        text_lower = text.lower()
        matches = [p for p in mobile_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R014",
                "rule_name": RULES["R014"]["name"],
                "risk_score": RULES["R014"]["risk_score"],
                "evidence": f"Mobile-only instruction patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _check_document_request(self, text: str) -> Optional[dict]:
        """R015: Check for personal document requests."""
        document_patterns = [
            r'\baadhaar\b.*\b(?:share|send|upload|bhej|photo|copy|number)\b',
            r'\bpan\s*(?:card|number)\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bpassport\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bdriving\s*licence\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bvoter\s*id\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bsalary\s*slip\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bbank\s*statement\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bincome\s*proof\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\baddress\s*proof\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\bid\s*proof\b.*\b(?:share|send|upload|bhej|photo|copy)\b',
            r'\b(?:share|send|upload|bhej|photo|copy)\b.*\b(?:aadhaar|pan\s*card|passport|driving\s*licence|voter\s*id|salary\s*slip|bank\s*statement)\b',
            r'\bdocuments?\s*(?:bhej|send|share|upload|submit)\b',
            r'\bphoto\s*of\b.*\b(?:aadhaar|pan|passport|licence|id)\b',
            r'\bscan(?:ned)?\s*(?:copy|photo)\b.*\b(?:aadhaar|pan|passport|licence|id)\b',
        ]
        text_lower = text.lower()
        matches = [p for p in document_patterns if re.search(p, text_lower)]
        if matches:
            return {
                "rule_id": "R015",
                "rule_name": RULES["R015"]["name"],
                "risk_score": RULES["R015"]["risk_score"],
                "evidence": f"Document request patterns detected: {', '.join(matches[:3])}",
            }
        return None

    def _calculate_total_risk(self, triggered_rules: List[dict]) -> float:
        """Calculate total risk score from triggered rules using max + diminishing returns."""
        if not triggered_rules:
            return 0.0

        scores = sorted([r["risk_score"] for r in triggered_rules], reverse=True)
        max_score = scores[0]

        cumulative = max_score
        for score in scores[1:]:
            cumulative += score * 0.15

        return round(min(cumulative, 1.0), 4)

    def _generate_explanation(self, triggered_rules: List[dict]) -> str:
        """Generate explanation of triggered rules."""
        if not triggered_rules:
            return "No scam indicators detected."

        sorted_rules = sorted(triggered_rules, key=lambda r: r["risk_score"], reverse=True)
        top_rules = sorted_rules[:5]

        lines = [f"Detected {len(triggered_rules)} scam indicator(s):"]
        for rule in top_rules:
            lines.append(f"- {rule['rule_name']} (risk: {rule['risk_score']:.0%}): {rule['evidence']}")

        if len(triggered_rules) > 5:
            lines.append(f"- ...and {len(triggered_rules) - 5} more indicators")

rule_engine = RuleEngine()
