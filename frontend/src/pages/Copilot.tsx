import { useState, useRef, useEffect } from "react";
import ChatMessage from "../components/chat/ChatMessage";
import { askCopilot } from "../services/api";
 
interface Message {
  role: "user" | "assistant";
  text: string;
  confidence?: number;
  citations?: { document: string; snippet: string }[];
  trace?: { agent: string; action: string }[];
}
 
export default function Copilot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
 
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
 
  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage: Message = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
 
    try {
      const res = await askCopilot(userMessage.text);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.data.answer,
          confidence: res.data.confidence,
          citations: res.data.citations,
          trace: res.data.trace,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Something went wrong reaching the Copilot. Please try again." },
      ]);
    }
    setLoading(false);
  };
 
  return (
    <div className="flex h-full flex-col p-8">
      <h1 className="mb-4 text-3xl font-bold text-amber">Expert Copilot</h1>
      <div className="flex-1 overflow-y-auto rounded-xl bg-navy p-4">
        {messages.map((m, i) => (
          <ChatMessage
            key={i}
            role={m.role}
            text={m.text}
            confidence={m.confidence}
            citations={m.citations}
            trace={m.trace}
          />
        ))}
        {loading && <p className="text-sm text-gray-400">Copilot is thinking...</p>}
        <div ref={bottomRef} />
      </div>
      <div className="mt-4 flex gap-2">
        <input
          className="flex-1 rounded bg-graphite p-3 text-white"
          placeholder="Ask a question about your ingested documents..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} className="rounded bg-amber px-6 font-semibold text-navy">
          Send
        </button>
      </div>
    </div>
  );
}
