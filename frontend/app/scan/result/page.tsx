"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import RiskMeter from "@/components/RiskMeter";
import VerdictCard from "@/components/VerdictCard";
import ActionGuideWrapper from "@/components/ActionGuideWrapper";
import { ScanResultResponse } from "@/types";
import { getScanById } from "@/services/api";

function ScanResultContent() {
  const searchParams = useSearchParams();
  const scanId = searchParams.get("id");

  const [result, setResult] = useState<ScanResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check localStorage first for instant render
    const cached = localStorage.getItem("lastScanResult");
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (!scanId || parsed.id === scanId) {
          setResult(parsed);
          setLoading(false);
          return;
        }
      } catch {
        // Cached data is corrupted, fall through to API fetch
      }
    }

    if (scanId) {
      getScanById(scanId)
        .then((res) => {
          setResult(res);
        })
        .catch(() => {
          setError("Failed to load scan result. Please try again.");
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [scanId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mb-4" />
        <p className="text-slate-400 text-sm animate-pulse">Loading Threat Intelligence Analysis...</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="max-w-xl mx-auto text-center py-16 space-y-4">
        <div className="text-5xl">🔍</div>
        <h2 className="text-2xl font-bold text-white">
          {error || "No Scan Result Selected"}
        </h2>
        <p className="text-slate-400 text-sm">
          {error ? "Please try submitting again." : "Please submit a URL, message, or screenshot to generate a new threat analysis report."}
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 uppercase tracking-widest mb-1">
            <span>Scan ID: {result.id}</span>
            <span>•</span>
            <span>{result.scan_type.toUpperCase()}</span>
          </div>
          <h1 className="text-3xl font-bold text-white">Threat Intelligence Analysis</h1>
        </div>
        <div className="text-xs text-slate-500 font-mono">
          Scanned: {new Date(result.created_at).toLocaleString()}
        </div>
      </div>

      {/* Top Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Risk Meter Card */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col items-center justify-center backdrop-blur-xl">
          <RiskMeter score={result.risk_score} />
        </div>

        {/* Verdict Card */}
        <div className="md:col-span-2">
          <VerdictCard
            verdict={result.verdict}
            category={result.scam_category}
            confidence={result.confidence_score}
            summary={result.input_summary}
          />
        </div>
      </div>

      {/* AI Explanation & Reasons */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 md:p-8 backdrop-blur-xl space-y-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <span className="text-cyan-400">🧠</span> AI Threat Rationale & Explanation
        </h3>
        <p className="text-slate-300 leading-relaxed text-sm md:text-base bg-slate-950/80 p-4 rounded-xl border border-slate-800/80 font-sans">
          {result.ai_explanation || "Content passed through multi-layer verification rules."}
        </p>

        {result.reasons && result.reasons.length > 0 && (
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Detected Threat Indicators</h4>
            <ul className="space-y-2">
              {result.reasons.map((reason, i) => (
                <li key={i} className="flex items-start gap-2.5 text-sm text-slate-300">
                  <span className="text-red-400 mt-0.5">⚠️</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.matched_phrases && result.matched_phrases.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Matched Hinglish Scam Phrases</h4>
            <div className="flex flex-wrap gap-2">
              {result.matched_phrases.map((phrase, i) => (
                <span key={i} className="px-3 py-1 bg-red-500/10 border border-red-500/30 rounded-lg text-xs font-medium text-red-300">
                  "{phrase}"
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Action Recommendation Guide */}
      <ActionGuideWrapper
        actions={result.recommended_actions}
        confidenceScore={result.confidence_score}
      />
    </div>
  );
}

export default function ScanResultPage() {
  return (
    <Suspense fallback={
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mb-4" />
        <p className="text-slate-400 text-sm">Loading Scan Result...</p>
      </div>
    }>
      <ScanResultContent />
    </Suspense>
  );
}
