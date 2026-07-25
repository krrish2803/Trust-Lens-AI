"use client";

import { usePathname } from "next/navigation";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import Footer from "@/components/Footer";
import PublicNavbar from "@/components/PublicNavbar";

const publicRoutes = ["/", "/signin", "/signup"];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isPublicRoute = publicRoutes.includes(pathname);

  if (isPublicRoute) {
    return (
      <>
        <PublicNavbar />
        <main className="pt-16 min-h-screen pb-12">{children}</main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <Sidebar />
      <main className="pt-16 md:pl-64 min-h-screen pb-20 md:pb-8">
        {children}
      </main>
      <Footer />
    </>
  );
}
