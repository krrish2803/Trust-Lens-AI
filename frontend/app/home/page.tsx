import Hero from "@/components/Hero";
import ScanCard from "@/components/ScanCard";

const scanOptions = [
  {
    icon: "link",
    title: "Paste Link",
    description:
      "Analyze suspicious URLs, shorteners, or phishing sites.",
    ctaLabel: "Analyze URL",
    href: "/scan?tab=link",
    recommended: false,
    iconBg: "bg-[#2a3548]",
    iconColor: "text-[#adc6ff]",
  },
  {
    icon: "chat",
    title: "Paste Message",
    description:
      "Scan SMS, WhatsApp texts, or email content for social engineering.",
    ctaLabel: "Verify Text",
    href: "/scan?tab=message",
    recommended: true,
    iconBg: "bg-[#4d8eff]",
    iconColor: "text-[#002e6a]",
  },
  {
    icon: "screenshot_region",
    title: "Upload Screenshot",
    description:
      "OCR-powered detection for payment receipts and UI spoofs.",
    ctaLabel: "Analyze Image",
    href: "/scan?tab=screenshot",
    recommended: false,
    iconBg: "bg-[#2a3548]",
    iconColor: "text-[#adc6ff]",
  },
];

const trustIndicators = [
  {
    icon: "policy",
    iconBg: "bg-[#6bd8cb]/10",
    iconColor: "text-[#6bd8cb]",
    title: "100+ Scam Patterns",
    description:
      "Specifically tuned for UPI, banking, and KYC fraud common in India.",
  },
  {
    icon: "psychology",
    iconBg: "bg-[#adc6ff]/10",
    iconColor: "text-[#adc6ff]",
    title: "Guardian Intel",
    description:
      "Deep learning analysis that explains exactly why a request is suspicious.",
  },
];

export default function HomePage() {
  return (
    <div className="relative px-4 md:px-8 max-w-5xl mx-auto">
      {/* Hero */}
      <Hero />

      {/* Trust Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-16">
        {trustIndicators.map((item) => (
          <div
            key={item.title}
            className="glass-card p-6 rounded-2xl flex items-center gap-5 hover:border-white/10 transition-all duration-200"
          >
            <div
              className={`w-12 h-12 rounded-xl ${item.iconBg} ${item.iconColor} flex items-center justify-center shrink-0`}
            >
              <span className="material-symbols-outlined text-2xl">
                {item.icon}
              </span>
            </div>
            <div>
              <h3 className="font-[family-name:var(--font-manrope)] font-semibold text-base text-white mb-1">
                {item.title}
              </h3>
              <p className="text-[#c2c6d6] text-sm leading-relaxed">
                {item.description}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Input Options Bento */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-16">
        {scanOptions.map((opt) => (
          <ScanCard key={opt.title} {...opt} />
        ))}
      </div>

      {/* Live Threat Map Banner */}
      <div className="relative w-full aspect-video rounded-3xl overflow-hidden border border-white/5 bg-[#1f2a3c] group mb-16">
        {/* Gradient overlay image placeholder */}
        <div
          className="absolute inset-0 opacity-50 group-hover:scale-105 transition-transform duration-700"
          style={{
            background:
              "radial-gradient(ellipse at 30% 60%, rgba(77,142,255,0.3) 0%, transparent 60%), radial-gradient(ellipse at 70% 40%, rgba(107,216,203,0.2) 0%, transparent 60%)",
          }}
        />
        {/* Animated grid lines */}
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

        {/* Bottom gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#081425] via-transparent to-transparent" />

        {/* Content */}
        <div className="absolute bottom-8 left-8 right-8 flex flex-col md:flex-row justify-between items-end gap-4">
          <div>
            <h3 className="font-[family-name:var(--font-manrope)] font-bold text-2xl md:text-3xl text-white mb-1">
              Live Threat Map
            </h3>
            <p className="text-[#c2c6d6] text-sm md:text-base">
              Monitoring scam clusters across major Indian digital payment
              gateways in real-time.
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
      </div>
    </div>
  );
}
