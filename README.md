# TrustLens AI 🛡️
> **Detect. Explain. Protect.**
> AI-powered Scam & Phishing Detection Platform custom-built for Indian users.

![TrustLens AI Banner](trustlens_ai_branding/logo.svg)

TrustLens AI is an intelligent, multi-layered cyber scam and phishing detection ecosystem built specifically to protect Indian users from digital financial fraud. By combining rule-based heuristics, Hinglish scam-phrase analysis (200+ verified patterns), OCR-powered screenshot evaluation, and deep AI security models, TrustLens AI allows users to analyze suspicious links, SMS/WhatsApp messages, emails, and payment receipts in real time. 

It provides instant risk verdicts (**Safe**, **Low**, **Medium**, **High**, **Critical**), multi-layered confidence scores, scam categorizations (e.g., UPI Fraud, Fake KYC, Job Scam, Cyber Arrest), and plain-language explainability with step-by-step emergency action guides.

---

## 💡 Key Features

- **🌐 URL Phishing Detection:** Analyzes domain squatting, typosquatting, suspicious TLDs (`.xyz`, `.top`, `.club`), URL shorteners (`bit.ly`, `tinyurl`), and IP host patterns.
- **💬 Hinglish Scam Phrase Matcher:** Trained on a dataset of 200+ authentic Hinglish fraud patterns spanning 14 Indian cyber scam categories.
- **📸 Screenshot OCR Analysis:** Tesseract OCR engine extracts text from payment receipts, WhatsApp chats, and fake lottery cheques to detect reverse QR & collect requests.
- **🛡️ 15-Rule Heuristic Engine:** Evaluates urgency language, credential harvesting, brand impersonation, authority threats, and time pressure tactics.
- **🎯 Multi-Layer Risk Scoring:** Combines weighted scores across phrase matching (35%), rule engine (30%), URL detector (25%), and scam classifier (10%).
- **🧠 Plain-Language Explainability:** Generates clear, non-technical explanations and step-by-step action guides (e.g., "Never enter UPI PIN to receive money").
- **🚨 Instant Bug Reporting & QA Portal:** Built-in validation suite ensuring technical precision and zero false positives on official banking domains.

---

## 🚀 Overview

### Frontend Application
- **Framework:** Next.js 16 (App Router)
- **UI Library:** React 19, TypeScript
- **Styling:** Tailwind CSS v4, Lucide React Icons
- **State Management:** React Hooks & Context API

### Backend Microservices
- **API Framework:** FastAPI / Python 3.14
- **Web Server:** Uvicorn
- **Data Schemas:** Pydantic v2
- **OCR Engine:** Tesseract OCR (PyTesseract)
- **Database:** MongoDB (Async Motor driver)

### AI & Security Models
- **NLP Engine:** Custom Hinglish Pattern Matcher + Fuzzy Sequence Matcher
- **Security APIs:** NVIDIA AI Security Models / Google Gemini 1.5 Pro integration ready

---

## ⚡ 8-Layer Multi-Tiered Architecture

