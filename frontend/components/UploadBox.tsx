"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { ScreenshotScanIcon } from "@/components/icons/BrandIcons";
import { scanUrl, scanMessage, scanImage } from "@/services/api";

type TabType = "link" | "message" | "screenshot";

export interface UploadBoxProps {
  onFileSelect?: (file: File) => void;
  defaultTab?: TabType;
}

const tabs: { id: TabType; label: string; icon: string | null; brandIcon?: string }[] = [
  { id: "link", label: "Link", icon: "link" },
  { id: "message", label: "Message", icon: "chat_bubble" },
  { id: "screenshot", label: "Screenshot", icon: null, brandIcon: "screenshot" },
];

const features = [
  {
    icon: "shield_lock",
    title: "Privacy First",
    description: "Data is processed in isolation and never stored.",
  },
  {
    icon: "local_fire_department",
    title: "Deep Analysis",
    description: "Checks against 1M+ known threat indicators.",
  },
  {
    icon: "psychology",
    title: "AI Detection",
    description: "Identifies semantic social engineering tricks.",
  },
];

export default function UploadBox({ onFileSelect, defaultTab = "link" }: UploadBoxProps) {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<TabType>(defaultTab);
  const [urlValue, setUrlValue] = useState("");
  const [messageValue, setMessageValue] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (file: File | null) => {
    setSelectedFile(file);
    if (file && onFileSelect) {
      onFileSelect(file);
    }
  };

  const [apiError, setApiError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (activeTab === "link" && !urlValue.trim()) return;
    if (activeTab === "message" && !messageValue.trim()) return;
    if (activeTab === "screenshot" && !selectedFile) return;

    setIsScanning(true);
    setApiError(null);

    try {
      let result;
      if (activeTab === "link") {
        result = await scanUrl(urlValue.trim());
      } else if (activeTab === "message") {
        result = await scanMessage(messageValue.trim());
      } else {
        result = await scanImage(selectedFile!);
      }
      localStorage.setItem("lastScanResult", JSON.stringify(result));
      router.push(`/scan/result?id=${result.id}`);
    } catch (err: any) {
      setApiError(err.message || "Scan failed. Please ensure the backend is running.");
    } finally {
      setIsScanning(false);
    }
  };

  const canSubmit =
    (activeTab === "link" && urlValue.trim()) ||
    (activeTab === "message" && messageValue.trim()) ||
    (activeTab === "screenshot" && selectedFile);

  return (
    <div className="space-y-6">
      {/* Tab Bar */}
      <div className="glass-card rounded-2xl p-1.5 flex gap-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-sm font-semibold transition-all duration-200 ${
              activeTab === tab.id
                ? "bg-[#4d8eff] text-[#002e6a] shadow-lg"
                : "text-[#c2c6d6] hover:text-[#d8e3fb] hover:bg-[#2a3548]"
            }`}
          >
            {tab.brandIcon === "screenshot" ? (
              <ScreenshotScanIcon
                size={18}
                color={activeTab === tab.id ? "#002e6a" : "#c2c6d6"}
              />
            ) : (
              <span className="material-symbols-outlined text-lg leading-none">
                {tab.icon}
              </span>
            )}
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Input Panel */}
      <div className="glass-panel rounded-2xl p-6 md:p-8 space-y-6">
        {/* Link Tab */}
        {activeTab === "link" && (
          <div className="space-y-3 animate-fade-in">
            <label htmlFor="url-input" className="block text-xs font-semibold text-[#8c909f] uppercase tracking-widest">
              Target URL
            </label>
            <input
              id="url-input"
              type="url"
              value={urlValue}
              onChange={(e) => setUrlValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAnalyze()}
              placeholder="https://suspicious-site.com/..."
              className="w-full bg-[#081425] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3.5 text-sm outline-none transition-colors duration-200 font-[family-name:var(--font-geist)]"
            />
            <p className="flex items-center gap-1.5 text-xs text-[#8c909f]">
              <span className="material-symbols-outlined text-sm">info</span>
              We&apos;ll perform a safe, isolated deep-link analysis.
            </p>
          </div>
        )}

        {/* Message Tab */}
        {activeTab === "message" && (
          <div className="space-y-3 animate-fade-in">
            <label htmlFor="message-input" className="block text-xs font-semibold text-[#8c909f] uppercase tracking-widest">
              Paste Message / SMS / Email
            </label>
            <textarea
              id="message-input"
              value={messageValue}
              onChange={(e) => setMessageValue(e.target.value)}
              placeholder="Paste the suspicious SMS, WhatsApp message, or email here..."
              rows={6}
              className="w-full bg-[#081425] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3.5 text-sm outline-none transition-colors duration-200 resize-none"
            />
            <p className="flex items-center gap-1.5 text-xs text-[#8c909f]">
              <span className="material-symbols-outlined text-sm">info</span>
              Works with Hindi, English, and Hinglish messages.
            </p>
          </div>
        )}

        {/* Screenshot Tab */}
        {activeTab === "screenshot" && (
          <div className="space-y-3 animate-fade-in">
            <label htmlFor="screenshot-upload" className="block text-xs font-semibold text-[#8c909f] uppercase tracking-widest">
              Upload Screenshot
            </label>
            <div
              id="drop-zone"
              role="button"
              tabIndex={0}
              aria-label="Upload screenshot by clicking or dragging a file"
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  fileInputRef.current?.click();
                }
              }}
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={(e) => {
                e.preventDefault();
                setIsDragging(false);
                const file = e.dataTransfer.files[0];
                if (file) handleFileChange(file);
              }}
              onClick={() => fileInputRef.current?.click()}
              className={`flex flex-col items-center justify-center gap-4 border-2 border-dashed rounded-2xl py-14 px-6 text-center cursor-pointer transition-all duration-200 ${
                isDragging
                  ? "border-[#4d8eff] bg-[#4d8eff]/5"
                  : "border-[#424754] hover:border-[#adc6ff]/40 hover:bg-[#1f2a3c]/50"
              }`}
            >
              {selectedFile ? (
                <>
                  <span
                    className="material-symbols-outlined text-5xl text-[#6bd8cb]"
                    style={{ fontVariationSettings: "'FILL' 1" }}
                  >
                    check_circle
                  </span>
                  <div>
                    <p className="text-[#d8e3fb] font-semibold">
                      {selectedFile.name}
                    </p>
                    <p className="text-[#8c909f] text-sm mt-1">
                      {(selectedFile.size / 1024).toFixed(0)} KB
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleFileChange(null);
                    }}
                    className="text-xs text-[#ffb4ab] hover:underline"
                  >
                    Remove
                  </button>
                </>
              ) : (
                <>
                  <span className="material-symbols-outlined text-5xl text-[#424754]">
                    cloud_upload
                  </span>
                  <div>
                    <p className="text-[#c2c6d6] font-semibold">
                      Drop screenshot here or{" "}
                      <span className="text-[#adc6ff]">browse</span>
                    </p>
                    <p className="text-[#8c909f] text-sm mt-1">
                      PNG, JPG, WEBP — max 10MB
                    </p>
                  </div>
                </>
              )}
            </div>
            <input
              ref={fileInputRef}
              id="screenshot-upload"
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileChange(file);
              }}
            />
            <p className="flex items-center gap-1.5 text-xs text-[#8c909f]">
              <span className="material-symbols-outlined text-sm">info</span>
              OCR-powered detection for payment receipts and UI spoofs.
            </p>
          </div>
        )}

        {/* Analyze Button */}
        <button
          id="analyze-button"
          onClick={handleAnalyze}
          disabled={!canSubmit || isScanning}
          className={`w-full flex items-center justify-center gap-3 py-4 rounded-xl font-bold text-base transition-all duration-200 ${
            canSubmit && !isScanning
              ? "bg-[#adc6ff] hover:bg-[#bdd0ff] text-[#002e6a] active:scale-95 cursor-pointer"
              : "bg-[#2a3548] text-[#8c909f] cursor-not-allowed"
          }`}
        >
          {isScanning ? (
            <>
              <span className="animate-spin-slow material-symbols-outlined text-xl leading-none">
                progress_activity
              </span>
              Analyzing...
            </>
          ) : (
            <>
              Analyze Now
              <span className="material-symbols-outlined text-xl leading-none">
                bolt
              </span>
            </>
          )}
        </button>

        {apiError && (
          <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm text-center">
            {apiError}
          </div>
        )}
      </div>

      {/* Feature pills */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {features.map((f) => (
          <div
            key={f.title}
            className="glass-card rounded-xl p-4 flex items-start gap-3"
          >
            <span className="material-symbols-outlined text-[#6bd8cb] text-xl mt-0.5 shrink-0">
              {f.icon}
            </span>
            <div>
              <p className="text-[#d8e3fb] text-sm font-semibold">{f.title}</p>
              <p className="text-[#8c909f] text-xs leading-relaxed mt-0.5">
                {f.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
