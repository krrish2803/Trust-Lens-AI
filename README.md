# TrustLens AI

> **Detect. Explain. Protect.**

AI-powered Scam & Phishing Detection Platform built for Indian users.

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)
![Next.js 16](https://img.shields.io/badge/Next.js-16-black.svg)

---

## Problem Statement

India loses over **₹10,000 crore annually** to digital payment fraud. With 800M+ UPI users, scammers exploit Hinglish messages, fake KYC links, OTP phishing, and UPI QR fraud to target vulnerable populations — often elderly users and first-time digital payment adopters.

Existing solutions focus on English-language spam detection and fail to catch:
- **Hinglish scam phrases** like "OTP batao", "account freeze ho jayega"
- **Fake banking URLs** mimicking SBI, HDFC, ICICI with typosquatting
- **Payment screenshot fraud** using manipulated QR codes and receipts
- **Multi-channel attacks** spanning SMS, WhatsApp, Telegram, and email

There is no unified, open-source tool that combines OCR, Hinglish NLP, and AI analysis for Indian scam detection.

---

## Proposed Solution

TrustLens AI is a **multi-layered detection pipeline** that analyzes suspicious content through 6 independent engines and produces a unified risk verdict:

| Layer | What It Does | Example |
|-------|-------------|---------|
| **Hinglish Phrase Matcher** | Matches 200+ verified scam phrases with fuzzy matching | "OTP batao", "account block" |
| **Rule Engine** | 15 heuristic rules for urgency, credential harvesting, brand impersonation | Detects "share OTP immediately" |
| **URL Detector** | Analyzes domain squatting, suspicious TLDs, URL shorteners | `sbi-kyc-update.online` |
| **Domain Checker** | Checks against 244 trusted + 1000 suspicious domains | Flags `bit.ly/free-kbc-reward` |
| **Pattern Analyzer** | Social engineering, urgency indicators, emotional triggers | Detects authority threats |
| **Scam Classifier** | Categorizes into 13 scam types (OTP, KYC, UPI fraud, etc.) | Labels as "OTP Scam" |

Results are blended with **NVIDIA NIM AI** (Nemotron 49B) for nuanced analysis, producing:
- Risk score (0-100) with 5 verdict levels
- Plain-language explanation in English/Hinglish
- Step-by-step emergency action guide

---

## Key Features

- **URL Phishing Detection** — Domain squatting, typosquatting, suspicious TLDs, URL shorteners
- **Hinglish Scam Phrase Matcher** — 200+ verified fraud patterns across 14 Indian scam categories
- **Screenshot OCR Analysis** — EasyOCR extracts text from payment receipts, WhatsApp chats, banking screens
- **AI-Powered Analysis** — NVIDIA NIM (Nemotron 49B) for nuanced threat assessment
- **13-Category Scam Classification** — OTP, KYC, UPI, lottery, job, loan, digital arrest scams
- **Plain-Language Explainability** — Non-technical explanations and action guides
- **JWT Authentication** — Secure user accounts with bcrypt password hashing
- **Scan History** — Full audit trail saved to MongoDB

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4 |
| Backend | FastAPI, Python 3.11, Pydantic v2, Uvicorn |
| AI Engine | NVIDIA NIM API (`nvidia/llama-3.3-nemotron-super-49b-v1.5`) |
| OCR | EasyOCR (Hindi + English) |
| Database | MongoDB Atlas (Motor async driver) |
| Auth | JWT + bcrypt (python-jose, passlib) |
| Deployment | Docker, Render, Vercel |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (free tier works)
- NVIDIA NIM API key (free at [build.nvidia.com](https://build.nvidia.com))

### 1. Clone & Setup Backend

```bash
git clone https://github.com/krrish2803/Trust-Lens-AI.git
cd Trust-Lens-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and NVIDIA API key
```

### 2. Start Backend

```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5001 --reload
```

API docs: [http://localhost:5001/docs](http://localhost:5001/docs)

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### 4. Run Tests

```bash
python -m pytest backend/tests/ -v
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/?appName=Cluster0
MONGODB_DB_NAME=trustlens_db

# NVIDIA NIM AI
NVIDIA_NIM_API_KEY=nvapi-xxxxx

# Server
DEBUG=False
SECRET_KEY=your-secret-key-here
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/api/auth/signup` | POST | Create account |
| `/api/auth/login` | POST | Login, get JWT |
| `/api/auth/me` | GET | Get current user |
| `/scan/url` | POST | Scan a URL for phishing |
| `/scan/message` | POST | Scan SMS/WhatsApp/email text |
| `/scan/image` | POST | Upload screenshot for OCR + scan |
| `/history` | GET | Get scan history |

---

## File Structure

```
Trust-Lens-AI/
├── backend/
│   ├── ai/                        # AI model integration
│   │   ├── classifier.py          # NVIDIA NIM classifier orchestrator
│   │   ├── confidence_score.py    # Confidence calculator
│   │   ├── explainability.py      # Plain-language explanation generator
│   │   ├── nvidia_client.py       # NVIDIA NIM API client
│   │   └── prompt_builder.py      # Prompt construction + injection defense
│   ├── api/                       # FastAPI route handlers
│   │   ├── auth.py                # JWT signup/login/profile
│   │   ├── health.py              # Health check endpoint
│   │   ├── history.py             # Scan history endpoints
│   │   ├── message.py             # Text/SMS/WhatsApp scan
│   │   ├── scan.py                # Unified auto-scan endpoint
│   │   ├── screenshot.py          # Image/OCR scan
│   │   └── url.py                 # URL phishing scan
│   ├── database/                  # MongoDB layer
│   │   ├── history.py             # History repository
│   │   ├── models.py              # DB document schemas
│   │   └── mongodb.py             # Connection manager + in-memory fallback
│   ├── detection/                 # Core detection engines
│   │   ├── domain_checker.py      # 244 trusted + 1000 suspicious domains
│   │   ├── pattern_analyzer.py    # Social engineering + urgency patterns
│   │   ├── phrase_matcher.py      # 200+ Hinglish scam phrases
│   │   ├── risk_engine.py         # Multi-layer risk aggregation
│   │   ├── rule_engine.py         # 15 heuristic security rules
│   │   ├── scam_classifier.py     # 13-category scam classifier
│   │   ├── url_detector.py        # URL phishing + TLD analyzer
│   │   └── utils.py               # Text normalization utilities
│   ├── models/
│   │   └── schemas.py             # Pydantic request/response models
│   ├── ocr/                       # OCR pipeline
│   │   ├── image_reader.py        # EasyOCR wrapper
│   │   ├── preprocessing.py       # Image enhancement
│   │   └── screenshot_parser.py   # OCR error correction + entity extraction
│   ├── tests/                     # Test suite (20 tests)
│   ├── app.py                     # FastAPI app entry point
│   ├── config.py                  # Centralized configuration
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── app/                       # Next.js App Router pages
│   │   ├── page.tsx               # Landing page
│   │   ├── home/page.tsx          # Authenticated home
│   │   ├── scan/                  # Scan pages (URL, message, image)
│   │   ├── result/page.tsx        # Scan result display
│   │   ├── history/page.tsx       # Scan history
│   │   ├── signin/page.tsx        # Login
│   │   └── signup/page.tsx        # Registration
│   ├── components/                # Reusable UI components
│   │   ├── UploadBox.tsx          # Multi-tab scan input
│   │   ├── RiskMeter.tsx          # Animated circular risk gauge
│   │   ├── VerdictCard.tsx        # Verdict display card
│   │   ├── ActionGuide.tsx        # Emergency action steps
│   │   └── ...                    # 15+ components
│   ├── services/
│   │   ├── api.ts                 # API client with auth headers
│   │   └── auth.ts                # JWT token management
│   └── types/
│       └── index.ts               # TypeScript interfaces
├── datasets/                      # JSON detection datasets
│   ├── hinglish_phrases.json      # 200+ scam phrases
│   ├── trusted_domains.json       # 244 verified Indian domains
│   ├── suspicious_domains.json    # 1000+ known phishing domains
│   └── ...                        # 8 dataset files
├── Dockerfile                     # Multi-stage Docker build
├── docker-compose.yml             # Full-stack orchestration
├── render.yaml                    # Render deploy config
└── LICENSE                        # MIT License
```

---

## How It Works

```
User Input (URL / Text / Screenshot)
        │
        ▼
┌─────────────────────────────────────┐
│         Input Router                │
│   (URL? → url.py)                   │
│   (Text? → message.py)              │
│   (Image? → screenshot.py)          │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Phrase  │ │Rule    │ │URL     │
│Matcher │ │Engine  │ │Detector│
│(200+)  │ │(15)    │ │        │
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    ▼          ▼          ▼
┌─────────────────────────────────────┐
│     Risk Score Aggregator           │
│  rule_score × 0.60                  │
│  + phrase_score × 0.25              │
│  + url_score × 0.15                 │
│  + pattern_boost × 0.10             │
│  (floor: 70 if rules trigger)       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     NVIDIA NIM AI Analysis          │
│  (nemotron-49b blending)            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Verdict + Explanation + Actions    │
│  Risk: 0-100 │ Category │ Guide    │
└─────────────────────────────────────┘
```

---

## Detection Categories

| # | Category | Example |
|---|----------|---------|
| 1 | OTP Scam | "OTP batao", "share your OTP" |
| 2 | KYC Scam | "KYC update pending, account blocked" |
| 3 | Bank Impersonation | Fake SBI/HDFC/ICICI alerts |
| 4 | Delivery Scam | "India Post parcel stuck, pay fee" |
| 5 | Lottery & Prize | "KBC lottery won, claim reward" |
| 6 | UPI Fraud | "Scan QR to receive money" |
| 7 | Investment Scam | "Guaranteed 10x return" |
| 8 | Job Scam | "Work from home, earn 50k daily" |
| 9 | Fake Loan | "Instant loan approved, pay processing fee" |
| 10 | Digital Arrest | "CBI investigating, join video call" |
| 11 | Phishing URL | Fake banking login pages |
| 12 | Tax Refund | "Income tax refund pending" |
| 13 | Safe Content | Legitimate messages |

---

## Contributing

Contributions welcome! Please open an issue or PR.

```bash
# Fork → Branch → Commit → PR
git checkout -b feature/your-feature
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- NVIDIA NIM for AI inference API
- EasyOCR for multilingual text extraction
- MongoDB Atlas for database hosting
- The Indian cybersecurity community for scam pattern research

---

**TrustLens AI** — Empowering Indian citizens with AI-driven cyber defense.
