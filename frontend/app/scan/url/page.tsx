"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { scanUrl } from "@/services/api";

export default function ScanUrlPage() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await scanUrl(url.trim());
      // Save result in localStorage for instant render
      localStorage.setItem("lastScanResult", JSON.stringify(result));
      router.push(`/scan/result?id=${result.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to scan URL. Please verify backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto space-y-8 py-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Scan Suspicious URL</h1>
          <p className="text-slate-400">
            Check any web link, domain name, or short URL for phishing attacks, fake brand clones, and malicious IP redirects.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 backdrop-blur-xl rounded-2xl p-6 md:p-8 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="url" className="block text-sm font-medium text-slate-300 mb-2">
                Enter Web Address (URL)
              </label>
              <input
                id="url"
                type="text"
                placeholder="https://sbi-kyc-update.online or http://bit.ly/claim-reward"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-700/80 rounded-xl px-4 py-3.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500 transition-all font-mono text-sm"
              />
            </div>

            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
                ⚠️ {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !url.trim()}
              className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold rounded-xl shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-base"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing Threat Layers...
                </>
              ) : (
                "🛡️ Analyze URL Threat"
              )}
            </button>
          </form>

          <div className="mt-8 border-t border-slate-800/80 pt-6">
            <h3 className="text-xs uppercase font-bold text-slate-400 tracking-wider mb-3">Quick URL Samples to Try</h3>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => setUrl("http://sbi-kyc-update-portal.online")}
                className="px-3 py-1.5 bg-slate-800/80 hover:bg-slate-700/80 rounded-lg text-xs font-mono text-cyan-400 transition"
              >
                sbi-kyc-update-portal.online
              </button>
              <button
                type="button"
                onClick={() => setUrl("http://192.168.1.1/login.php")}
                className="px-3 py-1.5 bg-slate-800/80 hover:bg-slate-700/80 rounded-lg text-xs font-mono text-cyan-400 transition"
              >
                192.168.1.1/login.php
              </button>
              <button
                type="button"
                onClick={() => setUrl("https://bit.ly/free-kbc-reward-claim")}
                className="px-3 py-1.5 bg-slate-800/80 hover:bg-slate-700/80 rounded-lg text-xs font-mono text-cyan-400 transition"
              >
                bit.ly/free-kbc-reward-claim
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
