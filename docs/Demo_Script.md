# TrustLens AI Pitch & Live Demo Scripts

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Presentation & Demo Lead  
**Date:** July 25, 2026  
**Document Status:** Hackathon Stage-Ready  

---

## Part 1: 3-Minute Live Product Demo Script

**Target Duration:** Exactly 180 seconds  
**Presenter Roles:** Presenter 1 (Storyteller / Hook) & Presenter 2 (Live Screen Driver)

---

### Time: 0:00 - 0:30 (The Hook & Real-World Problem)

**(Presenter 1):**  
"Good evening judges! Last month, Ramesh, a 54-year-old school teacher from Jaipur, received an SMS: *'Aapka SBI account block ho gaya hai, turant KYC update karein.'* Panic-stricken, Ramesh clicked the link, entered his OTP, and within 4 minutes lost 1.2 Lakh Rupees—his entire monthly pension savings. 

Every single day in India, over 4,000 citizens fall victim to digital fraud—ranging from reverse UPI QR codes on OLX to fake KBC lottery WhatsApp audio clips. Existing antivirus tools block malware files, but they don't understand **Hinglish social engineering**. 

That is why we built **TrustLens AI**. Tagline: **Detect. Explain. Protect.**"

---

### Time: 0:30 - 1:30 (Live Product Demonstration)

**(Presenter 2 shares screen showing TrustLens AI Web Dashboard):**

**Demo Scenario 1: Hinglish Bank Threat & Phishing Link**
"Let's take Ramesh's exact message and paste it into TrustLens AI:  
`'Aapka SBI account block ho gaya hai, turant KYC update karo http://sbi-verify.com'`

Watch what happens when I click **Analyze Threat**. 

In less than 1 second, TrustLens AI returns a **CRITICAL RISK** alert with a 92% confidence score! Notice how our system doesn't just give a raw score—it breaks down the threat into 4 transparent layers:
1. **Phrase Matcher:** Identifies the classic Hinglish threat pattern: *'account block ho gaya'*.
2. **Rule Engine:** Triggers 3 security heuristics—Urgency, Brand Impersonation, and Account Threat.
3. **URL Detector:** Identifies `sbi-verify.com` as a spoofed domain squatting domain.
4. **Explainability Engine:** Explains in plain Hindi/English: *'SBI will never ask for KYC updates via external SMS links.'*"

---

**Demo Scenario 2: Reverse UPI QR Code Fraud (Screenshot OCR)**
"Now let's look at another epidemic: **OLX UPI Fraud**. 
A scammer sends a buyer a screenshot saying: *'Scan this QR code on PhonePe to receive your 15,000 Rs advance deposit.'*

I drag and drop the chat screenshot directly into our **Screenshot OCR** scanner. 

Our Tesseract engine extracts the text from the image, and TrustLens AI immediately alerts: **CRITICAL RISK — REVERSE UPI FRAUD**. 

It displays our core defense rule in bold red:  
⚠️ **'UPI PIN is ONLY required to SEND money, NEVER to RECEIVE money!'**"

---

### Time: 1:30 - 2:30 (Technical Innovation & Core Architecture)

**(Presenter 1):**  
"Under the hood, TrustLens AI is powered by:
- **A 210-Entry Hinglish Scam Phrase Dataset** covering 14 Indian scam vectors (OTP, UPI, Fake KYC, Cyber Arrest, Delivery, Job Scams).
- **A 15-Rule Security Engine** with negative advisory safeguards so official bank SMS alerts are never falsely flagged.
- **Multi-Layer Risk Scoring Engine** combining weighted NLP, heuristic, and URL intelligence.
- **FastAPI Python Microservices** running under 200ms latency paired with a Next.js 16 frontend."

---

### Time: 2:30 - 3:00 (Impact & Call to Action)

**(Presenter 1):**  
"TrustLens AI is not just a hackathon prototype—it is a production-tested security shield. All 28 unit and integration test cases in our test suite pass with 100% precision. 

With TrustLens AI, we are turning confusion into clarity and protecting millions of Indian smartphone users from losing their hard-earned money. 

Thank you, and we are ready for your questions!"

---

---

## Part 2: 5-Minute Comprehensive Pitch Demo Script

**Target Duration:** 300 seconds  
**Context:** Slide Pitch Presentation + Live Interactive Demo

---

### Section 1: Problem & Market Opportunity (1 minute)
- **Slide 1 - Title:** TrustLens AI: Detect. Explain. Protect.
- **Slide 2 - The Crisis:** 75% of Indian cybercrimes are financial fraud. Rs 7,000+ Crore lost annually to digital scamming.
- **Key Insight:** Scammers target psychology, not software vulnerabilities. They exploit language nuances in Hinglish (e.g., *"Paise paane ke liye PIN dalo"*).

### Section 2: The Solution & Live Product Demo (2 minutes)
- **Slide 3 - Product Architecture:** Multi-layer security stack combining NLP, Heuristics, URL Intelligence, and OCR.
- **Live Demo Execution:**
  - Demonstrate SMS scam scan.
  - Demonstrate URL phishing detector on typosquatting domain (`http://paytm-cashback-claim.xyz`).
  - Demonstrate Screenshot OCR analysis on fake KBC cheque image.
  - Highlight plain-language explainability and step-by-step action guides.

### Section 3: Technical Validation & Competitive Advantage (1 minute)
- **Slide 4 - Technical Excellence:**
  - 210 Verified Hinglish scam phrases dataset.
  - Zero false positive rate on official bank domain whitelists (`sbi.co.in`, `hdfcbank.com`).
  - 100% pass rate across 28 automated test suite cases.
- **Slide 5 - Competitive Matrix:**

| Feature | Generic Antivirus | Chrome Safe Browsing | TrustLens AI |
| :--- | :---: | :---: | :---: |
| **Hinglish Scam Phrase Understanding** | ❌ No | ❌ No | ✅ **210+ Phrases** |
| **Reverse UPI Fraud Detection** | ❌ No | ❌ No | ✅ **Native** |
| **Screenshot Receipt OCR** | ❌ No | ❌ No | ✅ **Built-in** |
| **Plain-Language Explainability** | ❌ No | ❌ Technical URL alert | ✅ **Actionable Advice** |

### Section 4: Business Model & Roadmap (1 minute)
- **Slide 6 - Go-To-Market & Integration:**
  - B2C Free Web & WhatsApp Bot Assistant.
  - B2B Enterprise API for Banking & E-Commerce Apps (preventing fraud before payment gateway execution).
  - Direct Integration with I4C (1930 Cyber Crime Reporting Portal).
- **Slide 7 - Conclusion:** Call to action & Q&A invitation.

---

*Demo scripts certified stage-ready by Presentation Lead.*
