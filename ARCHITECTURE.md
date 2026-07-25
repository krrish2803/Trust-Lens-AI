# TrustLens AI — System Architecture

> Visual architecture documentation with Mermaid diagrams.

---

## High-Level System Architecture

```mermaid
graph TB
    User([👤 User])

    subgraph Frontend ["Frontend — Next.js 16"]
        UI[React 19 UI]
        AuthSvc[Auth Service<br/>JWT + localStorage]
        APIClient[API Client<br/>Authorization Header]
    end

    subgraph Backend ["Backend — FastAPI + Python 3.11"]
        Gateway[API Gateway<br/>Rate Limiter + CORS]
        
        subgraph Auth ["Authentication"]
            JWT[JWT Auth<br/>bcrypt + jose]
        end

        subgraph Scan ["Scan Endpoints"]
            URLScan["/scan/url"]
            MsgScan["/scan/message"]
            ImgScan["/scan/image"]
            AutoScan["/scan/ (auto)"]
        end

        subgraph Detection ["Detection Pipeline"]
            PM[Phrase Matcher<br/>200+ Hinglish phrases]
            RE[Rule Engine<br/>15 heuristic rules]
            UD[URL Detector<br/>Phishing + TLD]
            DC[Domain Checker<br/>244 trusted + 1000 suspicious]
            PA[Pattern Analyzer<br/>Social engineering]
            SC[Scam Classifier<br/>13 categories]
        end

        subgraph AI ["AI Engine"]
            NC[NVIDIA NIM Client<br/>Nemotron 49B]
            PB[Prompt Builder<br/>Injection defense]
            CC[Confidence Calculator]
            EE[Explainability Engine]
        end

        subgraph OCR ["OCR Pipeline"]
            IE[Image Enhancement]
            ER[EasyOCR Reader<br/>Hindi + English]
            SP[Screenshot Parser<br/>Error correction]
        end

        subgraph Data ["Data Layer"]
            MG[(MongoDB Atlas<br/>history + users)]
            DS[(JSON Datasets<br/>phrases, domains)]
        end
    end

    subgraph External ["External APIs"]
        NVIDIA[NVIDIA NIM API<br/>nemotron-49b-v1.5]
    end

    User -->|Browser| UI
    UI --> AuthSvc
    AuthSvc --> APIClient
    APIClient -->|HTTP REST| Gateway

    Gateway --> JWT
    Gateway --> Scan

    URLScan --> UD
    URLScan --> DC
    URLScan --> RE

    MsgScan --> PM
    MsgScan --> RE
    MsgScan --> PA

    ImgScan --> IE
    IE --> ER
    ER --> SP
    SP --> PM
    SP --> RE

    AutoScan -->|URL detected| URLScan
    AutoScan -->|Text detected| MsgScan

    PM --> SC
    RE --> SC
    UD --> SC
    PA --> SC

    SC --> CC
    CC --> NC
    NC -->|API call| NVIDIA
    NC --> EE

    MG -.->|save/load| Scan
    DS -.->|query| Detection
```

---

## Request Flow — URL Scan

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant G as Gateway
    participant URL as URL Endpoint
    participant UD as URL Detector
    participant DC as Domain Checker
    participant RE as Rule Engine
    participant SC as Scam Classifier
    participant AI as NVIDIA NIM
    participant DB as MongoDB

    U->>F: Enter suspicious URL
    F->>G: POST /scan/url<br/>{url: "sbi-kyc-update.online"}
    G->>G: Rate limit check
    
    par Parallel Detection
        URL->>UD: analyze(url)
        UD-->>URL: phishing_score=0.9
        URL->>DC: check(url)
        DC-->>URL: status=suspicious, score=0.3
        URL->>RE: evaluate(url)
        RE-->>URL: rule_score=85, rules=[4 triggered]
    end

    URL->>SC: classify(text, results)
    SC-->>URL: category="KYC Scam", confidence=0.8

    URL->>AI: classify_content(url, findings)
    AI-->>URL: risk_score=90, explanation="..."

    URL->>URL: combined_risk = 90
    URL->>DB: save_scan(result)
    URL-->>F: ScanResultResponse
    F-->>U: Score: 90, Verdict: Critical
```

---

## Request Flow — Message Scan

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant MSG as Message Endpoint
    participant PM as Phrase Matcher
    participant RE as Rule Engine
    participant PA as Pattern Analyzer
    participant SC as Scam Classifier
    participant AI as NVIDIA NIM
    participant DB as MongoDB

    U->>F: Paste SMS/WhatsApp text
    F->>G: POST /scan/message<br/>{text: "Dear Customer..."}

    par Parallel Detection
        MSG->>PM: detect(text)
        PM-->>MSG: phrases=["OTP batao"]
        MSG->>RE: evaluate(text)
        RE-->>MSG: score=100, rules=[4 triggered]
        MSG->>PA: analyze(text)
        PA-->>MSG: urgency=2, social_eng=1
    end

    MSG->>SC: classify(text, results)
    SC-->>MSG: category="OTP Scam", confidence=0.85

    MSG->>MSG: combined_risk = 70<br/>(rule_score×0.6 + phrase×0.25 + pattern×0.15)

    MSG->>AI: classify_content(text, findings)
    AI-->>MSG: risk_score=75, explanation="..."

    MSG->>DB: save_scan(result)
    MSG-->>F: ScanResultResponse
    F-->>U: Score: 70, Verdict: High Risk
```

---

## Detection Pipeline Architecture

