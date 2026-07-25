"use client";

import { memo, useEffect, useRef } from "react";
import { getRiskLevel, getRiskStrokeColor } from "@/utils/riskUtils";

interface RiskMeterProps {
  score: number; // 0–100
}

function RiskMeterInner({ score }: RiskMeterProps) {
  const circleRef = useRef<SVGCircleElement>(null);
  const riskLevel = getRiskLevel(score);
  const strokeColor = getRiskStrokeColor(riskLevel);

  const radius = 88;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - score / 100);

  useEffect(() => {
    if (!circleRef.current) return;

    circleRef.current.style.strokeDashoffset = String(circumference);
    circleRef.current.style.transition = "none";

    let cancelled = false;
    let raf1: number;
    let raf2: number;

    raf1 = requestAnimationFrame(() => {
      raf2 = requestAnimationFrame(() => {
        if (!cancelled && circleRef.current) {
          circleRef.current.style.transition =
            "stroke-dashoffset 1.4s cubic-bezier(0.34,1.56,0.64,1)";
          circleRef.current.style.strokeDashoffset = String(offset);
        }
      });
    });

    return () => {
      cancelled = true;
      cancelAnimationFrame(raf1);
      cancelAnimationFrame(raf2);
    };
  }, [score, offset, circumference]);

  const getRiskLevelLabel = () => {
    if (score < 20) return "Safe";
    if (score < 40) return "Low";
    if (score < 60) return "Medium";
    if (score < 80) return "High";
    return "Critical";
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative w-48 h-48">
        <svg
          className="w-full h-full -rotate-90"
          viewBox="0 0 192 192"
          role="img"
          aria-label={`Risk score: ${score} percent — ${getRiskLevelLabel()} Risk`}
        >
          <circle
            cx="96"
            cy="96"
            r={radius}
            fill="transparent"
            stroke="#2a3548"
            strokeWidth="14"
          />
          <circle
            ref={circleRef}
            cx="96"
            cy="96"
            r={radius}
            fill="transparent"
            stroke={strokeColor}
            strokeWidth="14"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ filter: `drop-shadow(0 0 8px ${strokeColor}40)` }}
          />
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="font-[family-name:var(--font-manrope)] font-bold text-4xl"
            style={{ color: strokeColor }}
          >
            {score}%
          </span>
          <span className="text-[#8c909f] text-xs uppercase tracking-widest font-medium mt-1">
            Risk Score
          </span>
        </div>
      </div>

      <div
        className="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider"
        style={{
          background: `${strokeColor}18`,
          color: strokeColor,
          border: `1px solid ${strokeColor}35`,
        }}
      >
        {getRiskLevelLabel()} Risk
      </div>
    </div>
  );
}

const RiskMeter = memo(RiskMeterInner);
export default RiskMeter;
