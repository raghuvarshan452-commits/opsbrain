interface GlowButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "amber" | "glass";
  className?: string;
  disabled?: boolean;
}
 
export default function GlowButton({
  children,
  onClick,
  variant = "amber",
  className = "",
  disabled,
}: GlowButtonProps) {
  const base =
    "rounded-full px-6 py-2 font-semibold transition-all hover:-translate-y-0.5 disabled:opacity-50";
  const styles =
    variant === "amber"
      ? "bg-amber text-navy shadow-glow-amber hover:shadow-lg"
      : "border border-white/15 bg-white/10 text-white backdrop-blur-md";
 
  return (
    <button onClick={onClick} disabled={disabled} className={`${base} ${styles} ${className}`}>
      {children}
    </button>
  );
}
