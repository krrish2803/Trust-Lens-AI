import VerdictCard from "@/components/VerdictCard";
import RiskMeter from "@/components/RiskMeter";
import ConfidenceBar from "@/components/ConfidenceBar";
import ScamCategory from "@/components/ScamCategory";
import ActionGuideWrapper from "@/components/ActionGuideWrapper";
import { mockScanResult } from "@/data/mockData";
import { formatTimestamp } from "@/utils/riskUtils";

export default function ReportPage() {
  const result = mockScanResult;

  return (
    <div className="px-4 md:px-8 py-8 max-w-5xl mx-auto space-y-5">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-sm text-[#8c909f]">
        <a href="/history" className="hover:text-[#adc6ff] transition-colors">
          History
        </a>
        <span className="material-symbols-outlined text-base">chevron_right</span>
        <span className="text-[#adc6ff] font-medium">
          Verdict #{result.scanId}
        </span>
      </nav>

      {/* Verdict Hero Card */}
      <VerdictCard
        verdict={result.verdict}
        title="High Danger Detected"
        description="TrustLens AI has identified high-confidence indicators of malicious intent in this communication."
        timestamp={formatTimestamp(result.timestamp)}
        scanId={result.scanId}
        riskLevel={result.riskLevel}
      />

      {/* Bento grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-5">
        {/* Risk Meter + Confidence Bar */}
        <div className="md:col-span-5 glass-panel rounded-2xl p-8 flex flex-col items-center justify-center gap-8 min-h-[360px]">
          <RiskMeter score={result.riskScore} />
          <div className="w-full">
            <ConfidenceBar value={result.confidenceScore} />
          </div>
        </div>

        {/* Category + Analysis */}
        <div className="md:col-span-7 flex flex-col gap-5">
          {/* Scam category */}
          <ScamCategory category={result.category} />

          {/* Analysis summary */}
          <div className="glass-panel rounded-2xl p-6 flex-1">
            <h4 className="font-[family-name:var(--font-manrope)] font-semibold text-base text-[#d8e3fb] mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-[#adc6ff] text-xl">
                info
              </span>
              Analysis Summary
            </h4>
            <div className="space-y-4 text-[#c2c6d6]">
              <p className="text-sm leading-relaxed">
                {result.explanation.split("urgent language").join("")}
                This message uses{" "}
                <span className="text-[#d8e3fb] font-semibold">
                  urgent language
                </span>{" "}
                and a{" "}
                <span className="text-[#d8e3fb] font-semibold">
                  suspicious link
                </span>{" "}
                masquerading as an official verification portal.
              </p>
              <p className="text-sm leading-relaxed">
                The sender&apos;s domain originates from a high-risk server
                cluster often associated with credential harvesting. The
                linguistic pattern analysis suggests an automated script
                designed to trigger anxiety and rapid decision-making.
              </p>

              {/* Original content quote */}
              {result.originalContent && (
                <div className="p-4 bg-[#081425] rounded-xl border border-[#424754]/50 italic font-[family-name:var(--font-geist)] text-xs text-[#c2c6d6] leading-relaxed">
                  {result.originalContent}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action Guide — full width */}
        <div className="md:col-span-12">
          <ActionGuideWrapper
            actions={result.actions}
            confidenceScore={result.confidenceScore}
          />
        </div>

        {/* Protected by Guardian banner */}
        <div className="md:col-span-12 relative glass-panel rounded-2xl overflow-hidden h-40 group">
          <div
            className="absolute inset-0 opacity-25 group-hover:scale-105 transition-transform duration-700"
            style={{
              background:
                "radial-gradient(ellipse at 20% 50%, rgba(107,216,203,0.4) 0%, transparent 60%), radial-gradient(ellipse at 80% 50%, rgba(77,142,255,0.3) 0%, transparent 60%)",
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#081425] via-[#081425]/50 to-transparent" />
          <div className="relative z-10 p-6 h-full flex items-end">
            <div className="flex items-center gap-3">
              <span
                className="material-symbols-outlined text-[#6bd8cb] text-2xl"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                verified
              </span>
              <h4 className="font-[family-name:var(--font-manrope)] font-semibold text-lg text-[#d8e3fb]">
                Protected by Guardian Intelligence
              </h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
