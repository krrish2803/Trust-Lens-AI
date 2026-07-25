// ─── Risk & Verdict ────────────────────────────────────────────────────────

export type RiskLevel = "safe" | "low" | "medium" | "high" | "critical";

export type Verdict = "SAFE" | "LOW_RISK" | "MEDIUM_RISK" | "HIGH_RISK" | "CRITICAL";

export type ScanType = "link" | "message" | "screenshot";

export type ScamCategoryType =
  | "Fake KYC Scam"
  | "UPI Fraud"
  | "Job Scam"
  | "Phishing Link"
  | "Impersonation"
  | "Lottery Scam"
  | "Investment Fraud"
  | "OTP Fraud"
  | "Package Delivery Scam"
  | "Tech Support Scam"
  | "Unknown";

// ─── Scan Result ───────────────────────────────────────────────────────────

export interface ScanResult {
  scanId: string;
  timestamp: string;
  input: string;
  type: ScanType;
  verdict: Verdict;
  riskLevel: RiskLevel;
  riskScore: number;          // 0–100
  confidenceScore: number;    // 0–100
  category: ScamCategoryType;
  explanation: string;
  originalContent?: string;
  actions: ActionStep[];
}

export interface ActionStep {
  step: number;
  title: string;
  description: string;
  severity: "error" | "primary" | "tertiary";
}

// ─── History ───────────────────────────────────────────────────────────────

export interface ScanHistoryItem {
  scanId: string;
  timestamp: string;
  title: string;
  snippet: string;
  type: ScanType;
  verdict: Verdict;
  riskLevel: RiskLevel;
}

// ─── Dashboard ─────────────────────────────────────────────────────────────

export interface DashboardStats {
  totalScans: number;
  scamsBlocked: number;
  securityRating: number;
  monthlyChange: number;
}

export interface RecentScanItem {
  id: string;
  name: string;
  verdict: "Safe" | "Critical Scam" | "Suspicious" | "Verified" | "Medium Risk";
  time: string;
  icon: string;
}

// ─── User ──────────────────────────────────────────────────────────────────

export interface UserProfile {
  id: string;
  fullName: string;
  email: string;
  avatarUrl?: string;
}

export interface UserSettings {
  realtimeAlerts: boolean;
  biometricAuth: boolean;
  sessionTimeout: number; // minutes
}
