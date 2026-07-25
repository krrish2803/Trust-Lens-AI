import Link from "next/link";
import { mockDashboardStats, mockRecentScans } from "@/data/mockData";

export const metadata = {
  title: "Dashboard — TrustLens AI",
  description: "Intelligence dashboard with real-time risk analytics and surveillance stats.",
};

const statCards = [
  {
    label: "TOTAL SCANS",
    value: "14,208",
    subtext: "12% from last month",
    trend: "up",
    icon: "radar",
    iconBg: "bg-[#4d8eff]/10",
    iconColor: "text-[#4d8eff]",
    trendColor: "text-[#6bd8cb]",
  },
  {
    label: "SCAMS BLOCKED",
    value: "432",
    subtext: "High-threat neutralizations",
    icon: "gpp_bad",
    iconBg: "bg-[#ffb4ab]/10",
    iconColor: "text-[#ffb4ab]",
    trendColor: "text-[#6bd8cb]",
  },
  {
    label: "SECURITY RATING",
    value: "98",
    suffix: "/100",
    subtext: "Excellent",
    icon: "verified_user",
    iconBg: "bg-[#6bd8cb]/10",
    iconColor: "text-[#6bd8cb]",
    progress: 98,
  },
];

const verdictStyles: Record<string, { color: string; bg: string }> = {
  Safe: { color: "#6bd8cb", bg: "rgba(107,216,203,0.12)" },
  "Critical Scam": { color: "#ffb4ab", bg: "rgba(255,180,171,0.12)" },
  Suspicious: { color: "#ffb786", bg: "rgba(255,183,134,0.12)" },
  Verified: { color: "#6bd8cb", bg: "rgba(107,216,203,0.12)" },
  "Medium Risk": { color: "#adc6ff", bg: "rgba(173,198,255,0.12)" },
};

