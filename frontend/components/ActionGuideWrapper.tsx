"use client";

import ActionGuide from "@/components/ActionGuide";
import type { ActionStep } from "@/types";
import { useRouter } from "next/navigation";

interface ActionGuideWrapperProps {
  actions: ActionStep[];
  confidenceScore: number;
}

export default function ActionGuideWrapper({
  actions,
  confidenceScore,
}: ActionGuideWrapperProps) {
  const router = useRouter();

  const handleDownload = () => {
    alert("Download report — coming soon");
  };

  const handleDismiss = () => {
    router.back();
  };

  return (
    <ActionGuide
      actions={actions}
      confidenceScore={confidenceScore}
      onDownload={handleDownload}
      onDismiss={handleDismiss}
    />
  );
}
