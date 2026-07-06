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
    },
  },
  plugins: [],
};