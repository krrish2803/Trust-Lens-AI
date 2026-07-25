/**
 * BrandIcons.tsx
 * Inline SVG components for all TrustLens AI brand icons.
 * Extracted directly from trustlens_ai_branding icon code files
 *
 * Usage:
 *   <CriticalAlertIcon size={20} />
 *   <SafeVerdictIcon className="w-5 h-5" />
 *
 * All icons render at 24×24 by default (matching Material Symbols sizing).
 * Pass `size` (px number) or `className` to override dimensions.
 * Pass `color` to override the baked-in brand color.
 */

interface IconProps {
  size?: number;
  className?: string;
  color?: string;
}

// ─── Critical Alert — Circle with ✕, Error Red #ffb4ab ────────────────────

export function CriticalAlertIcon({
  size = 24,
  className,
  color = "#ffb4ab",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <circle cx="12" cy="12" r="10" />
      <line x1="15" y1="9" x2="9" y2="15" />
      <line x1="9" y1="9" x2="15" y2="15" />
    </svg>
  );
}

// ─── Safe Verdict — Shield with ✓, Teal #6bd8cb ───────────────────────────

export function SafeVerdictIcon({
  size = 24,
  className,
  color = "#6bd8cb",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <polyline points="9 11 11 13 15 9" />
    </svg>
  );
}

// ─── Risky Warning — Triangle with !, Amber #ffb786 ───────────────────────

export function RiskyWarningIcon({
  size = 24,
  className,
  color = "#ffb786",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  );
}

// ─── Fingerprint — Arc swirl, Primary Blue #adc6ff ────────────────────────

export function FingerprintIcon({
  size = 24,
  className,
  color = "#adc6ff",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <path d="M2 12a10 10 0 0 1 10-10" />
      <path d="M7 10a10 10 0 0 1 10 10" />
      <path d="M12 22a10 10 0 0 1-10-10" />
      <path d="M17 14a10 10 0 0 1-10-10" />
      <path d="M9 12c0-1.66 1.34-3 3-3s3 1.34 3 3" />
    </svg>
  );
}

// ─── Dashboard — Layout grid, Primary Blue #adc6ff ────────────────────────

export function DashboardIcon({
  size = 24,
  className,
  color = "#adc6ff",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="3" y1="9" x2="21" y2="9" />
      <line x1="9" y1="21" x2="9" y2="9" />
    </svg>
  );
}

// ─── Settings — Gear/cog, Primary Blue #adc6ff ────────────────────────────

export function SettingsIcon({
  size = 24,
  className,
  color = "#adc6ff",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  );
}

// ─── Screenshot Scan — Image frame, Primary Blue #adc6ff ──────────────────

export function ScreenshotScanIcon({
  size = 24,
  className,
  color = "#adc6ff",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      width={size}
      height={size}
      className={className}
      aria-hidden="true"
    >
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <circle cx="8.5" cy="8.5" r="1.5" />
      <polyline points="21 15 16 10 5 21" />
    </svg>
  );
}

// ─── Brand Logo Mark — Shield + eye (icon-only, no text) ─────────────────

export function LogoMark({
  size = 32,
  className,
}: Omit<IconProps, "color">) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 32 32"
      fill="none"
      width={size}
      height={size}
      className={className}
      aria-label="TrustLens AI"
      role="img"
    >
      <path
        d="M16 2L28 6V18C28 25.5 22 30 16 32C10 30 4 25.5 4 18V6L16 2Z"
        fill="#adc6ff18"
        stroke="#adc6ff"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <ellipse cx="16" cy="19" rx="6" ry="4" stroke="#adc6ff" strokeWidth="1.2" />
      <circle cx="16" cy="19" r="2" fill="#adc6ff" />
      <line x1="20.5" y1="15.5" x2="21.8" y2="14.2" stroke="#adc6ff" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}
