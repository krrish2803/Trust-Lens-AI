# TrustLens AI Hackathon Judge Q&A Preparation Matrix

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** QA & Technical Lead  
**Date:** July 25, 2026  
**Document Status:** Defense Ready  

---

## 1. Technical & Architecture Questions

### Q1: How does TrustLens AI handle novel scam phrases that are not in your 210-phrase dataset?
**Strong Answer:**  
"Great question! We do not rely solely on exact dataset matching. TrustLens AI employs a **4-layer hybrid defense architecture**:
1. **Fuzzy Sequence Matching:** Handles spelling variations and colloquial modifications with an 80% similarity threshold.
2. **15-Rule Heuristic Engine:** Detects underlying intent patterns such as urgency keywords (*turant*, *jaldi*), credential requests (*PIN*, *OTP*), authority impersonation, and time pressure—regardless of specific phrasing.
3. **Keyword Proximity Analysis:** Evaluates co-occurrence of high-risk terms (e.g., *UPI* + *Receive* + *PIN*).
4. **Scam Category Classifier:** Uses probabilistic scoring to classify unlisted messages based on structural features. This ensures high detection coverage even for newly emerging scam variations."

---

### Q2: How do you prevent false positives on legitimate bank transactional SMS or OTP alerts?
**Strong Answer:**  
"False positives destroy user trust, so we engineered two strict safeguards into our pipeline:
1. **Negative Advisory Filtering:** Our Rule Engine explicitly checks for negative safety phrases like *'Do NOT share'*, *'Never share'*, and *'Do not disclose'*. When these phrases are present in a message, the credential request rule is automatically suppressed.
2. **Domain Whitelist & Sender Verification:** We maintain a verified registry of 244 official Indian domain names (`trusted_domains.json`). When a message originates from a verified header (e.g., `AD-SBIBNK`) or links to an official domain like `sbi.co.in`, the URL risk is set to `0.0`.
In our automated test suite, legitimate bank messages (such as Amazon or SBI OTP alerts) score `0.0` risk with zero false positive flags."

---

### Q3: What is the processing latency of your detection pipeline?
**Strong Answer:**  
"Our API pipeline is built using **FastAPI and Python 3.14** with asynchronous I/O. 
- For text and URL scans, the complete multi-layer pipeline (Phrase Matcher + Rule Engine + URL Detector + Risk Engine) executes in **under 45 milliseconds**.
- For image uploads requiring OCR processing, Tesseract extracts text and completes full evaluation in **under 350 milliseconds**.
This ultra-low latency makes TrustLens AI suitable for real-time API integrations inside mobile banking applications."

---

## 2. Market, Impact & Feasibility Questions

### Q4: How does TrustLens AI differ from Truecaller or Chrome Safe Browsing?
**Strong Answer:**  
"Truecaller identifies *who* is calling based on crowd-sourced caller IDs, but it does not analyze the **content or psychological manipulation** inside SMS or chat messages. Chrome Safe Browsing detects known blacklisted URLs, but fails completely against **Hinglish social engineering** and **reverse UPI QR code fraud**. 

TrustLens AI fills this critical void by understanding Hinglish context, extracting text from payment receipts via OCR, and providing **plain-language explainability** (e.g., explaining why entering a PIN to receive money is fraudulent)."

---

### Q5: How will you scale your dataset to cover regional Indian languages like Tamil, Telugu, or Marathi?
**Strong Answer:**  
"Our dataset architecture in `datasets/hinglish_phrases.json` is language-agnostic and schema-driven. Each phrase entry contains language tags, category identifiers, and severity weights. 

To expand regionally:
1. We are establishing community crowdsourcing hooks via our `/api/v1/report` endpoint.
2. We can ingest translated regional dialect sets into identical JSON schemas without changing a single line of backend C++ / Python detection logic."

---

### Q6: What is your business and monetization model?
**Strong Answer:**  
"We operate a B2C / B2B hybrid model:
1. **B2C (Free Consumer Shield):** Free web application and WhatsApp bot assistant for individual citizens to check suspicious links and messages.
2. **B2B Enterprise Security API:** Offered as a SaaS API to Banks, Fintech apps (PhonePe, Paytm, CRED), and E-commerce platforms to validate payment requests and incoming SMS links before users execute transactions.
3. **Cyber Crime Intelligence Data Feed:** Providing anonymized scam trend telemetry to security operations centers (SOCs) and law enforcement agencies (I4C)."

---

## 3. Quality Assurance & Implementation Questions

### Q7: How thoroughly has TrustLens AI been tested?
**Strong Answer:**  
"We have implemented a rigorous QA validation strategy:
- We built an automated test suite (`backend/tests/test_detection_pipeline.py`) covering 28 comprehensive test cases across 8 functional categories (URL scanning, SMS scanning, Email scanning, OCR, Phrase matching, Rule engine, Risk scoring, and Explainability).
- All 28 test cases execute with a **100% Pass Rate**.
- We also conducted a full Quality Assurance audit documented in `docs/Feature_Validation_Report.md` and `docs/Bug_Reports.md`, fixing domain squatting false positives and empty URL parsing edge cases."

---

### Q8: What happens if a scammer uses an image without text (e.g. pure QR code)?
**Strong Answer:**  
"Our OCR processor handles both textual OCR and QR code payload decoding. When a user uploads a QR code image, TrustLens AI decodes the embedded string (e.g. `upi://pay?pa=scammer@upi&pn=FakeMerchant&am=15000`). If it detects a payment link or collect payload presented to a user who expected to receive money, it flags an immediate **CRITICAL RISK** alert."

---

*Q&A Matrix certified defense-ready by QA Lead.*
