/**
 * TrustLens AI - Frontend TypeScript Definitions
 */

export type RiskLevel = 'Safe' | 'Low Risk' | 'Medium Risk' | 'High Risk' | 'Critical';

export type ScanType = 'url' | 'message' | 'image';

export type Verdict = 'SAFE' | 'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK' | 'CRITICAL';

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role?: string;
  created_at?: string;
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
  risk_score: number; // 0 to 100
  confidence_score: number; // 0.0 to 1.0
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

export interface HistoryResponse {
  status: string;
  count: number;
  data: ScanResultResponse[];
}
