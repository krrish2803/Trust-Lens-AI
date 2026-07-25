# TrustLens AI - System Architecture

```mermaid
flowchart TD
    User([User Submission]) --> InputType{Input Type?}
    
    InputType -->|URL| Layer3[Layer 3: URL & Domain Analyzer]
    InputType -->|SMS/Text/Email| Layer1[Layer 1: Hinglish Phrase Library]
    InputType -->|Screenshot/Image| Layer4[Layer 4: EasyOCR Extraction]
    
    Layer4 --> Layer1
    Layer1 --> Layer2[Layer 2: 10-Category Rule Engine]
    Layer3 --> Layer2
    
    Layer2 --> Layer5[Layer 5: NVIDIA AI Analysis]
    Layer5 --> Layer6[Layer 6: Weighted Risk Engine]
    
    Layer6 --> Layer7[Layer 7: Explainability Engine]
    Layer7 --> Layer8[Layer 8: Action Recommendation]
    
    Layer8 --> Output([Risk Score + Verdict + Actions])
```

## Component Breakdown

1. **FastAPI REST API**: High-performance asynchronous API layer built on Pydantic v2 validation models.
2. **Hinglish Scam Phrase Library**: Fuzzy string matching dataset trained on real-world Indian phishing messages.
3. **EasyOCR Pipeline**: Preprocesses images (CLAHE contrast & binarization) to extract text from WhatsApp chats and UPI receipts.
4. **NVIDIA NIM LLM**: Connects asynchronously to `meta/llama-3.3-70b-instruct` for deep context classification.
5. **Motor MongoDB Layer**: Async document persistence for scan history, reports, and audit logs.
