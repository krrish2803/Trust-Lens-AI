# TrustLens AI - API Specification

## Endpoints

### 1. Health Check
`GET /health`

**Response:**
```json
{
  "status": "healthy",
  "app": "TrustLens AI",
  "version": "1.0.0",
  "timestamp": "2026-07-25T14:00:00Z",
  "components": {
    "database": "connected",
    "ai_engine": "configured (NVIDIA NIM)",
    "ocr_engine": "ready"
  }
}
```

---

### 2. Scan URL
`POST /scan/url`

**Request Body:**
```json
{
  "url": "http://sbi-kyc-update.online"
}
```

**Response:**
```json
{
  "id": "url-a1b2c3d4",
  "scan_type": "url",
  "input_summary": "http://sbi-kyc-update.online",
  "risk_score": 88,
  "confidence_score": 0.95,
  "verdict": "Critical",
  "scam_category": "Phishing URL / Fake Site",
  "matched_phrases": [],
  "detected_urls": ["http://sbi-kyc-update.online"],
  "reasons": ["Domain contains suspicious TLD (.online)", "Typosquatted bank brand (sbi)"],
  "recommended_actions": [
    "⛔ DO NOT click on any links.",
    "🔒 NEVER share your OTP or passwords.",
    "📢 Report scam on cybercrime.gov.in or call 1930."
  ],
  "created_at": "2026-07-25T14:00:00Z"
}
```

---

### 3. Scan Message
`POST /scan/message`

**Request Body:**
```json
{
  "text": "Dear customer your HDFC account is blocked click here to update KYC immediately: http://bit.ly/fake-hdfc",
  "channel": "sms"
}
```

---

### 4. Scan Image / Screenshot
`POST /scan/image` (Multipart Form or JSON Base64)

---

### 5. Scan History
`GET /history?limit=20&skip=0`
