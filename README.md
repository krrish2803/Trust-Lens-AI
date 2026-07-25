# TrustLens AI 🛡️
> **Detect. Explain. Protect.**
> AI-powered Scam & Phishing Detection Platform custom-built for Indian users.

![TrustLens AI Banner](https://img.shields.io/badge/TrustLens-AI-cyan?style=for-the-badge&logo=shield)
![Next.js 15](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=nextdotjs)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)
![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM%20API-76B900?style=for-the-badge&logo=nvidia)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb)

---

## 🚀 Overview

**TrustLens AI** is an advanced 8-layer cybersecurity defense platform designed to protect Indian citizens from rapidly escalating digital scams, including:
- **OTP & Credential Scams** (Requests for bank passwords, UPI PINs, CVVs)
- **KYC & SIM Update Fraud** (Threats of account/SIM suspension)
- **Bank Impersonation** (Fake SBI, HDFC, ICICI, Axis SMS alerts)
- **Delivery & Courier Scams** (India Post/BlueDart parcel address fee traps)
- **KBC & WhatsApp Lottery Fraud** (Fake reward claims & lucky draw links)
- **CBI / Customs Digital Arrests** (Law enforcement impersonation)
- **Fake Instant Loan Apps** (Pre-approved loan processing fee traps)
- **Work-From-Home Task Scams** (Prepaid Telegram rating tasks)

---

## ⚡ 8-Layer Multi-Tiered Architecture

1. **Hinglish Scam Phrase Library**: Matching against 200+ localized Hinglish phrase patterns.
2. **Multi-Category Rule Engine**: Deterministic rules across 10 distinct Indian scam types.
3. **URL & Domain Analyzer**: Detection of IP address links, shorteners, typosquatting, and fake TLDs.
4. **EasyOCR Image Engine**: Text extraction from WhatsApp screenshots and payment app receipts.
5. **NVIDIA AI Deep Analysis**: LLM threat classification powered by NVIDIA NIM (`meta/llama-3.3-70b-instruct`).
6. **Risk Scoring Engine**: Weighted 0–100 risk score assignment (Safe, Low, Medium, High, Critical).
7. **Explainability Engine**: Human-understandable bulleted threat rationale.
8. **Action Recommendation Engine**: Context-aware safety steps & emergency actions (Cyber Crime 1930).

---

## 📦 Tech Stack

- **Frontend**: Next.js 15, TypeScript, TailwindCSS, Framer Motion, Lucide Icons
- **Backend**: Python 3.11+, FastAPI, Pydantic v2
- **Database**: MongoDB (Async Motor driver) with in-memory fallback
- **AI & OCR**: NVIDIA NIM API, EasyOCR (PyTorch), OpenCV
- **Deployment**: Docker, Render (`render.yaml`), Vercel (`vercel.json`)

---

## 🔧 Local Development Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- MongoDB (Optional, in-memory fallback available)

### 2. Backend Setup
```bash
# Clone repository
git clone https://github.com/krrish2803/Trust-Lens-AI.git
cd Trust-Lens-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run FastAPI server
uvicorn backend.app:app --reload --port 8000
```
API Documentation available at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Running Tests

```bash
# Run pytest backend test suite
pytest backend/tests -v
```

---

## 📄 License
Licensed under the [MIT License](LICENSE).
