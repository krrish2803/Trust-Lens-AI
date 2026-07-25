"use client";

import { useEffect, useRef } from "react";

interface ConfidenceBarProps {
  value: number; // 0–100
  label?: string;
}

export default function ConfidenceBar({
  value,
  label = "AI Confidence",
}: ConfidenceBarProps) {
  const barRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (barRef.current) {
      barRef.current.style.width = "0%";
      barRef.current.style.transition = "none";
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          if (barRef.current) {
            barRef.current.style.transition = "width 1.2s cubic-bezier(0.34,1.2,0.64,1)";
            barRef.current.style.width = `${value}%`;
          }
        });
      });
    }
  }, [value]);

  return (
    <div className="w-full space-y-2">
      <div className="flex justify-between items-baseline">
        <span className="text-xs text-[#8c909f] font-medium">{label}</span>
        <span className="font-[family-name:var(--font-manrope)] font-semibold text-xl text-[#6bd8cb]">
          {value}%
        </span>
      </div>

      {/* Track */}
      <div className="w-full h-3 bg-[#2a3548] rounded-full overflow-hidden">
        {/* Fill — teal → blue gradient */}
        <div
          ref={barRef}
          className="h-full rounded-full"
          style={{
            width: `${value}%`,
            background: "linear-gradient(to right, #6bd8cb, #4d8eff)",
            boxShadow: "0 0 10px rgba(107,216,203,0.35)",
          }}
        />
      </div>

      {/* Descriptor */}
      <p className="text-xs text-[#8c909f]">
        {value >= 90
          ? "Very high confidence — result is highly reliable"
          : value >= 70
            ? "High confidence — result is reliable"
            : value >= 50
              ? "Moderate confidence — use with caution"
              : "Low confidence — manual review recommended"}
      </p>
    </div>
  );
}
