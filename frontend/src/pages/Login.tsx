import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../lib/supabaseClient";
import GlassPanel from "../components/spatial/GlassPanel";
import GlowButton from "../components/spatial/GlowButton";
 
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
  };
 
  return (
    <div className="flex h-screen items-center justify-center">
      <GlassPanel className="w-96 p-8">
        <h1 className="mb-6 text-center text-2xl font-bold text-teal">OpsBrain</h1>
        {error && <p className="mb-3 text-sm text-red-400">{error}</p>}
 
        <GlowButton variant="glass" onClick={handleGoogleLogin} className="mb-4 w-full">
          Continue with Google
        </GlowButton>
 
        <div className="mb-4 flex items-center gap-3">
          <div className="h-px flex-1 bg-white/10" />
          <span className="text-xs text-gray-400">OR</span>
          <div className="h-px flex-1 bg-white/10" />
        </div>
 
        <input
          className="mb-3 w-full rounded-xl border border-white/10 bg-white/5 p-3 text-white placeholder-gray-500 backdrop-blur-md focus:border-amber/50 focus:outline-none"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="mb-5 w-full rounded-xl border border-white/10 bg-white/5 p-3 text-white placeholder-gray-500 backdrop-blur-md focus:border-amber/50 focus:outline-none"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <GlowButton onClick={handleLogin} className="w-full">
          Sign In
        </GlowButton>
      </GlassPanel>
    </div>
  );
}
