/**
 * scanner.ts — Scan submission & retrieval stubs
 *
 * Krrish: wire these functions to the FastAPI detection endpoints.
 * The function signatures, parameter names, and return types are fixed —
 * do NOT rename them (they are imported by pages that Muskan built).
 *
 * Expected FastAPI routes:
 *   POST /api/scan/url        → ScanResult
 *   POST /api/scan/message    → ScanResult
 *   POST /api/scan/image      → ScanResult
 *   GET  /api/scan/:scanId    → ScanResult
 *   GET  /api/history         → ScanHistoryItem[]
 */

import { apiGet, apiPost, apiPostForm } from "./api";
import type { ScanResult, ScanHistoryItem, RiskLevel } from "@/types";

// ─── Scan a URL ───────────────────────────────────────────────────────────

export async function scanUrl(url: string): Promise<ScanResult> {
  // TODO (Krrish): replace with real API call
  // return apiPost<ScanResult>("/api/scan/url", { url });
  return apiPost<ScanResult>("/api/scan/url", { url });
}

// ─── Scan a text message ──────────────────────────────────────────────────

export async function scanMessage(text: string): Promise<ScanResult> {
  // TODO (Krrish): replace with real API call
  // return apiPost<ScanResult>("/api/scan/message", { text });
  return apiPost<ScanResult>("/api/scan/message", { text });
}

// ─── Scan an uploaded image ───────────────────────────────────────────────

export async function scanImage(file: File): Promise<ScanResult> {
  // TODO (Krrish): replace with real API call
  const formData = new FormData();
  formData.append("file", file);
  return apiPostForm<ScanResult>("/api/scan/image", formData);
}

// ─── Fetch a specific scan result ─────────────────────────────────────────

export async function getScanResult(scanId: string): Promise<ScanResult> {
  // TODO (Krrish): replace with real API call
  // return apiGet<ScanResult>(`/api/scan/${scanId}`);
  return apiGet<ScanResult>(`/api/scan/${scanId}`);
}

// ─── Fetch scan history ───────────────────────────────────────────────────

export interface HistoryFilters {
  riskLevel?: RiskLevel | "all";
  page?: number;
  pageSize?: number;
  search?: string;
}

export async function getScanHistory(
  filters?: HistoryFilters,
): Promise<ScanHistoryItem[]> {
  // TODO (Krrish): replace with real API call
  const params = new URLSearchParams();
  if (filters?.riskLevel && filters.riskLevel !== "all")
    params.set("risk", filters.riskLevel);
  if (filters?.page) params.set("page", String(filters.page));
  if (filters?.search) params.set("q", filters.search);
  return apiGet<ScanHistoryItem[]>(`/api/history?${params.toString()}`);
}

// ─── Delete a scan from history ───────────────────────────────────────────

export async function deleteScan(scanId: string): Promise<void> {
  // TODO (Krrish): replace with real API call
  // return apiPost(`/api/scan/${scanId}/delete`, {});
  console.warn(`[stub] deleteScan(${scanId})`);
}
