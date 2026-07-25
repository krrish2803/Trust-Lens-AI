# TrustLens AI

> **Detect. Explain. Protect.**

TrustLens AI is an intelligent scam and phishing detection assistant built specifically to protect Indian users from digital financial fraud. By combining rule-based heuristics, Hinglish scam-phrase analysis, OCR-powered screenshot evaluation, and deep AI security models, TrustLens AI allows users to analyze suspicious links, SMS/WhatsApp messages, and payment receipts in real-time. It returns clear risk verdicts (Safe, Low, Medium, High, Critical), confidence scores, scam categorizations (UPI Fraud, Fake KYC, Job Scam), and plain-language explanations with step-by-step action guides.

---

## 🛠️ Tech Stack

- **Frontend:** Next.js 16 (App Router), React 19, Tailwind CSS v4, TypeScript
- **Backend:** FastAPI, Python *(backend integration pending)*
- **AI & Analytics:** NVIDIA AI APIs, Hinglish NLP detection models
- **OCR Engine:** Tesseract (for payment receipt & chat screenshot analysis)
- **Database:** MongoDB

---

## 📁 Repository Structure

```
Trust-Lens-AI/
├── frontend/                                   # Next.js web application
│   ├── app/                                    # App Router routes (Landing, Sign In, Sign Up, Home, etc.)
│   ├── components/                             # Reusable UI components & Brand SVGs
│   ├── data/                                   # Mock data for frontend preview
│   ├── public/                                 # Static assets (logo.svg, favicon.svg, icons/)
│   ├── services/                               # API & Auth service stubs (ready for FastAPI integration)
│   ├── types/                                  # TypeScript interface definitions
│   └── utils/                                  # Risk calculations & formatting helpers
├── stitch_trustlens_ai_security_assistant/     # Exported UI design reference screens
├── trustlens_ai_branding/                      # Brand identity specifications & icon specs
└── README.md                                   # Project documentation
```

---

## 🚀 Frontend Quick Start

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher

### Installation & Running Locally

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the local development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Environment Variables
Optionally create a `.env.local` file in `frontend/` if connecting to a custom backend endpoint:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## ⚙️ Backend Setup
*Backend setup and deployment instructions will be added by the backend engineering team.*
