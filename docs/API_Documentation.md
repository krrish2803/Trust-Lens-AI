# TrustLens AI REST API Specification

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Lead Backend Architect  
**Date:** July 25, 2026  
**Document Status:** Version 1.0 Production Spec  

---

## 1. Global API Information

- **Base URL (Local):** `http://localhost:8000/api/v1`
- **Base URL (Production):** `https://api.trustlens.ai/api/v1`
- **Content-Type:** `application/json`
- **Authentication:** Bearer JWT (for user history endpoints) / Public (for scan endpoints)

---

## 2. API Endpoints Reference

### 2.1 System Health Check

#### `GET /api/v1/health`
Returns the status of backend microservices, loaded detection models, and dataset counts.

**Request:**
```http
GET /api/v1/health HTTP/1.1
Host: localhost:8000
```

**Response (`200 OK`):**
```json
{
  "status": "healthy",
  "version": "2.0",
  "timestamp": "2026-07-25T20:52:50Z",
  "datasets": {
    "hinglish_phrases_count": 210,
    "trusted_domains_count": 244,
    "suspicious_domains_count": 1420
  },
  "services": {
    "phrase_matcher": "online",
    "rule_engine": "online",
    "url_detector": "online",
    "ocr_engine": "online"
  }
}
```

---

### 2.2 Unified Multi-Layer Scan

#### `POST /api/v1/scan`
Performs complete threat analysis across text, embedded URLs, and optional image OCR payload.

**Request Payload:**
```json
{
  "text": "Aapka SBI account block ho gaya hai, turant KYC update karo http://sbi-verify-kyc.com",
  "url": "http://sbi-verify-kyc.com",
  "sender_type": "unknown",
  "language_hint": "auto"
}
```

**Response (`200 OK`):**
```json
{
  "scan_id": "scan_8f91a02b4c12",
  "timestamp": "2026-07-25T20:52:50Z",
  "overall_verdict": {
    "risk_score": 0.7247,
    "risk_level": "high",
    "confidence": 0.8102,
    "verdict_text": "HIGH RISK: 4 detection layer(s) flagged this message as likely malicious. Strong warning advised.",
    "recommended_action": "WARN user strongly"
  },
  "scam_classification": {
    "scam_category": "fake_kyc",
    "category_name": "Fake KYC Scam",
    "category_description": "Scams impersonating banks/government for KYC updates",
    "confidence": 0.8102
  },
  "layer_breakdown": {
    "phrase_matcher": {
      "detected": true,
      "matches": [
        {
          "phrase": "Aapka bank account block hone wala hai",
          "type": "threat",
          "confidence": 0.95,
          "scam_category": "bank_impersonation"
        }
      ]
    },
    "rule_engine": {
      "rules_triggered": [
        {"rule_id": "R001", "name": "Urgency Language", "risk_score": 0.70},
        {"rule_id": "R004", "name": "Brand Impersonation", "risk_score": 0.85},
        {"rule_id": "R005", "name": "Account Threat", "risk_score": 0.80}
      ]
    },
    "url_detector": {
      "url": "http://sbi-verify-kyc.com",
      "final_url_risk": 0.88,
      "indicators": ["domain_squatting", "phishing_keywords"]
    }
  },
  "explainability": {
    "summary": "This message is impersonating State Bank of India (SBI) and threatening account suspension to trick you into entering credentials on an unofficial phishing site.",
    "action_steps": [
      "DO NOT click the link http://sbi-verify-kyc.com",
      "Never share OTPs, PINs, or passwords with anyone.",
      "Block the sender number immediately.",
      "Report suspicious SMS to 1930 Cyber Helpline."
    ]
  }
}
```

---

### 2.3 Standalone URL Phishing Analysis

#### `POST /api/v1/link`
Analyzes a URL for phishing keywords, domain squatting, typosquatting, and suspicious TLDs.

**Request Payload:**
```json
{
  "url": "http://sbi-kyc-update-login.com"
}
```

**Response (`200 OK`):**
```json
{
  "url": "http://sbi-kyc-update-login.com",
  "final_url_risk": 0.88,
  "verdict": "HIGH RISK: Phishing URL patterns identified.",
  "risk_indicators": [
    {
      "indicator": "domain_squatting",
      "evidence": "Domain contains bank name 'sbi' but is not an official domain",
      "risk_score": 0.85
    }
  ],
  "recommendation": "DO NOT OPEN THIS LINK. It is a spoofed bank phishing domain."
}
```

---

### 2.4 Message Text Scan

#### `POST /api/v1/message`
Scans raw text strings for 200+ Hinglish scam phrases and heuristic rules.

**Request Payload:**
```json
{
  "text": "Paisa paane ke liye UPI PIN enter karein",
  "sender_type": "unknown"
}
```

**Response (`200 OK`):**
```json
{
  "risk_score": 0.9650,
  "risk_level": "critical",
  "scam_category": "upi_scam",
  "verdict": "CRITICAL THREAT: Core UPI Fraud Pattern Detected.",
  "explanation": "UPI PIN is ONLY required to SEND money. Entering a PIN will DEBIT funds from your account."
}
```

---

### 2.5 Screenshot OCR Upload

#### `POST /api/v1/screenshot`
Processes multipart image upload, extracts text via Tesseract OCR, and executes complete scan.

**Request:** `multipart/form-data`  
**File Parameter:** `file` (Image `.png`, `.jpg`, `.jpeg`)

**Response (`200 OK`):**
```json
{
  "extracted_text": "PhonePe Receive Money: Request from Army Canteen. Enter UPI PIN to deposit Rs 15,000",
  "scan_results": {
    "risk_score": 0.9210,
    "risk_level": "critical",
    "scam_category": "upi_scam",
    "verdict": "CRITICAL RISK: Reverse QR / Collect Request Fraud detected in image text."
  }
}
```

---

### 2.6 cURL Command Examples

#### Scan Message Example:
```bash
curl -X POST "http://localhost:8000/api/v1/scan" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Aapka SBI account block ho gaya hai, turant KYC update karo http://sbi-verify.com",
           "url": "http://sbi-verify.com"
         }'
```

#### Scan Link Example:
```bash
curl -X POST "http://localhost:8000/api/v1/link" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://bit.ly/3xYz90A"}'
```

---

*API Specification certified by Lead Backend Architect.*
