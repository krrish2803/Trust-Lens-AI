"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import Footer from "@/components/Footer";
import PublicNavbar from "@/components/PublicNavbar";
import { isAuthenticated } from "@/services/auth";

const publicRoutes = ["/", "/signin", "/signup"];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isPublicRoute = publicRoutes.includes(pathname);

  useEffect(() => {
    if (!isPublicRoute && !isAuthenticated()) {
      router.replace("/signin");
    }
  }, [isPublicRoute, pathname, router]);

  if (isPublicRoute) {
    return (
      <>
        <PublicNavbar />
        <main id="main-content" className="pt-16 min-h-screen pb-12">{children}</main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <Sidebar />
      <main id="main-content" className="pt-16 md:pl-64 min-h-screen pb-20 md:pb-8">
        {children}
      </main>
      <Footer />
    </>
  );
}
