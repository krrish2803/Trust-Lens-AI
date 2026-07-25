import Link from "next/link";
import Image from "next/image";

const marketingFeatures = [
  {
    icon: "shield_with_heart",
    iconBg: "bg-[#4d8eff]/15",
    iconColor: "text-[#adc6ff]",
    title: "Detect. Explain. Protect.",
    description:
      "Instant risk verdict with clear, jargon-free explanations of social engineering tricks.",
  },
  {
    icon: "payments",
    iconBg: "bg-[#6bd8cb]/15",
    iconColor: "text-[#6bd8cb]",
    title: "Tuned for Indian Scams",
    description:
      "Specialized Hinglish & regional context rules for UPI, Fake KYC, and job fraud.",
  },
  {
    icon: "crop_free",
    iconBg: "bg-[#ffb786]/15",
    iconColor: "text-[#ffb786]",
    title: "OCR Screenshot Scanning",
    description:
      "Upload suspicious payment screenshots or WhatsApp chats to reveal hidden spoofs.",
  },
];

export default function LandingPage() {
  return (
    <div className="relative px-4 md:px-8 max-w-5xl mx-auto py-8 md:py-12">
      {/* Background Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-[#4d8eff]/10 blur-[120px] pointer-events-none rounded-full" />

      {/* Landing Hero */}
      <section className="relative text-center space-y-6 max-w-3xl mx-auto mb-16">
        {/* Animated Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#4d8eff]/10 border border-[#4d8eff]/30 text-[#adc6ff] text-xs font-semibold uppercase tracking-wider animate-pulse-subtle">
          <span className="w-2 h-2 rounded-full bg-[#6bd8cb] animate-ping" />
          AI Cybersecurity Shield for India
        </div>

        {/* Tagline & Headline */}
        <h1 className="font-[family-name:var(--font-manrope)] font-extrabold text-4xl sm:text-5xl md:text-6xl text-white tracking-tight leading-[1.15]">
          Detect. Explain.{" "}
          <span className="bg-gradient-to-r from-[#adc6ff] via-[#4d8eff] to-[#6bd8cb] bg-clip-text text-transparent">
            Protect.
          </span>
        </h1>

        {/* Value Prop Copy */}
        <p className="text-[#c2c6d6] text-base sm:text-lg md:text-xl leading-relaxed max-w-2xl mx-auto font-normal">
          TrustLens AI is your intelligent scam & phishing defense assistant.
          Instantly verify suspicious links, messages, or screenshots before you click or pay.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            href="/signup"
            className="w-full sm:w-auto bg-[#4d8eff] hover:bg-[#5a97ff] text-[#00285d] font-bold text-base px-8 py-3.5 rounded-xl transition-all duration-200 shadow-xl shadow-[#4d8eff]/20 active:scale-95 flex items-center justify-center gap-2"
          >
            Get Started Free
            <span className="material-symbols-outlined text-xl">arrow_forward</span>
          </Link>
          <Link
            href="/signin"
            className="w-full sm:w-auto glass-card hover:bg-[#2a3548] text-[#d8e3fb] font-semibold text-base px-8 py-3.5 rounded-xl border border-white/10 transition-all duration-200 active:scale-95 flex items-center justify-center gap-2"
          >
            Sign In
          </Link>
        </div>

        {/* Subtext */}
        <p className="text-[#8c909f] text-xs pt-2">
          No credit card required • Instant access to scam scanner
        </p>
      </section>

      {/* Feature Cards Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        {marketingFeatures.map((feat) => (
          <div
            key={feat.title}
            className="glass-panel p-7 rounded-2xl border border-white/5 hover:border-[#adc6ff]/20 transition-all duration-300 flex flex-col justify-between group"
          >
            <div>
              <div
                className={`w-12 h-12 rounded-xl ${feat.iconBg} ${feat.iconColor} flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-200`}
              >
                <span className="material-symbols-outlined text-2xl">
                  {feat.icon}
                </span>
              </div>
              <h3 className="font-[family-name:var(--font-manrope)] font-bold text-lg text-white mb-2">
                {feat.title}
              </h3>
              <p className="text-[#c2c6d6] text-sm leading-relaxed">
                {feat.description}
              </p>
            </div>
          </div>
        ))}
      </section>

      {/* Live Threat Map Banner */}
      <section className="relative w-full aspect-video rounded-3xl overflow-hidden border border-white/5 bg-[#1f2a3c] group mb-16">
        <div
          className="absolute inset-0 opacity-50 group-hover:scale-105 transition-transform duration-700"
          style={{
            background:
              "radial-gradient(ellipse at 30% 60%, rgba(77,142,255,0.3) 0%, transparent 60%), radial-gradient(ellipse at 70% 40%, rgba(107,216,203,0.2) 0%, transparent 60%)",
          }}
        />
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `linear-gradient(rgba(173,198,255,0.15) 1px, transparent 1px),
              linear-gradient(90deg, rgba(173,198,255,0.15) 1px, transparent 1px)`,
            backgroundSize: "40px 40px",
          }}
        />

        {/* Map dots */}
        <div className="absolute inset-0 flex items-center justify-center">
          {[
            { top: "30%", left: "25%", color: "#ffb4ab", size: 10 },
            { top: "50%", left: "55%", color: "#6bd8cb", size: 8 },
            { top: "40%", left: "70%", color: "#ffb786", size: 12 },
            { top: "60%", left: "40%", color: "#ffb4ab", size: 7 },
            { top: "35%", left: "45%", color: "#6bd8cb", size: 9 },
          ].map((dot, i) => (
            <div
              key={i}
              className="absolute rounded-full animate-pulse-subtle"
              style={{
                top: dot.top,
                left: dot.left,
                width: dot.size,
                height: dot.size,
                background: dot.color,
                boxShadow: `0 0 ${dot.size * 2}px ${dot.color}`,
                animationDelay: `${i * 0.4}s`,
              }}
            />
          ))}
        </div>

        <div className="absolute inset-0 bg-gradient-to-t from-[#081425] via-transparent to-transparent" />

        <div className="absolute bottom-8 left-8 right-8 flex flex-col md:flex-row justify-between items-end gap-4">
          <div>
            <h3 className="font-[family-name:var(--font-manrope)] font-bold text-2xl md:text-3xl text-white mb-1">
              Live Threat Map
            </h3>
            <p className="text-[#c2c6d6] text-sm md:text-base">
              Monitoring scam clusters across major Indian digital payment gateways in real-time.
            </p>
          </div>
          <div className="glass-card px-5 py-3 rounded-xl shrink-0">
            <p className="text-[#6bd8cb] font-bold text-xs uppercase tracking-wider">
              Active Shield
            </p>
            <p className="font-[family-name:var(--font-manrope)] font-bold text-xl text-white">
              99.8% Accuracy
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
