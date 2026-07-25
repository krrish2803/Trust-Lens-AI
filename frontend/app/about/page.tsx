"use client";

import AppShell from "@/components/AppShell";

export default function AboutPage() {
  return (
    <AppShell>
      <div className="max-w-4xl mx-auto space-y-10 py-6">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold uppercase tracking-widest">
            Mission & Architecture
          </div>
          <h1 className="text-4xl font-extrabold text-white tracking-tight">About TrustLens AI</h1>
          <p className="text-slate-400 max-w-2xl mx-auto leading-relaxed text-base">
            TrustLens AI is a next-generation scam & phishing detection platform specifically engineered for Indian digital users to safeguard against financial fraud, fake KYC alerts, digital arrests, and malicious links.
          </p>
        </div>

        {/* 8-Layer Architecture Grid */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 md:p-8 backdrop-blur-xl space-y-6">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <span className="text-cyan-400">⚡</span> 8-Layer Defense Architecture
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 1: Hinglish Scam Library</h3>
              <p className="text-xs text-slate-400 mt-1">200+ localized Hinglish phrase patterns covering OTP, KYC, bank alerts, and prize claims.</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 2: 10-Category Rule Engine</h3>
              <p className="text-xs text-slate-400 mt-1">Deterministic rule matching for OTP, KYC, UPI, Banks, Delivery, Investment, Job, Loan, Govt, and Lottery scams.</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 3: URL & Domain Analyzer</h3>
              <p className="text-xs text-slate-400 mt-1">Deep inspection of IP links, URL shorteners, typosquatting, fake TLDs, and SSL certificates.</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 4: EasyOCR Image Engine</h3>
              <p className="text-xs text-slate-400 mt-1">Optical Character Recognition for text extraction from WhatsApp screenshots and payment app receipts.</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 5: NVIDIA AI Analysis</h3>
              <p className="text-xs text-slate-400 mt-1">LLM threat classification powered by NVIDIA NIM (Llama-3.3-70B-Instruct).</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 6: Risk Scoring Engine</h3>
              <p className="text-xs text-slate-400 mt-1">Weighted 0-100 risk score categorization (Safe, Low, Medium, High, Critical).</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 7: Explainability Engine</h3>
              <p className="text-xs text-slate-400 mt-1">Generates clear bulleted rationale explaining why content was flagged.</p>
            </div>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
              <h3 className="text-sm font-semibold text-cyan-400">Layer 8: Action Recommendation</h3>
              <p className="text-xs text-slate-400 mt-1">Provides immediate emergency steps (Block sender, call 1930 Cyber Crime Helpline).</p>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
