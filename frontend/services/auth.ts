/**
 * auth.ts — Authentication service
 *
 * FastAPI routes:
 *   POST /api/auth/login   → { access_token: string }
 *   POST /api/auth/signup  → { access_token: string }
 *   POST /api/auth/logout  → void
 *   GET  /api/auth/me      → UserProfile
 */

import { apiGet, apiPost } from "./api";
import type { UserProfile } from "@/types";

const TOKEN_KEY = "access_token";

// ─── Token helpers ────────────────────────────────────────────────────────

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

function saveToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

// ─── Login ────────────────────────────────────────────────────────────────

export async function login(
  email: string,
  password: string,
): Promise<{ access_token: string }> {
  const result = await apiPost<{ access_token: string }>("/api/auth/login", {
    email,
    password,
  });
  saveToken(result.access_token);
  return result;
}

// ─── Signup ───────────────────────────────────────────────────────────────

export async function signup(
  name: string,
  email: string,
  password: string,
): Promise<{ access_token: string }> {
  const result = await apiPost<{ access_token: string }>("/api/auth/signup", {
    name,
    email,
    password,
  });
  saveToken(result.access_token);
  return result;
}

// ─── Logout ───────────────────────────────────────────────────────────────

export async function logout(): Promise<void> {
  if (typeof window !== "undefined") {
    localStorage.removeItem(TOKEN_KEY);
  }
}

// ─── Get current user profile ─────────────────────────────────────────────

export async function getProfile(): Promise<UserProfile> {
  return apiGet<UserProfile>("/api/auth/me");
}

// ─── Update profile ───────────────────────────────────────────────────────

export async function updateProfile(
  data: Partial<UserProfile>,
): Promise<UserProfile> {
  return apiPost<UserProfile>("/api/auth/profile", data);
}
