"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { scanMessage } from "@/services/api";

export default function ScanMessagePage() {
  const router = useRouter();
  const [text, setText] = useState("");
  const [channel, setChannel] = useState("auto");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await scanMessage(text.trim(), channel);
      localStorage.setItem("lastScanResult", JSON.stringify(result));
      router.push(`/scan/result?id=${result.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to scan message text.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="max-w-4xl mx-auto space-y-8 py-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Scan Message / SMS / WhatsApp</h1>
          <p className="text-slate-400">
            Paste suspicious SMS, WhatsApp messages, emails, or Hinglish text to detect OTP fraud, KYC threats, digital arrest scams, and fake loan traps.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 backdrop-blur-xl rounded-2xl p-6 md:p-8 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="channel" className="block text-sm font-medium text-slate-300 mb-2">
                Message Origin Channel
              </label>
              <select
                id="channel"
                value={channel}
                onChange={(e) => setChannel(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700/80 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50"
              >
                <option value="auto">Auto-detect Channel</option>
                <option value="sms">SMS Text Message</option>
                <option value="whatsapp">WhatsApp Message</option>
                <option value="email">Email Body</option>
                <option value="telegram">Telegram / Social Media</option>
              </select>
            </div>

            <div>
              <label htmlFor="text" className="block text-sm font-medium text-slate-300 mb-2">
                Message Content / Text
              </label>
              <textarea
                id="text"
                rows={6}
                placeholder="Dear customer, your SBI account is blocked due to missing KYC. Click link to update immediately: http://bit.ly/sbi-update or send OTP to 9876543210..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-700/80 rounded-xl p-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-all font-sans text-sm leading-relaxed"
              />
            </div>

            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
                ⚠️ {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !text.trim()}
              className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold rounded-xl shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50 flex items-center justify-center gap-2 text-base"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Running Hinglish & AI Classifiers...
                </>
              ) : (
                "🔍 Analyze Message Safety"
              )}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
