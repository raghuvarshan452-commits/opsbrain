import GlassPanel from "../spatial/GlassPanel";
 
interface KPICardProps {
  label: string;
  value: string | number;
  accent?: "amber" | "teal";
}
 
export default function KPICard({ label, value, accent = "teal" }: KPICardProps) {
  const accentClass = accent === "amber" ? "text-amber" : "text-teal";
  return (
    <GlassPanel glow={accent} className="p-6">
      <p className="text-sm text-gray-400">{label}</p>
      <p className={`mt-2 text-3xl font-bold ${accentClass}`}>{value}</p>
    </GlassPanel>
  );
}

