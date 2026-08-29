"use client";
import { useState } from "react";

type Source = { text: string; score?: number; entity?: string };
type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim() || loading) return;
    const userMsg = input;
    setMessages((m) => [...m, { role: "user", content: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg, use_rag: true }),
      });
      const data = await res.json();
      setMessages((m) => [
        ...m,
        { role: "assistant", content: data.answer, sources: data.sources },
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Lỗi: ${err}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <h1>Chatbot Văn hóa Đà Nẵng – Huế</h1>
      <p className="subtitle">
        Demo đồ án · RAG + LoRA fine-tune Qwen2.5-7B · 100% local
      </p>

      <div className="chat-box">
        {messages.length === 0 && (
          <p style={{ color: "#999" }}>
            Hỏi về lễ hội, làng nghề, nghệ nhân, ẩm thực Đà Nẵng - Huế…
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <div>{m.content}</div>
            {m.sources && m.sources.length > 0 && (
              <details className="sources">
                <summary>Nguồn ({m.sources.length})</summary>
                {m.sources.map((s, j) => (
                  <div key={j}>• {s.text}</div>
                ))}
              </details>
            )}
          </div>
        ))}
        {loading && <p className="loading">Đang suy nghĩ…</p>}
      </div>

      <div className="input-row">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Nhập câu hỏi…"
          disabled={loading}
        />
        <button onClick={send} disabled={loading || !input.trim()}>
          Gửi
        </button>
      </div>
    </main>
  );
}
