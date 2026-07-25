/**
 * TrustLens AI - API Client Service
 * Connects Next.js Frontend to FastAPI Backend.
 */

import { ScanResultResponse, HistoryResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiGet<T = any>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) {
    throw new Error(`API GET request to ${endpoint} failed with status ${res.status}`);
  }
  return res.json();
}

export async function apiPost<T = any>(endpoint: string, body: any): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`API POST request to ${endpoint} failed with status ${res.status}`);
  }
  return res.json();
}

export async function scanUrl(url: string): Promise<ScanResultResponse> {
  const res = await fetch(`${API_BASE_URL}/scan/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze URL.');
  }

  return res.json();
}

export async function scanMessage(text: string, channel: string = 'auto'): Promise<ScanResultResponse> {
  const res = await fetch(`${API_BASE_URL}/scan/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, channel }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze message content.');
  }

  return res.json();
}

export async function scanImage(file: File): Promise<ScanResultResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/scan/image`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to process screenshot OCR analysis.');
  }

  return res.json();
}

export async function getHistory(limit: number = 20): Promise<HistoryResponse> {
  const res = await fetch(`${API_BASE_URL}/history?limit=${limit}`, {
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error('Failed to load scan history.');
  }

  return res.json();
}

export async function getScanById(scanId: string): Promise<ScanResultResponse> {
  const res = await fetch(`${API_BASE_URL}/history/${scanId}`, {
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error('Scan result not found.');
  }

  return res.json();
}
