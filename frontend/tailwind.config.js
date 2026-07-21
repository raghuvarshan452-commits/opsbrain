/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
  colors: {
    navy: "#0B1B2B",
    graphite: "#1E2A38",
    amber: "#F5A623",
    teal: "#2DD4BF",
  },
  boxShadow: {
    "glow-amber": "0 0 24px rgba(245,166,35,0.35)",
    "glow-teal": "0 0 24px rgba(45,212,191,0.35)",
    float: "0 20px 40px -12px rgba(0,0,0,0.5)",
  },
  keyframes: {
    drift: {
      "0%, 100%": { transform: "translate(0,0)" },
      "50%": { transform: "translate(10px,-10px)" },
    },
    pulseGlow: {
      "0%, 100%": { opacity: 0.6 },
      "50%": { opacity: 1 },
    },
  },
  animation: {
    drift: "drift 8s ease-in-out infinite",
    pulseGlow: "pulseGlow 2s ease-in-out infinite",
  },
}

  },
  plugins: [],
};