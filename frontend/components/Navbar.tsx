"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Image from "next/image";
import { logout } from "@/services/auth";

const navLinks = [
  { href: "/home", label: "Home" },
  { href: "/history", label: "History" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/settings", label: "Settings" },
];

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleSignOut = async () => {
    try {
      await logout();
    } catch (_err) {
      console.warn("[SignOut] Executed logout stub");
    } finally {
      router.push("/");
    }
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#152031]/90 backdrop-blur-md border-b border-white/5 transition-all duration-300">
      <nav className="flex items-center justify-between w-full h-16 px-6 max-w-[1280px] mx-auto">
        {/* Logo — brand SVG wordmark */}
        <Link href="/home" className="flex items-center group">
          <Image
            src="/logo.svg"
            alt="TrustLens AI"
            width={160}
            height={36}
            priority
            className="h-8 w-auto"
          />
        </Link>

        {/* Desktop Nav Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => {
            const isActive = pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`font-medium text-sm transition-all duration-200 pb-0.5 ${
                  isActive
                    ? "text-[#adc6ff] border-b-2 border-[#adc6ff]"
                    : "text-[#c2c6d6] hover:text-[#adc6ff]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Right actions */}
        <div className="flex items-center gap-3">
          <Link
            href="/settings"
            aria-label="Account Settings"
            className="text-[#c2c6d6] hover:text-[#adc6ff] transition-colors flex items-center p-1 rounded-lg hover:bg-white/5"
            title="Account Settings"
          >
            <span className="material-symbols-outlined text-2xl">
              account_circle
            </span>
          </Link>

          {/* Sign Out Button */}
          <button
            onClick={handleSignOut}
            aria-label="Sign Out"
            title="Sign Out"
            className="text-[#c2c6d6] hover:text-[#ffb4ab] transition-colors flex items-center p-1 rounded-lg hover:bg-white/5 cursor-pointer"
          >
            <span className="material-symbols-outlined text-2xl">
              logout
            </span>
          </button>
        </div>
      </nav>
    </header>
  );
}
