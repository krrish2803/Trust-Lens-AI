# TrustLens AI User Guide & Operations Manual

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Quality Assurance & Technical Writing Lead  
**Date:** July 25, 2026  
**Document Status:** Published Operations Manual  

---

## 1. Introduction & Overview

Welcome to **TrustLens AI**, your personal AI security assistant engineered to shield Indian citizens from digital financial fraud, UPI scams, fake KYC alerts, and phishing traps.

This User Guide provides step-by-step instructions on how to operate TrustLens AI, analyze suspicious messages and links, interpret risk scores, and execute emergency protection procedures.

---

## 2. Navigating the TrustLens AI Dashboard

The TrustLens AI user interface consists of four primary sections:

1. **Header Navigation:** Access **Home / Scanner**, **Live Threat Map**, **Report Scam**, and **User History**.
2. **Multi-Input Scanner Box:** Central input area supporting Text/SMS input, URL link checking, and Screenshot Image upload.
3. **Risk Analysis Results Card:** Displays overall Risk Level (Safe, Low, Medium, High, Critical), Confidence Percentage, and Scam Category.
4. **Explainability & Emergency Action Panel:** Plain-language breakdown of detected threats with step-by-step action guides.

---

## 3. How to Perform a Scam Scan

### 3.1 Method A: Analyzing SMS / WhatsApp Text Messages

1. **Copy Message:** Copy the suspicious SMS or WhatsApp message from your phone.
2. **Paste into Scanner:** Navigate to [http://localhost:3000](http://localhost:3000), paste the text into the main text input area.
3. **Click "Analyze Threat":** Click the **Analyze Threat** button.
4. **View Verdict:** Within 1-2 seconds, TrustLens AI displays the risk assessment breakdown.

*Example Input:* `"Aapka SBI account block ho gaya hai, turant KYC update karo http://sbi-verify.com"`  
*Output:* **HIGH RISK** (Category: Fake KYC Scam).

---

### 3.2 Method B: Checking Suspicious Web Links / URLs

1. **Select "URL Scanner" Tab:** Switch to the URL tab in the input box.
2. **Enter Web Address:** Enter or paste the web link (e.g., `http://paytm-cashback-claim.xyz`).
3. **Click "Scan Link":** TrustLens AI checks the domain against whitelist registries, suspicious TLDs, and domain squatting databases.
4. **Review Result:** TrustLens AI will inform you whether the domain is an official verified website or a dangerous phishing site.

---

### 3.3 Method C: Uploading Payment Receipts or Chat Screenshots (OCR)

1. **Select "Screenshot OCR" Tab:** Click the Image Upload tab or drag-and-drop a screenshot file (`.png`, `.jpg`, `.jpeg`).
2. **Upload File:** Select a screenshot of a suspicious payment receipt, WhatsApp chat, or scratch card.
3. **Automatic Extraction:** TrustLens AI's OCR engine automatically extracts text from the image and runs full multi-layer detection.
4. **Review Results:** Inspect the extracted text alongside the security verdict.

---

## 4. Understanding Risk Verdicts & Color Codes

TrustLens AI classifies inputs into 5 distinct Risk Levels:

| Risk Level | Color Code | Risk Score Range | Recommended User Action |
| :--- | :--- | :--- | :--- |
| **SAFE** | 🟢 Green | `0.00 - 0.19` | **Approved:** Message/URL is from a verified official source. Safe to proceed. |
| **LOW** | 🔵 Blue | `0.20 - 0.44` | **Monitor:** Low risk indicators. Verify sender details before sharing information. |
| **MEDIUM** | 🟡 Yellow | `0.45 - 0.64` | **Caution:** Suspicious patterns found. Do not click links or share details. |
| **HIGH** | 🟠 Orange | `0.65 - 0.84` | **Warning:** Strong scam indicators flagged. Do not enter passwords or transfer money. |
| **CRITICAL** | 🔴 Red | `0.85 - 1.00` | **BLOCK:** Confirmed malicious scam. Immediately block sender and report to 1930. |

---

## 5. Step-by-Step Emergency Action Guide

When TrustLens AI flags a **HIGH** or **CRITICAL** risk threat, follow these immediate protection steps:

### If You Received a Fake UPI Collect / Reverse QR Request:
1. **DO NOT Enter UPI PIN:** Remember, entering a UPI PIN ALWAYS deducts money from your account.
2. **Decline Collect Request:** Decline the pending payment request inside Google Pay / PhonePe / Paytm.
3. **Block Sender:** Block the phone number on WhatsApp / OLX / Call log.

### If You Already Shared an OTP or Netbanking Password:
1. **Call Bank Toll-Free Number Immediately:** Call your bank's official card blocking helpline (number listed on back of debit card).
2. **Freeze Account:** Request the bank executive to temporarily freeze netbanking and block debit/credit cards.
3. **Report to Cyber Crime Cell:** Dial national cybercrime helpline **1930** or register complaint on [cybercrime.gov.in](https://cybercrime.gov.in).

---

## 6. Community Scam Reporting

Help protect fellow citizens by reporting newly discovered scam messages:

1. Click **"Report Scam"** in the top navigation bar.
2. Paste the scam message text or upload screenshot evidence.
3. Select scam category (e.g., Job Scam, UPI Scam).
4. Click **"Submit Report"**. Our security team validates and adds verified patterns to the Hinglish dataset.

---

*User Guide certified by Quality Assurance & Product Operations.*
