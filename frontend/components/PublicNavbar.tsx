"use client";

import Link from "next/link";
import Image from "next/image";

export default function PublicNavbar() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#152031]/90 backdrop-blur-md border-b border-white/5 transition-all duration-300">
      <nav aria-label="Public navigation" className="flex items-center justify-between w-full h-16 px-6 max-w-[1280px] mx-auto">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center group">
          <Image
            src="/logo.svg"
            alt="TrustLens AI"
            width={160}
            height={36}
            priority
            className="h-8 w-auto"
          />
        </Link>

        {/* Right CTA Actions */}
        <div className="flex items-center gap-3">
          <Link
            href="/signin"
            className="text-sm font-semibold text-[#c2c6d6] hover:text-white px-4 py-2 rounded-xl transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="bg-[#4d8eff] hover:bg-[#5a97ff] text-[#00285d] text-sm font-bold px-4 py-2 rounded-xl transition-all duration-200 shadow-md active:scale-95"
          >
            Get Started
          </Link>
        </div>
      </nav>
    </header>
  );
}
