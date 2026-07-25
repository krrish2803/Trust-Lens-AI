# Comprehensive Research Report: Indian Cyber Scams & Phishing Patterns

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Research, Technical Writing & Quality Assurance Lead  
**Date:** July 25, 2026  
**Document Status:** Complete & Verified  

---

## Executive Summary

Digital financial fraud in India has scaled exponentially following the rapid adoption of Unified Payments Interface (UPI), smartphone penetration, and digital banking services. According to empirical data from the Indian Cyber Crime Coordination Centre (I4C) and National Cyber Crime Reporting Portal (NCPCR), financial cyber fraud accounts for over 75% of reported cybercrime complaints in India.

This research report provides an authoritative analysis of 14 dominant Indian cyber scam vectors. Each scam section includes verified operational mechanics, common Hinglish and English phishing phrases, victim demographics, psychological warning signs, and actionable prevention protocols.

---

## 1. OTP Scams (One-Time Password Theft)

### Scam Name
OTP Theft & Social Engineering Fraud

### How It Works
Scammers impersonate bank officials, e-commerce representatives, or telecom support agents over voice calls (vishing) or messages (smishing). They inform victims about account blocking, suspicious debit, or pending updates, inducing urgency. They request the victim to read back or forward the 6-digit OTP sent to their mobile device. The OTP is then used to complete unauthorized card transactions, reset banking passwords, or initiate SIM swaps.

### Common Phrases
- "Apna OTP bhejo verification ke liye turant"
- "Wrong OTP chala gaya aapko, galti se padh ke bata do"
- "Card unblock karne ke liye 6-digit code share karein"
- "Refund process karne ke liye phone par aaya SMS read karein"

### Target Audience
Senior citizens, non-tech savvy rural/semi-urban internet users, online shoppers.

### Warning Signs
- Direct request for OTP over voice call or SMS reply.
- Artificial time pressure ("account will be closed in 10 minutes").
- Refusal by the caller to provide official bank employee credentials.

### Prevention Tips
- Never share OTPs, PINs, or passwords with anyone under any circumstances.
- Banks explicitly state they never request OTPs over call or chat.
- Set up SIM lock and transaction limits on banking applications.

---

## 2. UPI Scams (Unified Payments Interface Fraud)

### Scam Name
UPI Collect Request & Reverse QR Code Fraud

### How It Works
Scammers exploit the common misconception that receiving money requires entering a UPI PIN. On marketplaces like OLX or Quikr, scammers pose as buyers (often claiming to be Indian Army officers or defense personnel to build trust). They send a UPI 'Collect Money' request or a payment QR code image, instructing the victim to scan the QR code or enter their UPI PIN to "receive advance money". Once the PIN is entered, funds are immediately debited from the victim's bank account.

### Common Phrases
- "Paisa paane ke liye UPI PIN enter karein"
- "Google Pay par Rs 10,000 receive ka notification aya hai, PIN dalo"
- "Army officer hu, canteen goods purchase ke liye UPI payment accept karo"
- "Scan this QR code image to receive booking deposit"

### Target Audience
Online secondhand marketplace sellers, small business owners, festival shoppers.

### Warning Signs
- Requirement to enter UPI PIN or scan QR code when receiving funds.
- Buyer overpaying or offering advance payment without physically seeing goods.
- Pushy behavior urging immediate app authorization.

### Prevention Tips
- **Core Rule of UPI:** Entering UPI PIN is ONLY required to SEND money, never to RECEIVE money.
- Scanning a QR code ALWAYS deducts money from your account.
- Verify buyer credentials before initiating transaction workflow.

---

## 3. Fake KYC Scams (Know Your Customer Verification Fraud)

### Scam Name
Fake KYC Verification & Account Suspension Fraud

### How It Works
Victims receive SMS or WhatsApp alerts stating that their bank account, Paytm wallet, Aadhaar link, or SIM card KYC has expired. The message warns of immediate account freezing within 24 hours and includes a link to a phishing website or an APK file. Entering credentials on the phishing site or installing the APK allows scammers to harvest bank details, identity numbers, and SMS logs.

### Common Phrases
- "Aapka SBI account KYC update ke bina 24 ghante me block ho jayega"
- "Paytm KYC expire ho chuka hai, niche diye link par Aadhaar verify karein"
- "Jio SIM KYC suspended. Call customer care immediately"
- "Download HDFC_KYC_Update.apk file to update details"

