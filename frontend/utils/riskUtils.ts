import type { RiskLevel, Verdict } from "@/types";

// ─── Risk Score → Level ────────────────────────────────────────────────────

export function getRiskLevel(score: number): RiskLevel {
  if (score < 20) return "safe";
  if (score < 40) return "low";
  if (score < 60) return "medium";
  if (score < 80) return "high";
  return "critical";
}

// ─── Risk Level → Tailwind Classes ────────────────────────────────────────

export function getRiskColor(level: RiskLevel): string {
  switch (level) {
    case "safe":
      return "text-[#6bd8cb]";
    case "low":
      return "text-[#adc6ff]";
    case "medium":
      return "text-[#adc6ff]";
    case "high":
      return "text-[#ffb786]";
    case "critical":
      return "text-[#ffb4ab]";
  }
}

export function getRiskBgColor(level: RiskLevel): string {
  switch (level) {
    case "safe":
      return "bg-[#6bd8cb]/15 border-[#6bd8cb]/25";
    case "low":
      return "bg-[#adc6ff]/12 border-[#adc6ff]/25";
    case "medium":
      return "bg-[#adc6ff]/12 border-[#adc6ff]/25";
    case "high":
      return "bg-[#ffb786]/12 border-[#ffb786]/25";
    case "critical":
      return "bg-[#ffb4ab]/15 border-[#ffb4ab]/30";
  }
}

export function getRiskStrokeColor(level: RiskLevel): string {
  switch (level) {
    case "safe":
      return "#6bd8cb";
    case "low":
      return "#adc6ff";
    case "medium":
      return "#4d8eff";
    case "high":
      return "#ffb786";
    case "critical":
      return "#ffb4ab";
  }
}

// ─── Risk Level → Label ────────────────────────────────────────────────────

export function getRiskLabel(level: RiskLevel): string {
  switch (level) {
    case "safe":
      return "Safe";
    case "low":
      return "Low Risk";
    case "medium":
      return "Medium Risk";
    case "high":
      return "High Risk";
    case "critical":
      return "Critical";
  }
}

// ─── Verdict → Readable ───────────────────────────────────────────────────

export function getVerdictLabel(verdict: Verdict): string {
  switch (verdict) {
    case "SAFE":
      return "Safe";
    case "LOW_RISK":
      return "Low Risk";
    case "MEDIUM_RISK":
      return "Medium Risk";
    case "HIGH_RISK":
      return "Risky";
    case "CRITICAL":
      return "Critical";
  }
}

export function getVerdictIcon(verdict: Verdict): string {
  switch (verdict) {
    case "SAFE":
      return "verified";
    case "LOW_RISK":
      return "info";
    case "MEDIUM_RISK":
      return "warning_amber";
    case "HIGH_RISK":
      return "warning";
    case "CRITICAL":
      return "gpp_bad";
  }
}

// ─── Format timestamp ─────────────────────────────────────────────────────

export function formatTimestamp(iso: string): string {
  try {
    return new Date(iso).toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  } catch {
    return iso;
  }
}

// ─── Scan type icon ───────────────────────────────────────────────────────

export function getScanTypeIcon(type: string): string {
  switch (type) {
    case "link":
      return "link";
    case "message":
      return "chat";
    case "screenshot":
      return "screenshot_region";
    default:
      return "search";
  }
}
