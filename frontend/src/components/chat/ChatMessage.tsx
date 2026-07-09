interface Citation {
  document: string;
  snippet: string;
}

interface ChatMessageProps {
  role: "user" | "assistant";
  text: string;
  confidence?: number;
  citations?: Citation[];
}

export default function ChatMessage({ role, text, confidence, citations }: ChatMessageProps) {
  const isUser = role === "user";
  return (
    <div className={`mb-4 flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-lg rounded-xl p-4 ${
          isUser ? "bg-amber text-navy" : "bg-graphite text-gray-100"
        }`}
      >
        <p>{text}</p>
        {confidence !== undefined && (
          <p className="mt-2 text-xs text-teal">Confidence: {(confidence * 100).toFixed(0)}%</p>
        )}
        {citations && citations.length > 0 && (
          <div className="mt-2 space-y-1 border-t border-gray-600 pt-2">
            {citations.map((c, i) => (
              <p key={i} className="text-xs text-gray-400">
                📎 {c.document} — "{c.snippet}"
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}