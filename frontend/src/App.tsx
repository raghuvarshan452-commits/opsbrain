import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Copilot from "./pages/Copilot";
import GraphExplorer from "./pages/GraphExplorer";
import Compliance from "./pages/Compliance";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import Upload from "./pages/Upload";
 
const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/upload", label: "Upload" },
  { to: "/copilot", label: "Copilot" },
  { to: "/graph", label: "Knowledge Graph" },
  { to: "/compliance", label: "Compliance" },
  { to: "/analytics", label: "Analytics" },
  { to: "/settings", label: "Settings" },
];
 

 
function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-navy">
      <aside className="w-56 bg-graphite p-4">
        <h2 className="mb-8 text-xl font-bold text-teal">OpsBrain</h2>
        <nav className="flex flex-col gap-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className="rounded px-3 py-2 text-gray-300 hover:bg-navy hover:text-amber"
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="flex-1">{children}</main>
    </div>
  );
}
 
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Shell><Dashboard /></Shell>} />
        <Route path="/copilot" element={<Shell><Copilot /></Shell>} />
        <Route path="/graph" element={<Shell><GraphExplorer /></Shell>} />
        <Route path="/compliance" element={<Shell><Compliance /></Shell>} />
        <Route path="/analytics" element={<Shell><Analytics /></Shell>} />
        <Route path="/settings" element={<Shell><Settings /></Shell>} />
        <Route path="/upload" element={<Shell><Upload /></Shell>} />
      </Routes>
    </BrowserRouter>
  );
}
