/**
 * TrustLens AI - Unified Type System & Canonical Definitions
 */

export type RiskLevel =
  | 'safe' | 'low' | 'medium' | 'high' | 'critical'
  | 'Safe' | 'Low Risk' | 'Medium Risk' | 'High Risk' | 'Critical';

export type ScanType = 'url' | 'message' | 'image' | 'link' | 'screenshot' | 'text';

export type Verdict = 'SAFE' | 'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK' | 'CRITICAL';

export interface UserProfile {
  id: string;
  name?: string;
  fullName?: string;
  email: string;
  role?: string;
  created_at?: string;
}

export interface UserSettings {
  realtimeAlerts?: boolean;
  biometricAuth?: boolean;
  sessionTimeout?: number;
}

export interface ThreatDetail {
  layer: string;
  finding: string;
  severity: string;
  weight: number;
}

export interface ActionStep {
  step: number;
  title: string;
  description: string;
  severity: 'primary' | 'tertiary' | 'error';
}

export interface ScanResultResponse {
  id: string;
  scan_type: ScanType;
  input_summary: string;
  risk_score: number;
  confidence_score: number;
  verdict: RiskLevel;
  scam_category: string;
  matched_phrases: string[];
  detected_urls: string[];
  reasons: string[];
  recommended_actions: string[] | ActionStep[];
  extracted_text?: string;
  ai_explanation?: string;
  threat_breakdown?: ThreatDetail[];
  created_at: string;
}

// Canonical model matching UI & mock representations
export interface ScanResult {
  scanId: string;
  timestamp: string;
  input: string;
  type: ScanType;
  verdict: Verdict | RiskLevel;
  riskLevel: RiskLevel;
  riskScore: number;
  confidenceScore: number;
  category: string;
  explanation: string;
  originalContent?: string;
  actions: ActionStep[];
}

export interface ScanHistoryItem {
  scanId: string;
  timestamp: string;
  title: string;
  snippet: string;
  type: ScanType;
  verdict: Verdict | string;
  riskLevel: RiskLevel;
}

export interface DashboardStats {
  totalScans: number;
  scamsBlocked: number;
  securityRating: number;
  monthlyChange: number;
}

export interface RecentScanItem {
  id: string;
  name: string;
  verdict: string;
  time: string;
  icon: string;
}

export interface HistoryResponse {
  status: string;
  count: number;
  data: ScanResultResponse[];
}
