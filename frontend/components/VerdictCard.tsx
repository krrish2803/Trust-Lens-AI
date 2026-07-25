"use client";

import { getRiskStrokeColor, getRiskLevel, getVerdictIcon, getVerdictLabel } from "@/utils/riskUtils";
import type { Verdict, RiskLevel } from "@/types";
import {
  CriticalAlertIcon,
  SafeVerdictIcon,
  RiskyWarningIcon,
} from "@/components/icons/BrandIcons";

interface VerdictCardProps {
  verdict: Verdict;
  title: string;
  description: string;
  timestamp: string;
  scanId: string;
  riskLevel?: RiskLevel;
}

export default function VerdictCard({
  verdict,
  title,
  description,
  timestamp,
  scanId,
  riskLevel,
}: VerdictCardProps) {
  const level = riskLevel ?? getRiskLevel(
    verdict === "CRITICAL" ? 95
    : verdict === "HIGH_RISK" ? 82
    : verdict === "MEDIUM_RISK" ? 52
    : verdict === "LOW_RISK" ? 28
    : 5
  );
  const strokeColor = getRiskStrokeColor(level);
  const icon = getVerdictIcon(verdict);
  const verdictLabel = getVerdictLabel(verdict);

  const isSafe = verdict === "SAFE" || verdict === "LOW_RISK";

  return (
    <div className="relative overflow-hidden glass-panel rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-center gap-8">
      {/* Scan-line animation overlay */}
      <div
        className="absolute inset-0 pointer-events-none animate-scan-line opacity-40"
        style={{
          background: `linear-gradient(to bottom, transparent, ${strokeColor}18, transparent)`,
          height: "40%",
          top: 0,
        }}
      />

      {/* Icon — brand SVG: Critical=✕circle, Safe=shield✓, High/Med=triangle! */}
      <div
        className="relative z-10 shrink-0 w-20 h-20 rounded-full flex items-center justify-center animate-float"
        style={{
          background: `${strokeColor}18`,
          border: `2px solid ${strokeColor}30`,
          filter: `drop-shadow(0 0 16px ${strokeColor}30)`,
        }}
      >
        {verdict === "CRITICAL" ? (
          <CriticalAlertIcon size={44} color={strokeColor} />
        ) : verdict === "SAFE" || verdict === "LOW_RISK" ? (
          <SafeVerdictIcon size={44} color={strokeColor} />
        ) : (
          <RiskyWarningIcon size={44} color={strokeColor} />
        )}
      </div>

      {/* Content */}
      <div className="relative z-10 flex-1 text-center md:text-left">
        {/* Verdict badge */}
        <div
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-3"
          style={{
            background: `${strokeColor}15`,
            border: `1px solid ${strokeColor}30`,
            color: strokeColor,
          }}
        >
          <span className="material-symbols-outlined text-[12px]">
            {isSafe ? "verified" : "report"}
          </span>
          Verdict: {verdictLabel}
        </div>

        <h1 className="font-[family-name:var(--font-manrope)] font-bold text-3xl md:text-4xl text-[#d8e3fb] mb-2">
          {title}
        </h1>
        <p className="text-[#c2c6d6] text-base leading-relaxed max-w-xl">
          {description}
        </p>
      </div>

      {/* Timestamp + ID */}
      <div className="relative z-10 flex flex-col items-center md:items-end gap-2 shrink-0">
        <span className="text-xs text-[#8c909f] font-medium">Scan ID</span>
        <span className="font-[family-name:var(--font-geist)] text-sm bg-[#152031] px-3 py-1.5 rounded-lg text-[#adc6ff] border border-[#424754]/50">
          #{scanId}
        </span>
        <span className="text-xs text-[#8c909f] mt-1">Timestamp</span>
        <span className="font-[family-name:var(--font-geist)] text-xs bg-[#152031] px-3 py-1.5 rounded-lg text-[#6bd8cb] border border-[#424754]/50">
          {timestamp}
        </span>
      </div>
    </div>
  );
}
