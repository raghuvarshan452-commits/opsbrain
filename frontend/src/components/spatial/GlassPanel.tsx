import type { ReactNode } from "react";
interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  glow?: "amber" | "teal" | "none";
}
 
export default function GlassPanel({ children, className = "", glow = "none" }: GlassPanelProps) {
  const glowClass =
    glow === "amber" ? "shadow-glow-amber" : glow === "teal" ? "shadow-glow-teal" : "shadow-float";
 
  return (
    <div
      className={`rounded-2xl border border-white/10 bg-white/[0.06] backdrop-blur-xl transition-transform hover:-translate-y-1 ${glowClass} ${className}`}
    >
      {children}
    </div>
  );
}