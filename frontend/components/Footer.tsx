"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { DashboardIcon } from "@/components/icons/BrandIcons";

// Home + History + Scan keep Material Symbols; Dashboard uses brand icon
const navItems = [
  { href: "/home", label: "Home", materialIcon: "home", brandIcon: null },
  { href: "/history", label: "History", materialIcon: "history", brandIcon: null },
  { href: "/dashboard", label: "Dashboard", materialIcon: null, brandIcon: "dashboard" },
  { href: "/scan", label: "Scan", materialIcon: "radar", brandIcon: null },
] as const;

export default function Footer() {
  const pathname = usePathname();

  const isActive = (href: string) => pathname.startsWith(href);

  return (
    <footer className="md:hidden">
      <nav
        className="fixed bottom-0 left-0 right-0 z-50 bg-[#2a3548]/95 backdrop-blur-md border-t border-white/5 rounded-t-2xl shadow-2xl"
        aria-label="Mobile navigation"
      >
        <div className="flex justify-around items-center px-2 py-2">
          {navItems.map((item) => {
            const active = isActive(item.href);
            const iconColor = active ? "#adc6ff" : "#8c909f";
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex flex-col items-center justify-center gap-0.5 px-4 py-1.5 rounded-xl text-xs font-medium transition-all duration-150 active:scale-90 ${
                  active
                    ? "bg-[#4d8eff]/20 text-[#adc6ff]"
                    : "text-[#8c909f] hover:text-[#c2c6d6]"
                }`}
              >
                {item.brandIcon === "dashboard" ? (
                  <DashboardIcon size={20} color={iconColor} />
                ) : (
                  <span className="material-symbols-outlined text-xl leading-none">
                    {item.materialIcon}
                  </span>
                )}
                {item.label}
              </Link>
            );
          })}
        </div>
      </nav>
    </footer>
  );
}