```mermaid
graph LR
    subgraph Input ["Input"]
        URL[URL]
        TXT[Text]
        IMG[Image]
    end

    subgraph Layer1 ["Layer 1 — Extraction"]
        UD[URL Detector<br/>phishing score]
        DC[Domain Checker<br/>reputation]
        PM[Phrase Matcher<br/>200+ patterns]
        RE[Rule Engine<br/>15 rules]
        ER[EasyOCR<br/>text extraction]
        PA[Pattern Analyzer<br/>social eng.]
    end

    subgraph Layer2 ["Layer 2 — Classification"]
        SC[Scam Classifier<br/>13 categories]
    end

    subgraph Layer3 ["Layer 3 — Aggregation"]
        RS[Risk Scorer<br/>weighted blend]
        CC[Confidence Calc]
    end

    subgraph Layer4 ["Layer 4 — AI Enhancement"]
        AI[NVIDIA NIM<br/>Nemotron 49B]
        EE[Explainability<br/>plain language]
    end

    subgraph Output ["Output"]
        VERDICT[Verdict<br/>Score + Category<br/>+ Explanation<br/>+ Actions]
    end

    URL --> UD --> SC
    URL --> DC --> SC
    TXT --> PM --> SC
    TXT --> RE --> SC
    TXT --> PA --> SC
    IMG --> ER --> PM

    SC --> RS --> CC --> AI --> EE --> VERDICT
```

---

## Scoring Model

```mermaid
graph TD
    subgraph Inputs ["Detection Scores (0-100)"]
        RS[Rule Score<br/>0-100]
        PS[Phrase Score<br/>0-100]
        US[URL Risk Score<br/>0-100]
        PB[Pattern Boost<br/>0-30]
    end

    subgraph Weights ["Weighted Combination"]
        W1["rule_score × 0.60"]
        W2["phrase_score × 0.25"]
        W3["url_risk × 0.15"]
        W4["pattern_boost × 0.10"]
    end

    subgraph Floor ["Floor Rule"]
        FR{"rule_score ≥ 70?"}
        YES["combined = max(combined, 70)"]
        NO["Keep combined"]
    end

    subgraph AI ["AI Blend"]
        AIW["combined × 0.6 + AI_score × 0.4"]
    end

    subgraph Verdict ["Verdict Mapping"]
        V1["0-14 → Safe"]
        V2["15-34 → Low Risk"]
        V3["35-59 → Medium Risk"]
        V4["60-79 → High Risk"]
        V5["80-100 → Critical"]
    end

    RS --> W1 --> FR
    PS --> W2 --> FR
    US --> W3 --> FR
    PB --> W4 --> FR

    FR -->|Yes| YES --> AIW
    FR -->|No| NO --> AIW

    AIW --> V1
    AIW --> V2
    AIW --> V3
    AIW --> V4
    AIW --> V5
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph Users ["Users"]
        Browser[Browser]
        Mobile[Mobile Browser]
    end

    subgraph Vercel ["Vercel — Frontend"]
        FE[Next.js 16<br/>trustlens-ai.vercel.app]
    end

    subgraph Render ["Render — Backend"]
        BE[Docker Container<br/>FastAPI + EasyOCR]
        HEALTH[/health endpoint]
    end

    subgraph External ["External Services"]
        MDB[(MongoDB Atlas<br/>Cluster0)]
        NIM[NVIDIA NIM API<br/>Nemotron 49B]
    end

    Browser --> FE
    Mobile --> FE
    FE -->|API calls| BE
    BE -->|auth + data| MDB
    BE -->|AI analysis| NIM
    HEALTH -->|30s check| BE
```

---

## Docker Build Pipeline

```mermaid
graph LR
    subgraph Builder ["Builder Stage"]
        BASE1[python:3.11.9-slim]
        SYS1[libgl1, libglib2.0-0<br/>libffi-dev, libssl-dev]
        REQ[requirements.txt]
        INSTALL[pip install]
    end

    subgraph Runtime ["Runtime Stage"]
        BASE2[python:3.11.9-slim]
        SYS2[libgl1, libglib2.0-0<br/>libffi8, curl]
        PKGS[site-packages<br/>from builder]
        CODE[backend/ + datasets/]
        USER[appuser]
        CMD[uvicorn backend.app:app<br/>--port 8000]
    end

    BASE1 --> SYS1 --> REQ --> INSTALL --> PKGS
    BASE2 --> SYS2 --> PKGS
    CODE --> USER --> CMD
```

---

## Component Map

```mermaid
graph TB
    subgraph Frontend ["Frontend Components"]
        AppShell[AppShell<br/>auth guard]
        UploadBox[UploadBox<br/>3-tab input]
        RiskMeter[RiskMeter<br/>circular gauge]
        VerdictCard[VerdictCard<br/>verdict display]
        ConfidenceBar[ConfidenceBar<br/>bar chart]
        ActionGuide[ActionGuide<br/>emergency steps]
        ScamCategory[ScamCategory<br/>category badge]
    end

    subgraph Backend ["Backend Modules"]
        app.py[app.py<br/>FastAPI entry]
        config[config.py<br/>settings]
        auth[auth.py<br/>JWT]
        message[message.py<br/>text scan]
        url[url.py<br/>URL scan]
        screenshot[screenshot.py<br/>image scan]
    end

    subgraph Detection ["Detection Engines"]
        phrase[phrase_matcher.py<br/>200+ phrases]
        rule[rule_engine.py<br/>15 rules]
        urldet[url_detector.py<br/>phishing]
        domain[domain_checker.py<br/>reputation]
        pattern[pattern_analyzer.py<br/>social eng]
        scam[scam_classifier.py<br/>13 categories]
    end

    UploadBox -->|API calls| message
    UploadBox -->|API calls| url
    UploadBox -->|API calls| screenshot
    message --> phrase
    message --> rule
    message --> pattern
    message --> scam
    url --> urldet
    url --> domain
    url --> rule
    screenshot --> phrase
    screenshot --> rule
```
