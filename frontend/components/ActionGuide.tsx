"use client";

import type { ActionStep, RiskLevel } from "@/types";

interface ActionGuideProps {
  actions?: (ActionStep | string)[];
  confidenceScore?: number;
  verdict?: RiskLevel | string;
  onDownload?: () => void;
  onDismiss?: () => void;
}

const severityStyles: Record<string, { bg: string; text: string }> = {
  error: { bg: "bg-[#ffb4ab]/15", text: "text-[#ffb4ab]" },
  primary: { bg: "bg-[#4d8eff]/15", text: "text-[#adc6ff]" },
  tertiary: { bg: "bg-[#ffb786]/15", text: "text-[#ffb786]" },
};

export default function ActionGuide({
  actions = [],
  confidenceScore = 95,
  verdict = "Safe",
  onDownload,
  onDismiss,
}: ActionGuideProps) {
  // Normalize string actions into ActionStep objects if necessary
  const normalizedSteps: ActionStep[] = actions.map((act, idx) => {
    if (typeof act === "string") {
      let severity: "primary" | "tertiary" | "error" = "primary";
      if (act.includes("DO NOT") || act.includes("NEVER") || act.includes("🚨")) {
        severity = "error";
      } else if (act.includes("⚠️") || act.includes("Block")) {
        severity = "tertiary";
      }
      return {
        step: idx + 1,
        title: act.split(".")[0] || `Step ${idx + 1}`,
        description: act,
        severity,
      };
    }
    return act;
  });

  return (
    <div className="glass-panel rounded-2xl p-6 md:p-8 bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
      <h4 className="font-[family-name:var(--font-manrope)] font-semibold text-lg text-[#d8e3fb] mb-6 flex items-center gap-2">
        <span className="material-symbols-outlined text-[#6bd8cb] text-xl">
          security_update_good
        </span>
        Recommended Safety Actions
      </h4>

      {/* Action steps grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {normalizedSteps.map((action) => {
          const style = severityStyles[action.severity] ?? severityStyles.primary;
          return (
            <div
              key={action.step}
              className="flex gap-4 p-4 bg-[#152031] rounded-xl border border-white/5 hover:border-[#6bd8cb]/20 transition-all duration-200 group"
            >
              {/* Step number badge */}
              <div
                className={`w-10 h-10 shrink-0 rounded-full ${style.bg} ${style.text} flex items-center justify-center font-bold text-sm`}
              >
                {action.step}
              </div>

              <div>
                <h5 className="font-[family-name:var(--font-manrope)] font-semibold text-[#d8e3fb] mb-1 group-hover:text-[#6bd8cb] transition-colors text-sm">
                  {action.title}
                </h5>
                <p className="text-[#8c909f] text-xs leading-relaxed">
                  {action.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer row */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-t border-white/5 pt-6">
        <p className="text-[#8c909f] text-sm max-w-md leading-relaxed">
          TrustLens AI Engine is active. Threat analysis carries{" "}
          <span className="text-[#6bd8cb] font-semibold">{Math.round(confidenceScore * 100)}% confidence</span>. Always verify unverified financial requests.
        </p>

        <div className="flex gap-3 shrink-0">
          {onDownload && (
            <button
              id="download-report-btn"
              onClick={onDownload}
              className="px-6 py-2.5 rounded-full border border-[#8c909f] text-[#d8e3fb] text-sm font-semibold hover:bg-[#2a3548] active:scale-95 transition-all duration-200"
            >
              Download Report
            </button>
          )}
          {onDismiss && (
            <button
              id="dismiss-threat-btn"
              onClick={onDismiss}
              className="px-6 py-2.5 rounded-full bg-[#adc6ff] text-[#002e6a] text-sm font-bold hover:bg-[#bdd0ff] active:scale-95 transition-all duration-200"
            >
              Dismiss Threat
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
