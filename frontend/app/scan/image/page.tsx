"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import UploadBox from "@/components/UploadBox";
import { scanImage } from "@/services/api";

export default function ScanImagePage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const result = await scanImage(selectedFile);
      localStorage.setItem("lastScanResult", JSON.stringify(result));
      router.push(`/scan/result?id=${result.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to analyze image screenshot.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto space-y-8 py-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Upload Screenshot / Image</h1>
          <p className="text-slate-400">
            Upload screenshots of WhatsApp chats, UPI transaction receipts, SMS alerts, or banking apps. EasyOCR extracts text for threat analysis.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 backdrop-blur-xl rounded-2xl p-6 md:p-8 shadow-2xl space-y-6">
          <UploadBox onFileSelect={(file) => setSelectedFile(file)} />

          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
              ⚠️ {error}
            </div>
          )}

          <button
            type="button"
            onClick={handleScan}
            disabled={loading || !selectedFile}
            className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold rounded-xl shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50 flex items-center justify-center gap-2 text-base"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Processing EasyOCR & Multi-layer Pipeline...
              </>
            ) : (
              "📸 Extract & Scan Screenshot"
            )}
          </button>
        </div>
      </div>
    </AppShell>
  );
}