### Target Audience
Bank account holders, e-wallet users, senior citizens managing pensions.

### Warning Signs
- Shortened URLs or unofficial web domains (e.g., `sbi-kyc-verify.top`).
- Request to download `.apk` files directly over chat apps.
- Threats of immediate disconnection within tight window.

### Prevention Tips
- Complete KYC updates strictly inside verified mobile apps or physical bank branches.
- Never install APK files downloaded from WhatsApp, Telegram, or SMS links.
- Check bank communication domain headers (e.g., `AD-SBIBNK`).

---

## 4. Bank Impersonation Scams

### Scam Name
Financial Institution Impersonation & Security Alarm Fraud

### How It Works
Fraudsters send SMS, emails, or make IVR calls pretending to be representatives of major Indian banks (SBI, HDFC, ICICI, Axis). They report unauthorized debit transactions, international card usage, or expiring reward points. They prompt victims to click a link to cancel the charge or speak with an agent, who then extracts netbanking user IDs, passwords, card CVVs, and OTPs.

### Common Phrases
- "Dear customer, your netbanking is suspended due to suspicious login"
- "Aapke credit card par Rs 9,999 charge hua hai, cancel karne ke liye 1 dabayein"
- "Upgrade your credit card to Lifetime Free Super Premium without charges"
- "RBI Fraud Department notice: Submit your account audit form"

### Target Audience
Credit card holders, salaried employees, online netbanking users.

### Warning Signs
- Generic salutations ("Dear Customer" instead of your registered name).
- Callers requesting 16-digit card numbers, CVV, or passwords.
- Unofficial sender email addresses (e.g., `@gmail.com` or `@outlook.com`).

### Prevention Tips
- Cross-check bank communications using official customer care numbers on physical debit/credit cards.
- Never enter banking credentials on websites accessed via external links.
- Enable multi-factor authentication (MFA) and transaction notifications.

---

## 5. Delivery Scams (Smishing & Postal Fraud)

### Scam Name
Failed Parcel Delivery & Customs Seizure Fraud

### How It Works
Scammers send SMS messages pretending to be India Post, BlueDart, or Delhivery, stating that a package cannot be delivered due to an incomplete address or unpaid Rs 25 redelivery fee. Clicking the link takes the victim to a phishing portal where entering credit/debit card details to pay the small fee results in full card compromise. A high-risk variant involves claims that a parcel under the victim's name was seized at airport customs containing illegal narcotics (FedEx Cyber Arrest scam).

### Common Phrases
- "India Post: Aapka parcel address incomplete hone ki wajah se deliver nahi ho saka"
- "Courier delivery hold notice: Pay Rs 25 redelivery charge immediately"
- "BlueDart Parcel containing illegal items seized by Customs at Mumbai Airport"
- "Your Flipkart gift package is arriving! Pay Rs 99 handling fee"

### Target Audience
E-commerce shoppers, international students, general public.

### Warning Signs
- Unsolicited delivery SMS containing non-official URLs (e.g., `.top`, `.xyz`).
- Demands for small money payments via credit card to re-route parcels.
- Video calls from people in fake police uniforms claiming customs arrests.

### Prevention Tips
- Track packages directly through official courier apps or official websites.
- Customs and law enforcement agencies never conduct arrests or monetary settlements over Skype/WhatsApp video calls.
- Avoid clicking package redirection links in SMS.

---

## 6. Job & Internship Scams

### Scam Name
Work From Home Task Scam & Pre-paid Registration Fraud

### How It Works
Offers for work-from-home jobs, YouTube video liking, or data entry typing tasks are circulated via WhatsApp or Telegram. Initially, victims are paid small payouts (Rs 150-Rs 500) to build trust. Subsequently, victims are added to VIP Telegram groups and instructed to deposit "pre-paid task investment money" to earn 50% commission. Once high amounts (Rs 50,000+) are deposited, scammers block withdrawals, demanding additional "tax release payments."

### Common Phrases
- "Part-time job offer: Like YouTube videos and earn Rs 3,000 to Rs 5,000 daily"
- "Amazon Data Entry job confirmed! Pay Rs 1,500 registration fee"
- "Telegram VIP Prepaid Task Group: Deposit Rs 10,000 for high commission"
- "Typing job agreement penalty notice: Pay Rs 25,000 court fee"

### Target Audience
College students, unemployed youth, homemakers seeking part-time income.

