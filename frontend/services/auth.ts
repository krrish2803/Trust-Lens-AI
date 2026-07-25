/**
 * auth.ts — Authentication service stubs
 *
 * Krrish: wire these to the FastAPI auth endpoints.
 *
 * Expected FastAPI routes:
 *   POST /api/auth/login   → { access_token: string }
 *   POST /api/auth/logout  → void
 *   GET  /api/auth/me      → UserProfile
 */

import { apiGet, apiPost } from "./api";
import type { UserProfile } from "@/types";

// ─── Login ────────────────────────────────────────────────────────────────

export async function login(
  email: string,
  password: string,
): Promise<{ access_token: string }> {
  // TODO (Krrish): replace with real API call
  return apiPost("/api/auth/login", { email, password });
}

// ─── Signup ───────────────────────────────────────────────────────────────

export async function signup(
  name: string,
  email: string,
  password: string,
): Promise<{ access_token: string }> {
  // TODO (Krrish): replace with real API call
  return apiPost("/api/auth/signup", { name, email, password });
}

// ─── Logout ───────────────────────────────────────────────────────────────

export async function logout(): Promise<void> {
  // TODO (Krrish): replace with real API call + clear local token
  console.warn("[stub] logout()");
}

// ─── Get current user profile ─────────────────────────────────────────────

export async function getProfile(): Promise<UserProfile> {
  // TODO (Krrish): replace with real API call
  return apiGet<UserProfile>("/api/auth/me");
}

// ─── Update profile ───────────────────────────────────────────────────────

export async function updateProfile(
  data: Partial<UserProfile>,
): Promise<UserProfile> {
  // TODO (Krrish): replace with real API call
  return apiPost<UserProfile>("/api/auth/profile", data);
}
