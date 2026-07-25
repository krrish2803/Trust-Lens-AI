# Bug Reports & Technical Remediation Log

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Quality Assurance Lead  
**Date:** July 25, 2026  
**Document Status:** All Identified Issues Resolved & Verified  

---

## Bug Report #1: False Positive Phishing Flag on Whitelisted Official Bank Subdomains

### Issue Title
`URLDetector` Flags Whitelisted Official Subdomains as Domain Squatting

### Severity
High

### Steps to Reproduce
1. Instantiate `URLDetector` in Python.
2. Call `url_detector.detect("https://www.sbi.co.in")`.
3. Inspect `final_url_risk` score and `risk_indicators`.

### Expected Result
Official domain `sbi.co.in` should be recognized as a whitelisted bank domain, returning `final_url_risk = 0.0` and zero risk indicators.

### Actual Result
`final_url_risk` returned `0.94` with indicator `domain_squatting` because `domain.split('.')[0]` returned `"www"`, which triggered `alias_lower != domain_name` check (`"sbi" != "www"`).

### Suggested Fix
Add an explicit whitelist check at the beginning of `URLDetector.detect()` to immediately return `final_url_risk = 0.0` if the domain or parent domain exists in `trusted_domains.json`.

```python
is_trusted = domain in self.trusted_domains or any(domain == td or domain.endswith('.' + td) for td in self.trusted_domains)
if is_trusted:
    return {
        "url": url,
        "risk_indicators": [],
        "final_url_risk": 0.0,
        "verdict": "SAFE: Officially verified legitimate domain.",
        "recommendation": "SAFE to proceed. Official verified domain."
    }
```
*Status: **FIXED & VERIFIED***

---

## Bug Report #2: Non-Zero Risk Assigned to Empty URL Strings

### Issue Title
`URLDetector` Assigns Risk Score of 0.45 to Empty URL String Inputs

### Severity
Medium

### Steps to Reproduce
1. Call `url_detector.detect("")` or pass empty string payload during text-only message analysis.
2. Inspect `risk_indicators` and `final_url_risk`.

### Expected Result
Empty URL string should return `final_url_risk = 0.0` and zero risk indicators.

### Actual Result
`_check_https("")` evaluated empty string as non-HTTPS URL, returning `risk_score = 0.45`.

### Suggested Fix
Add early return check at start of `URLDetector.detect()` for empty strings:

```python
if not url or not url.strip():
    return {
        "url": "",
        "risk_indicators": [],
        "final_url_risk": 0.0,
        "verdict": "SAFE: No URL provided.",
        "recommendation": "SAFE"
    }
```
*Status: **FIXED & VERIFIED***

---

## Bug Report #3: False Positive Credential Theft Flag on Official Advisory Messages

### Issue Title
`RuleEngine` Flags Legitimate Messages Containing "Do Not Share" Warnings as Credential Requests

### Severity
High

### Steps to Reproduce
1. Call `RuleEngine.evaluate("123456 is your OTP. Do not share it with anyone.")`.
2. Inspect triggered rules.

### Expected Result
Legitimate transactional SMS with explicit warning *"do not share"* should NOT trigger `R002 Credential Request`.

### Actual Result
Rule `R002 Credential Request` triggered with risk score `0.95` due to keyword co-occurrence of `"share"` and `"OTP"`.

### Suggested Fix
Add negative advisory regex check in `RuleEngine._check_credential_request`:

```python
if re.search(r'\b(?:do\s*not|dont|don\'t|never)\s*(?:share|tell|disclose|give)\b', text_lower):
    return None
```
*Status: **FIXED & VERIFIED***

---

## Bug Report #4: Brand Impersonation Flag on Verified Sender Messages

### Issue Title
`RuleEngine` Flags Legitimate Brand Mentions from Verified Senders as Impersonation

### Severity
Medium

### Steps to Reproduce
1. Call `RuleEngine.evaluate("Your Amazon order has been dispatched", sender_type="verified")`.
2. Inspect triggered rules.

### Expected Result
Brand names in messages sent by verified sender headers (`sender_type="verified"`) should not be flagged as brand impersonation.

### Actual Result
Rule `R004 Brand Impersonation` triggered with risk score `0.85`.

### Suggested Fix
Update `RuleEngine._check_brand_impersonation` to bypass check when `sender_type == "verified"`:

```python
def _check_brand_impersonation(self, text: str, sender_type: str = "unknown") -> Optional[dict]:
    if sender_type == "verified":
        return None
```
*Status: **FIXED & VERIFIED***

---

## Bug Report #5: Hinglish Scam Phrase Dataset Under-Count

### Issue Title
Initial `hinglish_phrases.json` Dataset Contained Only 155 Phrases (Below Requirement of 200+)

### Severity
Medium

### Steps to Reproduce
1. Count entries in `datasets/hinglish_phrases.json`.
2. Observe total phrase count.

### Expected Result
Dataset must contain at least 200 realistic, verified Hinglish scam phrases across 14 scam categories with complete metadata (`phrase`, `scam_category`, `severity`, `why_it_is_suspicious`).

### Actual Result
Original dataset contained 155 phrases and lacked consistent `severity` and `why_it_is_suspicious` fields on some older entries.

### Suggested Fix
Wrote script `scratch/expand_hinglish_dataset.py` to systematically expand dataset to **210 verified Hinglish phrases** covering all 14 required categories, ensuring all mandatory metadata keys are present.

*Status: **FIXED & VERIFIED***

---

*Bug Log certified by Quality Assurance Lead. All 5 identified issues resolved.*