### Warning Signs
- Offers of lucrative pay for trivial tasks (liking posts, rating hotels).
- Demands for upfront "registration fees," "equipment deposits," or "prepaid task deposits."
- Recruitment conducted entirely over WhatsApp or Telegram without formal interviews.

### Prevention Tips
- Legitimate employers never ask candidates to pay money for job offers.
- Verify company registration on the Ministry of Corporate Affairs (MCA) portal.
- Reject offers promising guaranteed daily returns for social media engagements.

---

## 7. Loan Scams (Predatory Loan Apps & Advance Fee Fraud)

### Scam Name
Instant Loan Approval & Predatory Loan App Extortion

### How It Works
Scammers offer instant zero-CIBIL personal loans or government Mudra loans via SMS or unverified Android APKs. In advance fee schemes, victims are asked to pay processing fees, GST, or file charges prior to loan disbursement. In predatory loan app schemes, malicious APKs access the victim's phone contact list, media gallery, and SMS logs. The app disburses a small amount (e.g., Rs 3,000), and after 6 days demands Rs 10,000, threatening to send morphed photos to the victim's contacts if unpaid.

### Common Phrases
- "Instant Personal Loan of Rs 5,00,000 approved! Pay Rs 3,500 processing charge"
- "Pardhan Mantri Mudra Yojana Loan approved! Transfer GST Rs 4,999"
- "Zero CIBIL score required personal loan! Install QuickCash.apk"
- "Loan EMI overdue: Morphing picture police case threat sent to family"

### Target Audience
Financially stressed individuals, small vendors, college students.

### Warning Signs
- Instant loan offers without credit checks or income verification.
- Requirement to pay money upfront before receiving loan disbursement.
- Mobile loan apps requiring access to full contact list, gallery, and SMS.

### Prevention Tips
- Borrow only from RBI-registered Banks and Non-Banking Financial Companies (NBFCs).
- Verify lender registration on the RBI Sachet portal.
- Never grant contact list or gallery permissions to financial mobile apps.

---

## 8. Lottery & Prize Scams

### Scam Name
KBC Lottery Fraud & Fake Contest Winner Schemes

### How It Works
Victims receive WhatsApp audio messages, fake cheque images, or postal scratch cards claiming they have won 25 Lakh Rupees in the "KBC SIM Card Lucky Draw" or a brand-new Mahindra Thar car. To claim the prize, victims are asked to transfer money under the guise of processing fees, RTO registration tax, or GST into scammer-controlled accounts.

### Common Phrases
- "Congratulations! KBC Sim Card Lucky Draw me aapne 25 Lakh Jeete hain"
- "Aapko Mahindra Thar car prize me mili hai, RTO tax Rs 12,500 jama kijiye"
- "Scratch Coupon Winner! Claim Rs 75,000 cash prize after TDS fee"
- "Jio 10th Anniversary Offer: Free 3 Months 5G Recharge click link"

### Target Audience
Rural populations, low-income households, senior citizens.

### Warning Signs
- Winning a lottery or contest you never entered.
- Demand to deposit advance fees or taxes to release prize money.
- Use of celebrity images (e.g., Amitabh Bachchan) on poorly edited digital banners.

### Prevention Tips
- You cannot win a lottery without purchasing a valid ticket.
- Real contest prizes deduct TDS at source; winners are never asked to deposit tax via UPI.
- Report fake lottery audio clips to national cybercrime handles.

---

## 9. Investment Scams (Pig Butchering & High-Yield Schemes)

### Scam Name
High-Yield Crypto/Stock Investment Fraud (Pig Butchering)

### How It Works
Victims are lured through social media ads or added to WhatsApp/Telegram groups led by fake stock market "professors." Scammers persuade victims to download fake institutional trading apps that show fictitious 300% stock or crypto profits. When victims attempt to withdraw their funds, the platform demands an additional 18% GST or security deposit, ultimately locking the account once victims refuse to pay further.

### Common Phrases
- "Guaranteed 200% returns in 7 days! Join SEBI registered Stock Tips Group"
- "Institutional Trading Account: Buy IPO shares at 50% discount"
- "Bitcoin Cloud Mining Profit: Deposit Rs 5,000 for Rs 500 daily profit"
- "Pay 18% GST tax deposit to release your Rs 5 Lakh investment profit"

### Target Audience
Retail stock investors, IT professionals, retirees seeking passive returns.

