"use client";

import { useState } from "react";
import Link from "next/link";
import { mockHistory } from "@/data/mockData";
import { getRiskStrokeColor, getScanTypeIcon, formatTimestamp } from "@/utils/riskUtils";
import type { RiskLevel } from "@/types";
import ScamCategory from "@/components/ScamCategory";
import {
  SafeVerdictIcon,
  RiskyWarningIcon,
  CriticalAlertIcon,
} from "@/components/icons/BrandIcons";

const filterTabs: { label: string; value: RiskLevel | "all"; icon?: string }[] = [
  { label: "All Scans", value: "all" },
  { label: "Safe", value: "safe", icon: "safe" },
  { label: "Medium", value: "medium", icon: "risky" },
  { label: "High", value: "high", icon: "risky" },
  { label: "Critical", value: "critical", icon: "critical" },
];

const verdictLabel: Record<string, string> = {
  SAFE: "Secure",
  LOW_RISK: "Low Risk",
  MEDIUM_RISK: "Medium Risk",
  HIGH_RISK: "High Risk",
  CRITICAL: "Critical Risk",
};

export default function HistoryPage() {
  const [activeFilter, setActiveFilter] = useState<RiskLevel | "all">("all");
  const [search, setSearch] = useState("");

  const filtered = mockHistory.filter((item) => {
    const matchesFilter =
      activeFilter === "all" || item.riskLevel === activeFilter;
    const matchesSearch =
      !search ||
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.snippet.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="px-4 md:px-8 py-8 max-w-4xl mx-auto">
      {/* Page header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="font-[family-name:var(--font-manrope)] font-bold text-4xl md:text-5xl text-white mb-2">
            Scan Archives
          </h1>
          <p className="text-[#c2c6d6] text-base">
            Comprehensive audit trail of AI-analyzed activities.
          </p>
        </div>
        <div className="hidden md:flex w-12 h-12 rounded-xl bg-[#2a3548] items-center justify-center text-[#8c909f]">
          <span className="material-symbols-outlined text-xl">history</span>
        </div>
      </div>

      {/* Search bar (mobile) */}
      <div className="relative mb-6 md:hidden">
        <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[#8c909f] text-xl">
          search
        </span>
        <input
          type="text"
          placeholder="Search past scans..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-[#152031] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl pl-10 pr-4 py-3 text-sm outline-none transition-colors"
        />
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap mb-8">
        {filterTabs.map((tab) => {
          const isActive = activeFilter === tab.value;
          return (
            <button
              key={tab.value}
              id={`filter-${tab.value}`}
              onClick={() => setActiveFilter(tab.value)}
              className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                isActive
                  ? "bg-[#4d8eff] text-[#002e6a]"
                  : "bg-[#2a3548] text-[#c2c6d6] hover:bg-[#2a3548]/80 hover:text-white"
              }`}
            >
              {tab.icon === "safe" && (
                <SafeVerdictIcon size={16} color={isActive ? "#002e6a" : "#6bd8cb"} />
              )}
              {tab.icon === "risky" && (
                <RiskyWarningIcon size={16} color={isActive ? "#002e6a" : "#ffb786"} />
              )}
              {tab.icon === "critical" && (
                <CriticalAlertIcon size={16} color={isActive ? "#002e6a" : "#ffb4ab"} />
              )}
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Timeline list */}
      <div className="relative">
        {/* Vertical timeline line */}
        <div className="absolute left-3 top-0 bottom-0 w-px bg-[#2a3548] md:left-5" />

        <div className="space-y-3 pl-10 md:pl-14">
          {filtered.length === 0 ? (
            <div className="text-center py-16 text-[#8c909f]">
              <span className="material-symbols-outlined text-5xl mb-3 block">
                search_off
              </span>
              No scans matching your filter.
            </div>
          ) : (
            filtered.map((item, index) => {
              const color = getRiskStrokeColor(item.riskLevel as RiskLevel);
              return (
                <div key={item.scanId} className="relative">
                  {/* Timeline dot */}
                  <div
                    className="absolute -left-10 md:-left-14 top-5 w-3 h-3 rounded-full border-2 border-[#081425]"
                    style={{ background: color }}
                  />

                  <Link href={`/scan/result?id=${item.scanId}`}>
                    <div
                      className="glass-card rounded-xl p-4 md:p-5 flex items-center gap-4 hover:border-white/10 hover:bg-[#1f2a3c]/60 transition-all duration-200 cursor-pointer animate-fade-in-up"
                      style={{ animationDelay: `${index * 60}ms` }}
                    >
                      {/* Type icon */}
                      <div
                        className="w-10 h-10 md:w-12 md:h-12 rounded-xl flex items-center justify-center shrink-0"
                        style={{ background: `${color}18` }}
                      >
                        <span
                          className="material-symbols-outlined text-xl"
                          style={{ color }}
                        >
                          {getScanTypeIcon(item.type)}
                        </span>
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <p className="font-[family-name:var(--font-manrope)] font-semibold text-[#d8e3fb] text-sm md:text-base truncate">
                          {item.title}
                        </p>
                        <p className="text-[#8c909f] text-xs truncate mt-0.5">
                          {item.snippet}
                        </p>
                      </div>

                      {/* Verdict + time */}
                      <div className="flex flex-col items-end gap-1.5 shrink-0">
                        <ScamCategory
                          category={verdictLabel[item.verdict] ?? item.verdict}
                          compact
                        />
                        <span className="text-xs text-[#8c909f]">
                          {formatTimestamp(item.timestamp)}
                        </span>
                      </div>
                    </div>
                  </Link>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Load more */}
      <div className="text-center mt-10">
        <button
          id="load-more-btn"
          className="inline-flex items-center gap-2 text-[#c2c6d6] hover:text-[#adc6ff] text-sm font-medium transition-colors"
        >
          Load More History
          <span className="material-symbols-outlined text-base">
            expand_more
          </span>
        </button>
      </div>
    </div>
  );
}
