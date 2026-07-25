import type { Metadata } from "next";
import { Manrope, Inter, Geist_Mono } from "next/font/google";
import "./globals.css";
import AppShell from "@/components/AppShell";

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope",
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist",
  weight: ["400", "500"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "TrustLens AI — Detect. Explain. Protect.",
  description:
    "AI-powered scam and phishing detection for Indian users. Analyze suspicious links, messages, and screenshots instantly.",
  keywords: [
    "scam detection",
    "phishing",
    "UPI fraud",
    "KYC scam",
    "India cybersecurity",
    "AI security",
  ],
  openGraph: {
    title: "TrustLens AI — Detect. Explain. Protect.",
    description:
      "Real-time AI scanning to shield you from Indian financial fraud and digital scams.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`dark ${manrope.variable} ${inter.variable} ${geistMono.variable}`}
    >
      <head>
        {/* Material Symbols */}
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        />
      </head>
      <body className="bg-[#081425] text-[#d8e3fb] min-h-screen overflow-x-hidden font-[family-name:var(--font-inter)]">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:bg-[#4d8eff] focus:text-[#002e6a] focus:px-4 focus:py-2 focus:rounded-lg focus:font-semibold focus:outline-none"
        >
          Skip to main content
        </a>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
