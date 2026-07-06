export default function Login() {
  return (
    <div className="flex h-screen items-center justify-center bg-navy">
      <div className="w-96 rounded-xl bg-graphite p-8 shadow-lg">
        <h1 className="mb-6 text-2xl font-bold text-amber">OpsBrain Login</h1>
        {/* TODO: wire up Supabase Auth */}
        <input className="mb-3 w-full rounded bg-navy p-2 text-white" placeholder="Email" />
        <input className="mb-4 w-full rounded bg-navy p-2 text-white" placeholder="Password" type="password" />
        <button className="w-full rounded bg-amber p-2 font-semibold text-navy">
          Sign In
        </button>
      </div>
    </div>
  );
}
