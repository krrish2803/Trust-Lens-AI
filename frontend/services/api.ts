/**
 * api.ts — Base API client stub
 *
 * This file provides the base HTTP client configuration.
 * Krrish: replace the stub implementations with real fetch/axios calls
 * pointing to the FastAPI backend.
 *
 * Base URL is read from the NEXT_PUBLIC_API_URL env variable.
 * Default: http://localhost:8000
 */

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// ─── Generic GET ──────────────────────────────────────────────────────────

export async function apiGet<T>(path: string): Promise<T> {
  // TODO (Krrish): implement real fetch
  // const res = await fetch(`${API_BASE}${path}`, { headers: authHeaders() });
  // if (!res.ok) throw new ApiError(res.status, await res.text());
  // return res.json();
  console.warn(`[API stub] GET ${API_BASE}${path}`);
  throw new Error(`API not connected yet. GET ${path}`);
}

// ─── Generic POST ─────────────────────────────────────────────────────────

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  // TODO (Krrish): implement real fetch
  // const res = await fetch(`${API_BASE}${path}`, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json", ...authHeaders() },
  //   body: JSON.stringify(body),
  // });
  // if (!res.ok) throw new ApiError(res.status, await res.text());
  // return res.json();
  console.warn(`[API stub] POST ${API_BASE}${path}`, body);
  throw new Error(`API not connected yet. POST ${path}`);
}

// ─── Generic POST (multipart form) ───────────────────────────────────────

export async function apiPostForm<T>(
  path: string,
  formData: FormData,
): Promise<T> {
  // TODO (Krrish): implement real fetch
  console.warn(`[API stub] POST (form) ${API_BASE}${path}`, formData);
  throw new Error(`API not connected yet. POST form ${path}`);
}

// ─── Auth headers helper (to be filled in by auth.ts) ────────────────────

export function authHeaders(): Record<string, string> {
  // TODO (Krrish): read JWT token from cookie/localStorage
  return {};
}
