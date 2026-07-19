import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../lib/supabaseClient";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError(error.message);
      return;
    }
    navigate("/");
  };

  const handleGoogleLogin = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: window.location.origin },
    });
    if (error) setError(error.message);
    // On success, Supabase redirects to Google, then back to redirectTo — no further code needed here.
  };

  return (
    <div className="flex h-screen items-center justify-center bg-navy">
      <div className="w-96 rounded-xl bg-graphite p-8 shadow-lg">
        <h1 className="mb-6 text-2xl font-bold text-amber">OpsBrain Login</h1>
        {error && <p className="mb-3 text-sm text-red-400">{error}</p>}

        <button
          onClick={handleGoogleLogin}
          className="mb-4 flex w-full items-center justify-center gap-2 rounded bg-white p-2 font-semibold text-gray-800 hover:bg-gray-100"
        >
          <svg width="18" height="18" viewBox="0 0 48 48">
            <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.9 32.7 29.4 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.5 6.1 29.5 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.7-.4-3.5z" />
            <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.5 16 18.9 13 24 13c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.5 6.1 29.5 4 24 4 16.3 4 9.6 8.3 6.3 14.7z" />
            <path fill="#4CAF50" d="M24 44c5.3 0 10.1-2 13.7-5.4l-6.3-5.3C29.4 35 26.8 36 24 36c-5.4 0-9.9-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z" />
            <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.7 2-2 3.7-3.6 4.9l6.3 5.3C39.9 36 44 30.9 44 24c0-1.3-.1-2.7-.4-3.5z" />
          </svg>
          Continue with Google
        </button>

        <div className="mb-4 flex items-center gap-3">
          <div className="h-px flex-1 bg-gray-600" />
          <span className="text-xs text-gray-500">OR</span>
          <div className="h-px flex-1 bg-gray-600" />
        </div>

        <input
          className="mb-3 w-full rounded bg-navy p-2 text-white"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="mb-4 w-full rounded bg-navy p-2 text-white"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full rounded bg-amber p-2 font-semibold text-navy"
        >
          Sign In
        </button>
      </div>
    </div>
  );
}