import type {
  ScanResult,
  ScanHistoryItem,
  DashboardStats,
  RecentScanItem,
  UserProfile,
  UserSettings,
} from "@/types";

// ─── Mock Scan Result ─────────────────────────────────────────────────────

export const mockScanResult: ScanResult = {
  scanId: "SCAN-8821",
  timestamp: "2023-10-24T14:32:01Z",
  input: "https://trust-secure-kyc.io/update-now",
  type: "message",
  verdict: "HIGH_RISK",
  riskLevel: "high",
  riskScore: 88,
  confidenceScore: 94,
  category: "Fake KYC Scam",
  explanation:
    "This message uses urgent language and a suspicious link masquerading as an official verification portal. The sender's domain originates from a high-risk server cluster often associated with credential harvesting. Furthermore, the linguistic pattern analysis suggests an automated script designed to trigger anxiety and rapid decision-making.",
  originalContent:
    '"URGENT: Your account access will be terminated in 2 hours unless you complete the mandatory KYC update at: trust-secure-kyc.io"',
  actions: [
    {
      step: 1,
      title: "Do not click",
      description:
        "Clicking the link may install a keylogger or compromise your active session tokens.",
      severity: "error",
    },
    {
      step: 2,
      title: "Verify via official site",
      description:
        "Manually type the official URL in your browser or use a verified mobile application.",
      severity: "primary",
    },
    {
      step: 3,
      title: "Block sender",
      description:
        "Report this contact to your service provider to help others avoid the same threat.",
      severity: "tertiary",
    },
  ],
};

// ─── Mock History ─────────────────────────────────────────────────────────

export const mockHistory: ScanHistoryItem[] = [
  {
    scanId: "SCAN-9102",
    timestamp: "2024-01-15T14:45:00Z",
    title: "Suspicious Financial URL",
    snippet: "https://securesettle-bank-login-verify.com/update-auth/...",
    type: "link",
    verdict: "CRITICAL",
    riskLevel: "critical",
  },
  {
    scanId: "SCAN-9098",
    timestamp: "2024-01-15T11:20:00Z",
    title: "Client Message Verification",
    snippet: '"Meeting rescheduled for Friday at 3 PM. Sending invite..."',
    type: "message",
    verdict: "SAFE",
    riskLevel: "safe",
  },
  {
    scanId: "SCAN-9091",
    timestamp: "2024-01-14T17:12:00Z",
    title: "Potential Impersonation Email",
    snippet: "Sender: payroll-noreply@corp-internal-support.io",
    type: "message",
    verdict: "HIGH_RISK",
    riskLevel: "high",
  },
  {
    scanId: "SCAN-9087",
    timestamp: "2024-01-14T09:05:00Z",
    title: "Cloud Documentation Link",
    snippet: "https://docs.company-portal.net/v2/shared/project-zeus-report",
    type: "link",
    verdict: "SAFE",
    riskLevel: "safe",
  },
  {
    scanId: "SCAN-9082",
    timestamp: "2024-01-13T16:30:00Z",
    title: "Unverified SMS Sender",
    snippet:
      '"Your package delivery has been delayed. Click to view status..."',
    type: "message",
    verdict: "MEDIUM_RISK",
    riskLevel: "medium",
  },
  {
    scanId: "SCAN-9075",
    timestamp: "2024-01-13T10:15:00Z",
    title: "Prize Winner Notification",
    snippet:
      '"Congratulations! You have won Rs. 50,000. Claim now at prizeindia.co"',
    type: "message",
    verdict: "CRITICAL",
    riskLevel: "critical",
  },
];

// ─── Dashboard Stats ──────────────────────────────────────────────────────

export const mockDashboardStats: DashboardStats = {
  totalScans: 14208,
  scamsBlocked: 432,
  securityRating: 98,
  monthlyChange: 12,
};

export const mockRecentScans: RecentScanItem[] = [
  { id: "1", name: "intel-node-04.io", verdict: "Safe", time: "2m ago", icon: "language" },
  { id: "2", name: "bank-verification.co...", verdict: "Critical Scam", time: "14m ago", icon: "warning" },
  { id: "3", name: "contracts_v2.pdf", verdict: "Suspicious", time: "42m ago", icon: "description" },
  { id: "4", name: "meeting_notes.docx", verdict: "Verified", time: "1h ago", icon: "attach_file" },
];

// ─── User Profile ─────────────────────────────────────────────────────────

export const mockUserProfile: UserProfile = {
  id: "usr-001",
  fullName: "Adrian Sterling",
  email: "a.sterling@trustlens.ai",
};

export const mockUserSettings: UserSettings = {
  realtimeAlerts: true,
  biometricAuth: false,
  sessionTimeout: 30,
};