```
Trust-Lens-AI/
├── backend/                                   # FastAPI Python Backend Application
│   ├── ai/                                    # AI Model & Prompt Interfaces
│   ├── api/                                   # REST API Endpoint Routers (scan, link, message, screenshot, history, report)
│   ├── database/                              # MongoDB Connection & ODM Mappers
│   ├── detection/                             # Core Scam Detection Engines
│   │   ├── domain_checker.py                 # Whitelist & Domain Squatting Analyzer
│   │   ├── pattern_analyzer.py                # RegEx & Pattern Extraction Engine
│   │   ├── phrase_matcher.py                 # 200+ Hinglish Phrase Matching Engine
│   │   ├── risk_engine.py                    # Multi-Layer Risk Scoring & Aggregation
│   │   ├── rule_engine.py                    # 15 Predefined Security Rules
│   │   ├── scam_classifier.py                # 14 Scam Category Classifier
│   │   ├── url_detector.py                   # URL Phishing & TLD Analyzer
│   │   └── utils.py                          # String Normalization & Text Utilities
│   ├── models/                                # Pydantic Request/Response Models
│   ├── ocr/                                   # Tesseract OCR Screenshot Processor
│   ├── tests/                                 # PyTest & Unittest Suite (100% Pass Rate)
│   └── app.py                                 # FastAPI Main Application Gateway
├── datasets/                                  # Verified JSON Datasets
│   ├── bank_names.json                        # Indian Bank Names & Aliases
│   ├── fake_brand_patterns.json               # Brand Impersonation Rules
│   ├── hinglish_phrases.json                  # 200+ Verified Hinglish Scam Phrases
│   ├── phishing_keywords.json                 # High-Risk Phishing Keywords
│   ├── scam_templates.json                    # Fraud Message Templates
│   ├── suspicious_domains.json                # Known Phishing Domains
│   ├── trusted_domains.json                   # Verified Official Indian Domains
│   └── upi_patterns.json                      # UPI Fraud RegEx Patterns
├── docs/                                      # Complete Project Documentation
│   ├── AI_Workflow.md                         # AI Security Pipeline Workflow
│   ├── API_Documentation.md                   # Full REST API Reference
│   ├── Architecture.md                        # System Architecture & Diagram
│   ├── Bug_Reports.md                         # QA Bug Reports & Remediation Log
│   ├── Database_Schema.md                     # MongoDB Collections & Indexes
│   ├── Demo_Script.md                         # 3-Min & 5-Min Pitch Demo Scripts
│   ├── Deployment_Guide.md                    # Docker & Cloud Deployment Guide
│   ├── Feature_Validation_Report.md           # End-to-End QA Validation Audit
│   ├── Judge_QA.md                            # Hackathon Judge Q&A Matrix
│   ├── Research_Report.md                     # Indian Cyber Scams Research Report
│   ├── Test_Cases.md                          # 28 Verified Test Execution Cases
│   ├── User_Guide.md                          # User Operation Manual
│   └── Workflow.md                            # End-to-End Execution Flowchart
├── frontend/                                  # Next.js 16 Web Application
│   ├── app/                                   # App Router Pages (Landing, Dashboard, Scan, Report)
│   ├── components/                            # UI Components & Brand SVGs
│   ├── data/                                  # Mock & Preview Datasets
│   ├── services/                              # API Client & Backend Connection Services
│   └── types/                                 # TypeScript Interfaces
├── presentation/                              # Presentation Support Assets
│   ├── Demo_Video.mp4                         # Live System Walkthrough Video
│   ├── Pitch.pdf                              # Pitch Presentation Deck PDF
│   ├── Poster.png                             # Project Hackathon Poster
│   └── PPT_Review_and_Enhancements.md        # Slide-by-Slide Enhancement Audit
├── docker-compose.yml                         # Full-Stack Container Orchestration
├── requirements.txt                           # Backend Python Dependencies
└── README.md                                  # Root Documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: v3.10 or higher
- **Node.js**: v18.0.0 or higher
- **Tesseract OCR**: Installed on host OS (optional for local non-OCR testing)

---

### 1. Backend Setup & Run

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run backend test suite to verify pipeline:**
   ```bash
   python -m unittest tests/test_detection_pipeline.py
   ```

5. **Start the FastAPI development server:**
   ```bash
   python -m uvicorn app:app --reload --port 8000
   ```
   *The interactive API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs)*

---

### 2. Frontend Setup & Run

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

4. **Access Application:**
   Open browser at [http://localhost:3000](http://localhost:3000)

---

## 🔌 API Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /api/v1/health` | `GET` | System health check & dataset status |
| `POST /api/v1/scan` | `POST` | Unified multi-layer threat scan (Text / URL / Image) |
| `POST /api/v1/link` | `POST` | Standalone URL phishing & domain analysis |
| `POST /api/v1/message` | `POST` | SMS, Email & WhatsApp text phrase analysis |
| `POST /api/v1/screenshot` | `POST` | Upload screenshot image for OCR text extraction & scan |
| `GET /api/v1/history` | `GET` | Retrieve user scan audit history |
| `POST /api/v1/report` | `POST` | Submit newly discovered scam message to community database |

---

## 👥 Team Members

- **Lead AI & Backend Architect:** Cyber Security & NLP Engineering Lead
- **Frontend Lead & UI Designer:** UX & Product Designer
- **Research, Documentation, Testing & QA Lead:** System Validation & Technical Writer

---

## 🔮 Future Scope & Roadmap

1. **Multilingual Regional Expansion:** Extending phrase matcher datasets to Tamil, Telugu, Bengali, Marathi, and Kannada.
2. **Browser Extension:** Chrome & Firefox extension to automatically flag phishing URLs and fake UPI payment popups in real time.
3. **WhatsApp Bot Integration:** Interactive WhatsApp business bot allowing users to forward suspicious messages directly for instant verification.
4. **On-Device Mobile SDK:** Lightweight Android SDK for integration into banking applications to intercept SMS fraud before execution.
5. **Real-time Threat Intelligence Exchange:** Automated reporting gateway connecting flagged scam accounts directly to I4C (1930 Cyber Helpline portal).

---

*TrustLens AI — Empowering Indian citizens with AI-driven cyber defense.*