export default function DashboardPage() {
  const stats = mockDashboardStats;

  return (
    <div className="px-4 md:px-8 py-8 max-w-6xl mx-auto">
      {/* Page heading */}
      <div className="mb-10">
        <h1 className="font-[family-name:var(--font-manrope)] font-bold text-3xl md:text-4xl text-white mb-2">
          Intelligence Dashboard
        </h1>
        <p className="text-[#c2c6d6] text-base">
          Real-time surveillance and predictive risk assessment across your digital ecosystem.
        </p>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        {statCards.map((card) => (
          <div key={card.label} className="glass-panel rounded-2xl p-6">
            <div className="flex items-start justify-between mb-4">
              <span className="text-xs font-semibold text-[#8c909f] uppercase tracking-widest">
                {card.label}
              </span>
              <div
                className={`w-10 h-10 rounded-xl ${card.iconBg} ${card.iconColor} flex items-center justify-center`}
              >
                <span className="material-symbols-outlined text-xl">{card.icon}</span>
              </div>
            </div>
            <div className="flex items-baseline gap-1 mb-1">
              <span className="font-[family-name:var(--font-manrope)] font-bold text-4xl text-white">
                {card.value}
              </span>
              {card.suffix && (
                <span className="text-[#8c909f] text-lg font-medium">{card.suffix}</span>
              )}
            </div>
            <div className="flex items-center gap-1.5">
              {card.trend === "up" && (
                <span className="material-symbols-outlined text-sm text-[#6bd8cb]">
                  trending_up
                </span>
              )}
              <span className={`text-xs ${card.trendColor ?? "text-[#6bd8cb]"}`}>
                {card.subtext}
              </span>
            </div>
            {card.progress !== undefined && (
              <div className="mt-3 h-1.5 bg-[#2a3548] rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full bg-[#6bd8cb]"
                  style={{ width: `${card.progress}%` }}
                />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Risk Analysis Breakdown */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-[family-name:var(--font-manrope)] font-semibold text-lg text-white">
              Risk Analysis Breakdown
            </h2>
            <button className="flex items-center gap-1 text-sm text-[#adc6ff] hover:text-[#bdd0ff] transition-colors">
              Details
              <span className="material-symbols-outlined text-base">arrow_forward</span>
            </button>
          </div>

          {/* Chart placeholder — Krrish can swap in a Recharts component */}
          <div className="h-48 flex items-end gap-3 mb-6 px-2">
            {[
              { label: "Safe", height: "75%", color: "#6bd8cb" },
              { label: "Neutral", height: "40%", color: "#adc6ff" },
              { label: "Critical", height: "25%", color: "#ffb4ab" },
              { label: "Verified", height: "60%", color: "#4d8eff" },
              { label: "Encrypted", height: "35%", color: "#ffb786" },
            ].map((bar) => (
              <div key={bar.label} className="flex flex-col items-center gap-2 flex-1">
                <div
                  className="w-full rounded-t-lg transition-all duration-700 hover:opacity-90"
                  style={{
                    height: bar.height,
                    background: `linear-gradient(to top, ${bar.color}90, ${bar.color}40)`,
                    border: `1px solid ${bar.color}30`,
                  }}
                />
                <span className="text-xs text-[#8c909f]">{bar.label}</span>
              </div>
            ))}
          </div>

          {/* Metrics row */}
          <div className="grid grid-cols-3 gap-4 border-t border-white/5 pt-5">
            {[
              { label: "Active Monitoring", value: "24/7 Enabled" },
              { label: "Detection Speed", value: "42ms" },
              { label: "Confidence AI", value: "99.8%" },
            ].map((metric) => (
              <div key={metric.label}>
                <p className="text-xs text-[#8c909f] mb-1">{metric.label}</p>
                <p className="font-[family-name:var(--font-manrope)] font-bold text-[#d8e3fb] text-sm">
                  {metric.value}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Scans panel */}
        <div className="glass-panel rounded-2xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-[family-name:var(--font-manrope)] font-semibold text-base text-white">
              Recent Scans
            </h2>
            <button className="text-xs text-[#adc6ff] hover:underline">
              Clear all
            </button>
          </div>

          <div className="space-y-3">
            {mockRecentScans.map((scan) => {
              const style = verdictStyles[scan.verdict] ?? {
                color: "#8c909f",
                bg: "rgba(140,144,159,0.1)",
              };
              return (
                <div
                  key={scan.id}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-[#1f2a3c] transition-colors cursor-pointer"
                >
                  <div
                    className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                    style={{ background: style.bg }}
                  >
                    <span
                      className="material-symbols-outlined text-lg"
                      style={{ color: style.color }}
                    >
                      {scan.icon}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-[#d8e3fb] text-sm font-medium truncate">
                      {scan.name}
                    </p>
                    <span
                      className="inline-block text-xs px-2 py-0.5 rounded-full mt-0.5 font-medium"
                      style={{ background: style.bg, color: style.color }}
                    >
                      {scan.verdict}
                    </span>
                  </div>
                  <span className="text-xs text-[#8c909f] shrink-0">
                    {scan.time}
                  </span>
                </div>
              );
            })}
          </div>

          <Link
            href="/history"
            className="block mt-5 text-center text-sm text-[#adc6ff] hover:text-[#bdd0ff] transition-colors"
          >
            View All Activity →
          </Link>
        </div>
      </div>

      {/* Bottom row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Guardian AI Insight */}
        <div className="glass-panel rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-[#4d8eff]/15 flex items-center justify-center">
              <span className="material-symbols-outlined text-xl text-[#4d8eff]">
                psychology
              </span>
            </div>
            <h3 className="font-[family-name:var(--font-manrope)] font-semibold text-base text-white">
              Guardian AI Insight
            </h3>
          </div>
          <p className="text-[#c2c6d6] text-sm leading-relaxed mb-6">
            &quot;We&apos;ve detected a significant{" "}
            <span className="text-[#ffb786] font-semibold">18% increase</span>{" "}
            in spear-phishing attempts targeting financial domains in your
            region. TrustLens AI has automatically updated your behavioral
            firewall to preemptively block these emerging signature patterns.&quot;
          </p>
          <div className="flex gap-3">
            <button className="flex-1 py-2.5 rounded-xl bg-[#4d8eff] text-[#002e6a] text-sm font-bold hover:bg-[#5a97ff] active:scale-95 transition-all">
              Optimize Security
            </button>
            <button className="px-5 py-2.5 rounded-xl text-[#c2c6d6] text-sm font-medium hover:bg-[#2a3548] transition-all">
              Dismiss
            </button>
          </div>
        </div>

        {/* Global Intelligence Feed */}
        <div className="glass-panel rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs font-semibold text-[#8c909f] uppercase tracking-widest">
              Global Intelligence Feed
            </h3>
            <span className="flex items-center gap-1.5 text-xs font-semibold text-[#6bd8cb]">
              <span className="w-2 h-2 rounded-full bg-[#6bd8cb] animate-pulse" />
              Live Pulse
            </span>
          </div>

          <div className="h-32 rounded-xl bg-[#081425] border border-white/5 mb-5 flex items-center justify-center relative overflow-hidden">
            <div
              className="absolute inset-0 opacity-20"
              style={{
                backgroundImage:
                  "radial-gradient(circle at 30% 60%, rgba(77,142,255,0.5) 0%, transparent 50%), radial-gradient(circle at 70% 40%, rgba(107,216,203,0.4) 0%, transparent 50%)",
              }}
            />
            <div className="relative z-10 text-center">
              <p className="text-[#6bd8cb] text-sm font-semibold animate-pulse-subtle">
                ● NETWORK ACTIVE
              </p>
            </div>
          </div>

          <div className="text-center">
            <p className="font-[family-name:var(--font-manrope)] font-bold text-lg text-white">
              Global Node Status: 100% Operational
            </p>
            <p className="text-[#8c909f] text-sm mt-1">
              Monitoring 128 global datacenters
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
