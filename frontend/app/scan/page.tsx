import UploadBox from "@/components/UploadBox";

export const metadata = {
  title: "New Scan — TrustLens AI",
  description: "Submit a suspicious link, message, or screenshot for AI-powered threat analysis.",
};

export default function ScanPage() {
  return (
    <div className="px-4 md:px-8 py-8 max-w-4xl mx-auto">
      {/* Page heading */}
      <div className="mb-10 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#2a3548] text-[#c2c6d6] text-xs font-medium mb-4">
          <span className="w-2 h-2 rounded-full bg-[#6bd8cb] animate-pulse" />
          Guardian AI · Status: Protecting Active Session
        </div>
        <h1 className="font-[family-name:var(--font-manrope)] font-bold text-3xl md:text-4xl text-white mb-3">
          Guardian Intelligence Scan
        </h1>
        <p className="text-[#c2c6d6] text-base md:text-lg max-w-xl mx-auto leading-relaxed">
          Upload or paste suspicious content to evaluate potential threats with
          AI-driven risk assessment.
        </p>
      </div>

      {/* Scan input */}
      <UploadBox />
    </div>
  );
}