### Warning Signs
- Promises of guaranteed, risk-free high returns in short timeframes.
- Instructions to transfer investment funds into individual personal bank accounts.
- Trading apps not listed on official Google Play Store / Apple App Store.

### Prevention Tips
- Check SEBI registration numbers of investment advisors on the official SEBI website.
- Never invest through unverified APKs or links shared in messaging channels.
- Remember: All high market returns carry proportional investment risk.

---

## 10. Fake Customer Support Scams

### Scam Name
Search Engine Helpline Manipulation & Remote Desktop Fraud

### How It Works
When users search Google or Google Maps for customer care numbers of payment apps (PhonePe, Google Pay), airlines, or food delivery services (Swiggy, Zomato), they often find fraudulent numbers posted by scammers. Calling these numbers connects victims to scam agents who instruct them to install remote access applications (AnyDesk, TeamViewer, RustDesk) or open screen-sharing during banking logins.

### Common Phrases
- "Google Pay Helpline: Call 9830XXXXXX for instant refund"
- "Install RustDesk app on your phone so our technical support team can resolve"
- "Swiggy refund request: Open screen sharing and login to your UPI app"
- "IRCTC Ticket Cancellation Refund Helpline: Dial executive mobile number"

### Target Audience
Any user attempting to resolve online transaction or order issues.

### Warning Signs
- Customer support numbers starting with standard 10-digit mobile prefixes (`98xxx`, `99xxx`, `87xxx`).
- Support representative asking you to install screen-sharing software.
- Requests to initiate UPI payments or enter PINs to process refunds.

### Prevention Tips
- Obtain customer support contact numbers strictly from inside verified official apps.
- Never install AnyDesk, TeamViewer, or RustDesk on the instruction of a caller.
- Terminate calls immediately if asked to share your phone screen.

---

## 11. QR Code Scams

### Scam Name
Quishing & Merchant QR Payment Fraud

### How It Works
Scammers target online marketplace sellers or retail shopkeepers by claiming they want to transfer money. They send a QR code image via WhatsApp or present a physical QR sticker, asserting: "Scan this QR code and enter your PIN to credit money into your shop account." Additionally, quishing involves pasting malicious QR code stickers over legitimate public parking meters or restaurant table menus.

### Common Phrases
- "Aapke dukan ke QR code par cashback offer active hai, scan karke PIN dalo"
- "OLX purchase: Scan QR code image on PhonePe to receive advance payment"
- "Public Parking Quick Payment: Scan pasted QR sticker to pay online"
- "Scan QR code to receive government subsidy grant"

### Target Audience
Retail shopkeepers, online sellers, restaurant visitors, EV charging drivers.

### Warning Signs
- Instructions to scan a QR code when expecting to receive money.
- Physical QR code stickers pasted over printed signage on public meters.
- QR codes directing to unverified third-party websites or `.apk` downloads.

### Prevention Tips
- Scanning a QR code is exclusively used to make payments, never to receive them.
- Inspect physical QR signage for tampering or overlay stickers before scanning.
- Verify domain name displayed on phone after scanning any public QR code.

---

## 12. WhatsApp Scams

### Scam Name
Family In Distress & WhatsApp Pink Trojan Fraud

### How It Works
Scammers hack WhatsApp accounts or register new accounts using contact photos downloaded from social media. They message friends and relatives claiming an emergency ("Lost my phone", "Hospital emergency") and demand urgent money transfers. Another major vector is "WhatsApp Pink" or "WhatsApp Gold"—malicious APKs promising pink themes or exclusive features, which once installed silently steal contacts, SMS messages, and auto-forward malware to all contacts.

### Common Phrases
- "Hi Mom/Dad, my phone broke! Temporary number, send Rs 20,000 urgently"
- "WhatsApp Gold Edition free upgrade! Click link to activate status video"
- "WhatsApp verification code forwarded by mistake, please send back code"
- "Video call recording blackmail threat: Pay Rs 10,000 UPI"

### Target Audience
Parents, senior citizens, teenager social media users.

### Warning Signs
- Messages from familiar contacts requesting money via unusual payment handles.
- Links inviting installation of modified WhatsApp versions (.apk files).
- Requests to forward 6-digit WhatsApp registration codes sent via SMS.

### Prevention Tips
- Call the friend/family member directly on their known phone number before sending money.
- Enable Two-Step Verification inside WhatsApp settings.
- Never download unverified WhatsApp mods or third-party APK themes.

---

## 13. Telegram Scams

### Scam Name
Fake Telegram Escrow & Airdrop Bot Scams

