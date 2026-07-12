interface KPICardProps {
  label: string;
  value: string | number;
  accent?: "amber" | "teal";
}
 
export default function KPICard({ label, value, accent = "teal" }: KPICardProps) {
  const accentClass = accent === "amber" ? "text-amber" : "text-teal";
  return (
    <div className="rounded-xl bg-graphite p-6 shadow">
      <p className="text-sm text-gray-400">{label}</p>
      <p className={`mt-2 text-3xl font-bold ${accentClass}`}>{value}</p>
    </div>
  );
}
