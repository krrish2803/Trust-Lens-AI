"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { mockUserProfile, mockUserSettings } from "@/data/mockData";
import { logout } from "@/services/auth";

export default function SettingsPage() {
  const router = useRouter();
  const [profile] = useState(mockUserProfile);
  const [alerts, setAlerts] = useState<boolean>(mockUserSettings.realtimeAlerts ?? true);
  const [biometric, setBiometric] = useState<boolean>(mockUserSettings.biometricAuth ?? false);
  const [timeout, setTimeout_] = useState<number>(mockUserSettings.sessionTimeout ?? 30);

  const userFullName = profile.fullName || profile.name || "User";
  const avatarInitial = userFullName.trim().charAt(0).toUpperCase() || "U";

  const handleSignOut = async () => {
    try {
      await logout();
    } catch (_err) {
      console.warn("[SignOut] Executed logout stub");
    } finally {
      router.push("/");
    }
  };

  const toggleStyle = (on: boolean = false) =>
    `relative inline-flex w-12 h-6 rounded-full transition-all duration-300 cursor-pointer ${
      on ? "bg-[#4d8eff]" : "bg-[#2a3548]"
    }`;

  const knobStyle = (on: boolean = false) =>
    `absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-md transition-all duration-300 ${
      on ? "left-6" : "left-0.5"
    }`;

  return (
    <div className="px-4 md:px-8 py-8 max-w-3xl mx-auto space-y-8">
      <h1 className="font-[family-name:var(--font-manrope)] font-bold text-2xl text-white sr-only">
        Settings
      </h1>

      {/* ── Profile ────────────────────────────────────────────────────── */}
      <section>
        <h2 className="flex items-center gap-2 font-[family-name:var(--font-manrope)] font-semibold text-lg text-white mb-4">
          <span className="material-symbols-outlined text-xl text-[#adc6ff]">
            manage_accounts
          </span>
          Profile
        </h2>
        <div className="glass-panel rounded-2xl p-6 flex flex-col sm:flex-row items-start sm:items-center gap-6">
          {/* Avatar */}
          <div className="relative shrink-0">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[#4d8eff] to-[#6bd8cb] flex items-center justify-center text-[#002e6a] text-2xl font-bold">
              {avatarInitial}
            </div>
            <button
              aria-label="Edit avatar"
              className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-[#4d8eff] text-white flex items-center justify-center hover:bg-[#5a97ff] transition-colors"
            >
              <span className="material-symbols-outlined text-sm">edit</span>
            </button>
          </div>

          {/* Fields */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1 w-full">
            <div>
              <label className="block text-xs text-[#8c909f] mb-1.5 font-medium">
                Full Name
              </label>
              <input
                id="settings-full-name"
                type="text"
                defaultValue={userFullName}
                className="w-full bg-[#081425] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] rounded-xl px-4 py-2.5 text-sm outline-none transition-colors"
              />
            </div>
            <div>
              <label className="block text-xs text-[#8c909f] mb-1.5 font-medium">
                Work Email
              </label>
              <input
                id="settings-email"
                type="email"
                defaultValue={profile.email}
                className="w-full bg-[#081425] border border-[#424754] focus:border-[#4d8eff] text-[#d8e3fb] rounded-xl px-4 py-2.5 text-sm outline-none transition-colors"
              />
            </div>
          </div>
        </div>
      </section>

      {/* ── Security Alerts ──────────────────────────────────────────────── */}
      <section>
        <h2 className="flex items-center gap-2 font-[family-name:var(--font-manrope)] font-semibold text-lg text-white mb-4">
          <span className="material-symbols-outlined text-xl text-[#adc6ff]">
            shield
          </span>
          Security Alerts
        </h2>
        <div className="glass-panel rounded-2xl divide-y divide-white/5">
          {/* Real-time Detection toggle */}
          <div className="flex items-center justify-between p-5">
            <div>
              <p className="text-[#d8e3fb] text-sm font-semibold">
                Real-time Risk Detection
              </p>
              <p className="text-[#8c909f] text-xs mt-0.5">
                Receive instant push notifications for critical AI anomalies.
              </p>
            </div>
            <button
              id="toggle-realtime"
              aria-pressed={alerts}
              onClick={() => setAlerts(!alerts)}
              className={toggleStyle(alerts)}
            >
              <span className={knobStyle(alerts)} />
            </button>
          </div>

          {/* Biometric toggle */}
          <div className="flex items-center justify-between p-5">
            <div>
              <p className="text-[#d8e3fb] text-sm font-semibold">
                Biometric Authentication
              </p>
              <p className="text-[#8c909f] text-xs mt-0.5">
                Require FaceID or fingerprint for accessing sensitive reports.
              </p>
            </div>
            <button
              id="toggle-biometric"
              aria-pressed={biometric}
              onClick={() => setBiometric(!biometric)}
              className={toggleStyle(biometric)}
            >
              <span className={knobStyle(biometric)} />
            </button>
          </div>

          {/* Session timeout */}
          <div className="flex items-center justify-between p-5">
            <div>
              <p className="text-[#d8e3fb] text-sm font-semibold">
                Session Timeout
              </p>
              <p className="text-[#8c909f] text-xs mt-0.5">
                Automatically log out after periods of inactivity.
              </p>
            </div>
            <select
              id="session-timeout"
              value={timeout}
              onChange={(e) => setTimeout_(Number(e.target.value))}
              className="bg-[#2a3548] border border-[#424754] text-[#d8e3fb] text-sm rounded-xl px-3 py-2 outline-none focus:border-[#4d8eff] transition-colors cursor-pointer"
            >
              <option value={15}>15 Minutes</option>
              <option value={30}>30 Minutes</option>
              <option value={60}>1 Hour</option>
              <option value={0}>Never</option>
            </select>
          </div>
        </div>
      </section>

      {/* ── Privacy ──────────────────────────────────────────────────────── */}
      <section>
        <h2 className="flex items-center gap-2 font-[family-name:var(--font-manrope)] font-semibold text-lg text-white mb-4">
          <span className="material-symbols-outlined text-xl text-[#adc6ff]">
            privacy_tip
          </span>
          Privacy
        </h2>
        <div className="glass-panel rounded-2xl divide-y divide-white/5">
          <button className="flex items-center justify-between w-full p-5 hover:bg-[#1f2a3c]/50 transition-colors text-left">
            <div>
              <p className="text-[#d8e3fb] text-sm font-semibold">
                Data Collection Preferences
              </p>
              <p className="text-[#8c909f] text-xs mt-0.5">
                Manage how TrustLens AI utilizes your scanning history for model training.
              </p>
            </div>
            <span className="material-symbols-outlined text-[#8c909f]">
              chevron_right
            </span>
          </button>

          <div className="flex items-center justify-between p-5">
            <div>
              <p className="text-[#d8e3fb] text-sm font-semibold">
                Encrypted Storage
              </p>
              <p className="text-[#8c909f] text-xs mt-0.5">
                Currently using AES-256 end-to-end encryption for all cloud logs.
              </p>
            </div>
            <span className="material-symbols-outlined text-[#6bd8cb]">
              lock
            </span>
          </div>
        </div>
      </section>

      {/* ── About ────────────────────────────────────────────────────────── */}
      <section>
        <h2 className="flex items-center gap-2 font-[family-name:var(--font-manrope)] font-semibold text-lg text-white mb-4">
          <span className="material-symbols-outlined text-xl text-[#adc6ff]">
            info
          </span>
          About TrustLens
        </h2>
        <div className="glass-panel rounded-2xl p-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-xl bg-[#4d8eff]/15 flex items-center justify-center">
              <span
                className="material-symbols-outlined text-2xl text-[#4d8eff]"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                visibility
              </span>
            </div>
            <div>
              <p className="font-[family-name:var(--font-manrope)] font-bold text-[#d8e3fb]">
                TrustLens AI Guardian
              </p>
              <p className="text-[#8c909f] text-xs">Version 1.0.0-Beta</p>
            </div>
          </div>
          <p className="text-[#c2c6d6] text-sm leading-relaxed mb-5">
            Empowering financial intelligence with advanced AI scanning and
            guardian-level security. Designed for high-stakes environments where
            clarity and precision are non-negotiable.
          </p>
          <div className="flex gap-4 flex-wrap text-xs text-[#8c909f]">
            <button className="hover:text-[#adc6ff] transition-colors">
              Terms of Service
            </button>
            <span className="text-[#424754]">·</span>
            <button className="hover:text-[#adc6ff] transition-colors">
              Privacy Policy
            </button>
            <span className="text-[#424754]">·</span>
            <button className="hover:text-[#adc6ff] transition-colors">
              Licenses
            </button>
          </div>
        </div>
      </section>

      {/* Sign Out */}
      <button
        id="sign-out-btn"
        onClick={handleSignOut}
        className="w-full glass-card rounded-2xl py-4 flex items-center justify-center gap-2 text-[#ffb4ab] text-sm font-semibold hover:bg-[#ffb4ab]/5 active:scale-[0.99] transition-all duration-200 border border-[#ffb4ab]/15 cursor-pointer"
      >
        <span className="material-symbols-outlined text-xl">logout</span>
        Sign Out of Account
      </button>
    </div>
  );
}
