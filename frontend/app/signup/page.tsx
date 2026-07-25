"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { signup } from "@/services/auth";

export default function SignUpPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Basic client validation
    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill in all fields.");
      return;
    }
    if (!email.includes("@") || !email.includes(".")) {
      setError("Please enter a valid email address.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await signup(name, email, password);
      // On success, redirect to authenticated home /home per Option B routing
      router.push("/home");
    } catch (err: any) {
      setError(err?.message || "Failed to create account. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-12">
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
            Create Your Account
          </h1>
          <p className="text-[#c2c6d6] text-sm">
            Join TrustLens AI to protect your digital transactions.
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
              htmlFor="signup-name"
              className="block text-xs font-semibold uppercase tracking-wider text-[#8c909f] mb-1.5"
            >
              Full Name
            </label>
            <input
              id="signup-name"
              type="text"
              placeholder="Muskan Sharma"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-[#152031] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3 text-sm outline-none transition-colors"
            />
          </div>

          <div>
            <label
              htmlFor="signup-email"
              className="block text-xs font-semibold uppercase tracking-wider text-[#8c909f] mb-1.5"
            >
              Email Address
            </label>
            <input
              id="signup-email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-[#152031] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3 text-sm outline-none transition-colors"
            />
          </div>

          <div>
            <label
              htmlFor="signup-password"
              className="block text-xs font-semibold uppercase tracking-wider text-[#8c909f] mb-1.5"
            >
              Password
            </label>
            <input
              id="signup-password"
              type="password"
              placeholder="Minimum 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-[#152031] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] placeholder-[#424754] rounded-xl px-4 py-3 text-sm outline-none transition-colors"
            />
          </div>

          <div>
            <label
              htmlFor="signup-confirm-password"
              className="block text-xs font-semibold uppercase tracking-wider text-[#8c909f] mb-1.5"
            >
              Confirm Password
            </label>
            <input
              id="signup-confirm-password"
              type="password"
              placeholder="Repeat your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
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
                Creating account...
              </>
            ) : (
              "Create Account"
            )}
          </button>
        </form>

        {/* Footer link */}
        <div className="text-center pt-2 border-t border-white/5">
          <p className="text-xs text-[#8c909f]">
            Already have an account?{" "}
            <Link
              href="/signin"
              className="text-[#4d8eff] font-semibold hover:underline"
            >
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
