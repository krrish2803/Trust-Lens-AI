"use client";

import { memo } from "react";
import { FingerprintIcon } from "@/components/icons/BrandIcons";

interface ScamCategoryProps {
  category: string;
  icon?: string;
  compact?: boolean;
}

const categoryMeta: Record<string, { icon: string; color: string }> = {
  "Fake KYC Scam": { icon: "fingerprint", color: "#ffb786" },
  "UPI Fraud": { icon: "payments", color: "#ffb4ab" },
  "Job Scam": { icon: "work", color: "#ffb786" },
  "Phishing Link": { icon: "phishing", color: "#ffb4ab" },
  Impersonation: { icon: "person_off", color: "#ffb786" },
  "Lottery Scam": { icon: "casino", color: "#ffb4ab" },
  "Investment Fraud": { icon: "trending_down", color: "#ffb4ab" },
  "OTP Fraud": { icon: "lock_open", color: "#ffb786" },
  "Package Delivery Scam": { icon: "local_shipping", color: "#adc6ff" },
  "Tech Support Scam": { icon: "computer", color: "#adc6ff" },
  Safe: { icon: "verified", color: "#6bd8cb" },
  Unknown: { icon: "help_outline", color: "#8c909f" },
};

function ScamCategoryInner({ category, icon, compact = false }: ScamCategoryProps) {
  const meta = categoryMeta[category] ?? categoryMeta["Unknown"];
  const displayIcon = icon ?? meta.icon;
  const color = meta.color;

  if (compact) {
    return (
      <span
        className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold"
        style={{
          background: `${color}15`,
          color: color,
          border: `1px solid ${color}30`,
        }}
      >
        {category === "Fake KYC Scam" ? (
          <FingerprintIcon size={12} color={color} />
        ) : (
          <span className="material-symbols-outlined text-[12px]">
            {displayIcon}
          </span>
        )}
        {category}
      </span>
    );
  }

  return (
    <div
      className="glass-panel rounded-xl p-5 flex items-center justify-between"
      style={{ borderLeft: `4px solid ${color}` }}
    >
      <div>
        <p className="text-xs text-[#8c909f] font-medium uppercase tracking-wider mb-1">
          Threat Categorization
        </p>
        <h3 className="font-[family-name:var(--font-manrope)] font-semibold text-lg text-[#d8e3fb]">
          {category}
        </h3>
      </div>
      {category === "Fake KYC Scam" ? (
        <FingerprintIcon size={40} color={color} className="shrink-0" />
      ) : (
        <span
          className="material-symbols-outlined text-4xl"
          style={{
            color: color,
            fontVariationSettings: "'FILL' 0",
            filter: `drop-shadow(0 0 8px ${color}40)`,
          }}
        >
          {displayIcon}
        </span>
      )}
    </div>
  );
}

const ScamCategory = memo(ScamCategoryInner);
export default ScamCategory;
