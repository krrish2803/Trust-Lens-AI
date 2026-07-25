"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { DashboardIcon, SettingsIcon } from "@/components/icons/BrandIcons";

// Nav items — "home", "history" keep Material Symbols; Dashboard + Settings use brand icons
const navItems = [
  { href: "/home", label: "Home", materialIcon: "home", brandIcon: null },
  { href: "/history", label: "History", materialIcon: "history", brandIcon: null },
  { href: "/dashboard", label: "Dashboard", materialIcon: null, brandIcon: "dashboard" },
  { href: "/settings", label: "Settings", materialIcon: null, brandIcon: "settings" },
] as const;

const bottomItems = [
  { href: "/settings", label: "Profile", icon: "account_circle" },
  { href: "/home", label: "Support", icon: "help" },
];

export default function Sidebar() {
  const pathname = usePathname();

  const isActive = (href: string) => pathname.startsWith(href);

  return (
    <aside className="hidden md:flex flex-col fixed left-0 top-16 h-[calc(100vh-64px)] w-64 bg-[#111c2d] border-r border-white/5 p-6 z-40">
      {/* Nav items */}
      <nav className="flex flex-col gap-1 mb-6" aria-label="Main navigation">
        {navItems.map((item) => {
          const active = isActive(item.href);
          const iconColor = active ? "#00302b" : "#c2c6d6";
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                active
                  ? "bg-[#29a195] text-[#00302b]"
                  : "text-[#c2c6d6] hover:bg-[#2a3548] hover:text-[#d8e3fb]"
              }`}
            >
              {/* Brand icon for Dashboard and Settings, Material Symbol for others */}
              {item.brandIcon === "dashboard" ? (
                <DashboardIcon size={20} color={iconColor} />
              ) : item.brandIcon === "settings" ? (
                <SettingsIcon size={20} color={iconColor} />
              ) : (
                <span className="material-symbols-outlined text-xl leading-none">
                  {item.materialIcon}
                </span>
              )}
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* New Scan CTA */}
      <Link
        href="/scan"
        className="flex items-center justify-center gap-2 bg-[#4d8eff] hover:bg-[#5a97ff] text-[#00285d] font-bold py-3.5 rounded-xl transition-all duration-200 active:scale-95 mb-auto"
      >
        <span className="material-symbols-outlined text-xl leading-none">
          shield
        </span>
        New Scan
      </Link>

      {/* Bottom items */}
      <div className="flex flex-col gap-1 border-t border-white/5 pt-4 mt-4">
        {bottomItems.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className="flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm text-[#c2c6d6] hover:bg-[#2a3548] hover:text-[#d8e3fb] transition-all duration-200"
          >
            <span className="material-symbols-outlined text-xl leading-none">
              {item.icon}
            </span>
            {item.label}
          </Link>
        ))}
      </div>
    </aside>
  );
}
