# System Architecture Document: TrustLens AI

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Technical Architecture & Quality Assurance Lead  
**Date:** July 25, 2026  
**Document Status:** Approved Architecture Standard  

---

## 1. System Overview

TrustLens AI is designed as a modular, asynchronous, multi-layered cyber threat analysis ecosystem. The system handles heterogeneous inputs—including raw URLs, SMS/WhatsApp texts, email bodies, and screenshot images—processes them through parallel analytical engines, and produces a unified risk assessment with actionable explainability.

---

## 2. High-Level System Architecture Diagram

```mermaid
graph TD
    User([User / Browser Client]) -->|HTTP / REST| Frontend[Next.js 16 App Router]
    Frontend -->|JSON Payload / Form Data| API Gateway[FastAPI Gateway Router]
    
    subgraph Backend Core Engine
        API Gateway --> Scanner[Unified Scan Controller]
        
        Scanner -->|Image File| OCR[Tesseract OCR Engine]
        OCR -->|Extracted Text| PhraseMatcher
        
        Scanner -->|URL / Link| URLDetector[URL Phishing Detector]
        Scanner -->|Raw Text / SMS / Email| PhraseMatcher[Hinglish Phrase Matcher]
        Scanner -->|Text & Sender Metadata| RuleEngine[15-Rule Heuristic Engine]
        
        URLDetector -->|URL Risk & Flags| ScamClassifier[14-Category Scam Classifier]
        PhraseMatcher -->|Matched Phrases & Conf| ScamClassifier
        RuleEngine -->|Triggered Rules & Evid| ScamClassifier
        
        PhraseMatcher -->|Phrase Score| RiskEngine[Multi-Layer Risk Aggregator]
        RuleEngine -->|Rule Risk Score| RiskEngine
        URLDetector -->|URL Risk Score| RiskEngine
        ScamClassifier -->|Category Risk Score| RiskEngine
        
        RiskEngine -->|Weighted Risk Score| ExplainEngine[Explainability & Verdict Engine]
    end
    
    subgraph Data Layer
        URLDetector <-->|Query| TrustedDB[(trusted_domains.json)]
        URLDetector <-->|Query| SuspiciousDB[(suspicious_domains.json)]
        PhraseMatcher <-->|Query| HinglishDB[(hinglish_phrases.json - 210 Entries)]
        Scanner <-->|Audit History| Mongo[(MongoDB Instance)]
    end
    
    ExplainEngine -->|Final JSON Response| API Gateway
    API Gateway -->|Risk Level, Score, Actions| Frontend
    Frontend -->|Visual Dashboard & Guidance| User
```

---

## 3. Core Architectural Sub-Systems

### 3.1 Frontend Layer (Next.js 16 & React 19)
- **App Router Architecture:** Modular route organization (`/`, `/scan`, `/report`, `/history`, `/dashboard`).
- **Client-Side State Management:** React Hooks and context provider handling real-time scan progress, file upload staging, and error boundaries.
- **Visual Design System:** Custom dark-mode UI tokens utilizing Tailwind CSS v4, dynamic color coding (Green = Safe, Blue = Low, Yellow = Medium, Orange = High, Red = Critical), glassmorphism components, and responsive cards.

### 3.2 API Gateway Layer (FastAPI)
- **FastAPI Gateway Router:** Asynchronous ASGI web gateway running under Uvicorn.
- **Middleware Pipeline:** CORS middleware, request payload validation via Pydantic v2 schemas, rate limiting, and centralized error handling middleware.

### 3.3 Analytical Engine Layer

#### Layer A: Tesseract OCR Engine (`ScreenshotOCR`)
- Pre-processes uploaded image files (grayscale conversion, thresholding, contrast adjustment).
- Extracts textual strings from payment receipts, WhatsApp chats, and digital certificates.
- Forwards extracted text seamlessly into the primary scanning pipeline.

#### Layer B: URL Detector (`URLDetector`)
- Performs structural URL parsing, hostname extraction, and TLD lookup against a dataset of 30+ suspicious TLDs (`.xyz`, `.top`, `.club`, `.loan`).
- Detects domain squatting and typosquatting by cross-referencing brand aliases against official bank domain registries (`trusted_domains.json`).
- Checks for URL shortener masking (`bit.ly`, `tinyurl`, `t.co`) and raw IP address host usage.

#### Layer C: Hinglish Phrase Matcher (`PhraseMatcher`)
- Loads a dataset of 210 verified Hinglish scam phrases categorized across 14 scam types.
- Evaluates input using a hybrid 3-tier strategy:
  1. Exact String Matching on normalized text.
  2. Variation Matching across common Hinglish spelling variations.
  3. Fuzzy N-Gram Sequence Matching (using `SequenceMatcher` with 0.80 similarity threshold).

#### Layer D: Rule Engine (`RuleEngine`)
- Evaluates text against 15 predefined security rules (Urgency, Credential Request, Payment Request, Brand Impersonation, Account Threat, Reward/Prize Offer, Unknown Sender, etc.).
- Implements negative safety phrase checks (`"do not share"`, `"never share"`) to eliminate false positive flags on official bank advisory messages.

#### Layer E: Scam Classifier (`ScamClassifier`)
- Aggregates multi-source evidence (keyword matches, phrase matches, triggered rules, and URL risk).
- Maps threat patterns to 14 distinct scam categories (e.g., Fake KYC, UPI Fraud, Job Scam, Cyber Arrest, Delivery Scam).

#### Layer F: Multi-Layer Risk Aggregator (`RiskEngine`)
- Computes final risk score using weighted layer contributions:
  $$\text{Risk Score} = 0.35 \cdot S_{\text{phrase}} + 0.30 \cdot S_{\text{rules}} + 0.25 \cdot S_{\text{url}} + 0.10 \cdot S_{\text{pattern}}$$
- Maps computed numeric risk score to standardized Risk Levels:
  - **Critical:** $0.85 \le \text{Score} \le 1.00$ (Action: Block immediately)
  - **High:** $0.65 \le \text{Score} < 0.85$ (Action: Warn user strongly)
  - **Medium:** $0.45 \le \text{Score} < 0.65$ (Action: Caution advised)
  - **Low:** $0.20 \le \text{Score} < 0.45$ (Action: Monitor recommended)
  - **Safe:** $0.00 \le \text{Score} < 0.20$ (Action: Approved - safe)

#### Layer G: Explainability & Action Generator (`ExplainabilityEngine`)
- Converts complex technical detection indicators into plain-language summaries understandable by non-technical users.
- Renders step-by-step emergency action checklists (e.g., reporting to 1930 Cyber Helpline, freezing UPI PINs, blocking SIM cards).

---

## 4. Data Storage & Schema Design

- **MongoDB Database:** Stores user profiles, scan history logs, and community scam reports.
- **JSON File Datasets:** In-memory cached lookup tables for ultra-fast, zero-latency domain and phrase matching (`trusted_domains.json`, `hinglish_phrases.json`, `bank_names.json`).

---

## 5. Security & Privacy Architecture

- **Data Privacy:** Text inputs and uploaded screenshot images are processed in-memory for analysis and not used for AI model training.
- **Zero Third-Party Data Leakage:** All rule evaluations and Hinglish pattern matching run locally within the backend container.
- **Validation Controls:** Input sanitization against RegEx denial of service (ReDoS) and malicious script injection.

---

*Architecture Specification certified by Lead Backend Architect.*
