"use client";

import Link from "next/link";

export default function Hero() {
  return (
    <section className="text-center py-16 md:py-20 relative">
      {/* Radial gradient atmosphere */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 80% 60% at 50% 0%, rgba(77,142,255,0.18) 0%, transparent 70%)",
        }}
      />

      {/* AI Protection badge */}
      <div className="relative z-10 flex flex-col items-center gap-6">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#4d8eff]/10 border border-[#adc6ff]/20 text-[#adc6ff] text-sm font-medium animate-pulse-subtle">
          <span
            className="material-symbols-outlined text-[18px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            verified_user
          </span>
          AI-powered protection active
        </div>

        {/* Main tagline */}
        <h1 className="font-[family-name:var(--font-manrope)] font-bold text-5xl md:text-7xl text-white tracking-tight leading-tight">
          Detect.{" "}
          <span className="text-gradient-blue">Explain.</span>{" "}
          Protect.
        </h1>

        <p className="text-[#c2c6d6] text-lg md:text-xl max-w-2xl leading-relaxed">
          Real-time scanning and intelligence to shield you from evolving Indian
          financial fraud and digital scams.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 mt-2">
          <Link
            href="/scan"
            className="flex items-center justify-center gap-2 bg-[#adc6ff] hover:bg-[#bdd0ff] text-[#002e6a] font-bold h-14 px-8 rounded-xl transition-all duration-200 active:scale-95"
          >
            Scan Now
            <span className="material-symbols-outlined text-xl leading-none">
              arrow_forward
            </span>
          </Link>
          <Link
            href="/history"
            className="flex items-center justify-center gap-2 border border-[#424754] hover:bg-[#2a3548] text-[#d8e3fb] font-bold h-14 px-8 rounded-xl transition-all duration-200 active:scale-95"
          >
            View History
          </Link>
        </div>
      </div>
    </section>
  );
}
