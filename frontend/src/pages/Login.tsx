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
 
  return (
    <div className="flex h-screen items-center justify-center bg-navy">
      <div className="w-96 rounded-xl bg-graphite p-8 shadow-lg">
        <h1 className="mb-6 text-2xl font-bold text-amber">OpsBrain Login</h1>
        {error && <p className="mb-3 text-sm text-red-400">{error}</p>}
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
