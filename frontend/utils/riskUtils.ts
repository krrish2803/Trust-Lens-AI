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
  const l = (level || "").toLowerCase();
  if (l.includes("safe")) return "text-[#6bd8cb]";
  if (l.includes("low")) return "text-[#adc6ff]";
  if (l.includes("medium")) return "text-[#adc6ff]";
  if (l.includes("high")) return "text-[#ffb786]";
  if (l.includes("critical")) return "text-[#ffb4ab]";
  return "text-[#adc6ff]";
}

export function getRiskBgColor(level: RiskLevel): string {
  const l = (level || "").toLowerCase();
  if (l.includes("safe")) return "bg-[#6bd8cb]/15 border-[#6bd8cb]/25";
  if (l.includes("low")) return "bg-[#adc6ff]/12 border-[#adc6ff]/25";
  if (l.includes("medium")) return "bg-[#adc6ff]/12 border-[#adc6ff]/25";
  if (l.includes("high")) return "bg-[#ffb786]/12 border-[#ffb786]/25";
  if (l.includes("critical")) return "bg-[#ffb4ab]/15 border-[#ffb4ab]/30";
  return "bg-[#adc6ff]/12 border-[#adc6ff]/25";
}

export function getRiskStrokeColor(level: RiskLevel): string {
  const l = (level || "").toLowerCase();
  if (l.includes("safe")) return "#6bd8cb";
  if (l.includes("low")) return "#adc6ff";
  if (l.includes("medium")) return "#4d8eff";
  if (l.includes("high")) return "#ffb786";
  if (l.includes("critical")) return "#ffb4ab";
  return "#4d8eff";
}

// ─── Risk Level → Label ────────────────────────────────────────────────────

export function getRiskLabel(level: RiskLevel): string {
  const l = (level || "").toLowerCase();
  if (l.includes("safe")) return "Safe";
  if (l.includes("low")) return "Low Risk";
  if (l.includes("medium")) return "Medium Risk";
  if (l.includes("high")) return "High Risk";
  if (l.includes("critical")) return "Critical";
  return "Unknown";
}

// ─── Verdict → Readable ───────────────────────────────────────────────────

export function getVerdictLabel(verdict: Verdict | string): string {
  const v = (verdict || "").toUpperCase();
  if (v.includes("SAFE")) return "Safe";
  if (v.includes("LOW")) return "Low Risk";
  if (v.includes("MEDIUM")) return "Medium Risk";
  if (v.includes("HIGH")) return "Risky";
  if (v.includes("CRITICAL")) return "Critical";
  return verdict;
}

export function getVerdictIcon(verdict: Verdict | string): string {
  const v = (verdict || "").toUpperCase();
  if (v.includes("SAFE")) return "verified";
  if (v.includes("LOW")) return "info";
  if (v.includes("MEDIUM")) return "warning_amber";
  if (v.includes("HIGH")) return "warning";
  if (v.includes("CRITICAL")) return "gpp_bad";
  return "info";
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
    case "url":
      return "link";
    case "message":
    case "text":
      return "chat";
    case "screenshot":
    case "image":
      return "screenshot_region";
    default:
      return "search";
  }
}
