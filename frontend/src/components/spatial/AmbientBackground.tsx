export default function AmbientBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-navy">
      <div className="absolute -left-32 -top-32 h-96 w-96 animate-drift rounded-full bg-amber/10 blur-3xl" />
      <div
        className="absolute -bottom-32 -right-32 h-96 w-96 animate-drift rounded-full bg-teal/10 blur-3xl"
        style={{ animationDelay: "3s" }}
      />
    </div>
  );
}