### How It Works
Scammers leverage Telegram's anonymity to operate fake P2P crypto escrow bots, pump-and-dump stock channels, and automated clicker task bots. Users are prompted to transfer funds into bot-managed addresses for P2P transactions or pay "gas fees" to claim crypto airdrops. Impersonation of Telegram support admins with fake verification bots is also widely used to steal account session keys.

### Common Phrases
- "Telegram Crypto Pump & Dump: Buy token now before 1000% surge"
- "Telegram Wallet Escrow Bot: Send funds to bot address to complete trade"
- "Earn $100 daily using Telegram Airdrop Clicker Bot (Deposit $10 gas fee)"
- "Telegram Admin: Your account flagged for spam, verify with security bot"

### Target Audience
Crypto enthusiasts, Web3 users, gamers, young investors.

### Warning Signs
- Requests to transfer funds into unofficial automated Telegram bot wallets.
- Direct messages from pseudo Telegram support accounts demanding credentials.
- Unsolicited addition to high-yield investment channels.

### Prevention Tips
- Conduct P2P trades strictly on established, regulated exchange platforms.
- Never pay advance gas fees for unverified Telegram crypto airdrops.
- Restrict Telegram privacy settings to prevent unknown users from adding you to groups.

---

## 14. Social Media Scams

### Scam Name
Deepfake Media Extortion & Business Page Copyright Phishing

### How It Works
On Facebook and Instagram, scammers create sponsored posts offering fake verified blue badges for Rs 499 or send DM notices warning business page owners that their page will be deleted for copyright infringement. Clicking the appeal link leads to a Meta phishing page that steals account admin rights. Advanced social media scams use AI deepfake voice/video cloning of relatives or celebrities to solicit emergency medical donations.

### Common Phrases
- "Instagram Blue Tick Verified Badge for Rs 499! Click link to apply"
- "Facebook Copyright Notice: Your page will be deleted in 24 hrs, appeal link"
- "Deepfake Video: Urgent medical help needed for accident, donate via UPI"
- "Brand Ambassador collab offer: Free luxury watch, pay shipping Rs 299"

### Target Audience
Social media influencers, business page administrators, general users.

### Warning Signs
- Copyright alerts originating from personal user profiles rather than official Meta notification panels.
- Offers of official verified badges via third-party web links.
- Urgent video requests for money without verified voice/video authentication.

### Prevention Tips
- Manage Meta copyright notices solely within Meta Business Suite dashboard.
- Verify emergency calls by asking a personal question only the real individual could answer.
- Never enter social media passwords on external links.

---

## Summary Matrix of Cyber Scam Vectors

| Scam Category | Primary Attack Vector | Psychological Trigger | Primary Loss Risk |
| :--- | :--- | :--- | :--- |
| **OTP Scam** | Vishing / Smishing | Urgency & Fear | Bank Account Drain |
| **UPI Scam** | Marketplace / Collect Request | Greed & Confusion | Instant Direct Debit |
| **Fake KYC** | SMS Phishing / APK | Compliance Fear | Identity Theft & Financial Fraud |
| **Bank Impersonation** | Phishing Email / Call | Trust & Panic | Complete Banking Access Loss |
| **Delivery Scam** | Smishing / Smuggling Fake | Curiosity & Fear | Credit Card Theft & Extortion |
| **Job Scam** | WhatsApp / Telegram | Easy Income Opportunity | High Pre-paid Financial Loss |
| **Loan Scam** | Malicious APK / SMS | Financial Distress | Data Theft & Morphing Extortion |
| **Lottery Scam** | WhatsApp Audio / Cheque | Greed & Euphoria | Pre-paid Tax Loss |
| **Investment Scam** | Fake Trading App | High Return Expectation | Total Savings Wipeout |
| **Fake Support** | Search Engine Result | Helplessness / Confusion | Remote Access Device Control |
| **QR Code Scam** | QR Image / Sticker | Misunderstanding | Direct Merchant Loss |
| **WhatsApp Scam** | Impersonation / Trojan APK | Family Affection | Contact Spreading & Theft |
| **Telegram Scam** | Bot / Channel Signal | Web3 Hype / FOMO | Crypto Wallet Drain |
| **Social Media Scam** | Deepfake / Fake Meta Notice | Vanity & Page Protection | Account Hijacking & Extortion |

---

*Report compiled and validated by TrustLens AI Security Research Group.*
