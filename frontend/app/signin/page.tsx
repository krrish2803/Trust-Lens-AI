"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { login } from "@/services/auth";

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError("Please fill in all fields.");
      return;
    }
    if (!email.includes("@") || !email.includes(".")) {
      setError("Please enter a valid email address.");
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
      router.push("/home");
    } catch (_err) {
      setError("Sign-in failed. Please check your credentials and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center px-4 py-12">
      <div className="glass-panel w-full max-w-md p-8 rounded-2xl border border-white/10 shadow-2xl space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <Link href="/" className="inline-block mb-2">
            <Image
              src="/logo.svg"
              alt="TrustLens AI"
              width={160}
              height={36}
              priority
              className="h-8 w-auto mx-auto"
            />
          </Link>
          <h1 className="font-[family-name:var(--font-manrope)] font-bold text-2xl text-white">
            Welcome Back
          </h1>
          <p className="text-[#c2c6d6] text-sm">
            Sign in to access your scam detection dashboard.
          </p>
        </div>

        {/* Error notification */}
        {error && (
          <div className="bg-[#ffb4ab]/15 border border-[#ffb4ab]/30 rounded-xl p-3.5 text-xs text-[#ffb4ab] flex items-center gap-2">
            <span className="material-symbols-outlined text-base shrink-0">
              error
            </span>
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="signin-email"
              className="block text-xs font-semibold uppercase tracking-wider text-[#8c909f] mb-1.5"
            >
              Email Address
            </label>
            <input
              id="signin-email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-[#152031] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3 text-sm outline-none transition-colors"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label
                htmlFor="signin-password"
                className="block text-xs font-semibold uppercase tracking-wider text-[#8c909f]"
              >
                Password
              </label>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  alert("Password reset is not configured in demo mode.");
                }}
                className="text-xs font-medium text-[#6bd8cb] hover:underline"
              >
                Forgot password?
              </a>
            </div>
            <input
              id="signin-password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-[#152031] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3 text-sm outline-none transition-colors"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#4d8eff] hover:bg-[#5a97ff] text-[#00285d] font-bold text-sm py-3.5 rounded-xl transition-all duration-200 shadow-lg active:scale-95 flex items-center justify-center gap-2 mt-6 disabled:opacity-50"
          >
            {loading ? (
              <>
                <span className="w-4 h-4 rounded-full border-2 border-[#00285d] border-t-transparent animate-spin" />
                Signing in...
              </>
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        {/* Footer link */}
        <div className="text-center pt-2 border-t border-white/5">
          <p className="text-xs text-[#8c909f]">
            Don&apos;t have an account?{" "}
            <Link
              href="/signup"
              className="text-[#4d8eff] font-semibold hover:underline"
            >
              Sign Up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
