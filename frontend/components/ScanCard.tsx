"use client";

import { memo } from "react";
import Link from "next/link";
import { ScreenshotScanIcon } from "@/components/icons/BrandIcons";

interface ScanCardProps {
  icon: string;
  title: string;
  description: string;
  ctaLabel: string;
  href: string;
  recommended?: boolean;
  iconBg?: string;
  iconColor?: string;
}

function ScanCardInner({
  icon,
  title,
  description,
  ctaLabel,
  href,
  recommended = false,
  iconBg = "bg-[#2a3548]",
  iconColor = "text-[#adc6ff]",
}: ScanCardProps) {
  return (
    <Link href={href} className="block group h-full">
      <div
        className={`glass-card relative h-full flex flex-col gap-5 p-7 rounded-2xl transition-all duration-300 cursor-pointer hover:border-[#adc6ff]/25 hover:bg-[#1f2a3c]/70 ${
          recommended
            ? "border-2 border-[#4d8eff]/30 scale-[1.02] shadow-2xl shadow-[#4d8eff]/8"
            : ""
        }`}
      >
        {recommended && (
          <div className="absolute top-0 right-0 bg-[#4d8eff] text-[#002e6a] text-xs font-bold px-3 py-1 rounded-bl-xl rounded-tr-2xl">
            Recommended
          </div>
        )}

        <div
          className={`w-14 h-14 rounded-2xl ${iconBg} flex items-center justify-center ${iconColor} group-hover:scale-110 transition-transform duration-200`}
        >
          {icon === "screenshot_region" ? (
            <ScreenshotScanIcon size={30} color={iconColor.includes("text-[#002e6a]") ? "#002e6a" : "#adc6ff"} />
          ) : (
            <span className="material-symbols-outlined text-3xl leading-none">
              {icon}
            </span>
          )}
        </div>

        <div className="flex-1">
          <h3 className="font-[family-name:var(--font-manrope)] font-semibold text-lg text-white mb-2">
            {title}
          </h3>
          <p className="text-[#c2c6d6] text-sm leading-relaxed">{description}</p>
        </div>

        <div className="pt-4 border-t border-white/5 flex items-center text-[#adc6ff] font-semibold text-sm group-hover:text-[#bdd0ff] transition-colors">
          {ctaLabel}
          <span className="material-symbols-outlined ml-auto text-xl leading-none transition-transform group-hover:translate-x-1">
            chevron_right
          </span>
        </div>
      </div>
    </Link>
  );
}

const ScanCard = memo(ScanCardInner);
export default ScanCard;
