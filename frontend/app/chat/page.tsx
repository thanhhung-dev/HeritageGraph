"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { SettingOutlined, QuestionCircleOutlined } from "@ant-design/icons";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Array<{ doc?: string; url?: string; heading?: string }>;
}

const SUGGESTIONS = [
  "Lăng Tự Đức được xây dựng năm nào?",
  "Cao lầu là món gì?",
  "Festival Huế tổ chức mấy năm một lần?",
  "Làng Non Nước nổi tiếng về gì?",
  "Nhã nhạc cung đình Huế có gì đặc biệt?",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const hasMessages = messages.length > 0;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = useCallback(
    async (text?: string) => {
      const userMsg = text || input;
      if (!userMsg.trim() || loading) return;

      const newUserMsg: Message = {
        id: Date.now().toString(),
        role: "user",
        content: userMsg,
      };
      setMessages((m) => [...m, newUserMsg]);
      setInput("");
      setLoading(true);

      try {
        const res = await fetch("http://localhost:8000/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userMsg, use_rag: true }),
        });
        const data = await res.json();
        const botMsg: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        };
        setMessages((m) => [...m, botMsg]);
      } catch {
        setMessages((m) => [
          ...m,
          {
            id: (Date.now() + 1).toString(),
            role: "assistant",
            content: "Đã xảy ra lỗi khi kết nối tới máy chủ.",
          },
        ]);
      } finally {
        setLoading(false);
      }
    },
    [input, loading]
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="app">
      {/* Top bar */}
      <div className="topbar">
        <div className="topbar-actions">
          <button className="btn-icon" aria-label="Cài đặt">
            <SettingOutlined style={{ fontSize: 18 }} />
          </button>
          <button className="btn-icon" aria-label="Quyền riêng tư">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M22 13.5V10.5L18.6914 8.13674L18.2991 4.08973L15.701 2.58973L12 4.27343L8.29904 2.58975L5.70096 4.08975L5.3086 8.13672L2 10.5V12V13.5L5.30858 15.8633L5.70095 19.9103L8.29903 21.4103L12 19.7266L15.701 21.4103L18.299 19.9103L18.6914 15.8633L22 13.5Z" strokeLinecap="square" />
              <path d="M15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12Z" />
            </svg>
          </button>
        </div>
        <div className="topbar-auth">
          <button className="btn-ghost">Đăng nhập</button>
          <button className="btn-primary">Đăng ký</button>
        </div>
      </div>

      {!hasMessages ? (
        /* Landing */
        <div className="landing">
          <div className="landing-logo">
            <svg width="64" height="46" viewBox="0 0 212.121 151.515" style={{ shapeRendering: "crispEdges" }}>
              <rect x="30" y="0" width="30" height="30" fill="#FFAF01" />
              <rect x="152" y="0" width="30" height="30" fill="#FFAF01" />
              <rect x="30" y="30" width="60" height="30" fill="#FF8204" />
              <rect x="121" y="30" width="60" height="30" fill="#FF8204" />
              <rect x="30" y="61" width="152" height="30" fill="#FA500F" />
              <rect x="30" y="91" width="30" height="30" fill="#E51300" />
              <rect x="91" y="91" width="30" height="30" fill="#E51300" />
              <rect x="152" y="91" width="30" height="30" fill="#E51300" />
              <rect x="0" y="121" width="91" height="30" fill="#C4001D" />
              <rect x="121" y="121" width="91" height="30" fill="#C4001D" />
            </svg>
          </div>

          <div className="input-bar">
            <button className="input-add" aria-label="Thêm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square">
                <path d="M3 12H21" /><path d="M12 3V21" />
              </svg>
            </button>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Hỏi về di sản Đà Nẵng – Huế…"
              rows={1}
              className="input-textarea"
            />
            <div className="input-actions">
              <button className="input-fast" aria-label="Nhanh">⚡</button>
              <button
                className={`input-send ${input.trim() ? "active" : ""}`}
                aria-label="Gửi"
                onClick={() => input.trim() && send()}
              >
                {input.trim() ? (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12H19" /><path d="M12 5L19 12L12 19" />
                  </svg>
                ) : (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 22V19" /><path d="M8 6C8 3.79 9.79 2 12 2C14.21 2 16 3.79 16 6V11C16 13.21 14.21 15 12 15C9.79 15 8 13.21 8 11V6Z" /><path d="M4 10V11C4 15.42 7.58 19 12 19C16.42 19 20 15.42 20 11V10" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          <div className="suggestions">
            <p className="suggestions-title">Câu hỏi gợi ý</p>
            <div className="suggestion-list">
              {SUGGESTIONS.map((p) => (
                <button key={p} className="suggestion-chip" onClick={() => send(p)}>
                  {p}
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* Chat */
        <>
          <div className="chat-messages">
            {messages.map((msg) => (
              <div key={msg.id} className="msg">
                <div className="msg-label">{msg.role === "user" ? "Bạn" : "HeritageGraph"}</div>
                {msg.role === "user" ? (
                  <div className="msg-user">{msg.content}</div>
                ) : (
                  <div>
                    <div className="msg-assistant">{msg.content}</div>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="msg-sources">
                        {msg.sources.map((s, i) => (
                          <a key={i} href={s.url || "#"} target="_blank" rel="noreferrer" className="source-chip">
                            {s.doc || "Nguồn"}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="msg">
                <div className="msg-label">HeritageGraph</div>
                <div className="msg-assistant">Đang suy nghĩ…</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <div className="input-bar">
              <button className="input-add" aria-label="Thêm">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square">
                  <path d="M3 12H21" /><path d="M12 3V21" />
                </svg>
              </button>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Hỏi thêm…"
                rows={1}
                className="input-textarea"
              />
              <div className="input-actions">
                <button className="input-fast" aria-label="Nhanh">⚡</button>
                <button
                  className={`input-send ${input.trim() ? "active" : ""}`}
                  aria-label="Gửi"
                  onClick={() => input.trim() && send()}
                >
                  {input.trim() ? (
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M5 12H19" /><path d="M12 5L19 12L12 19" />
                    </svg>
                  ) : (
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 22V19" /><path d="M8 6C8 3.79 9.79 2 12 2C14.21 2 16 3.79 16 6V11C16 13.21 14.21 15 12 15C9.79 15 8 13.21 8 11V6Z" /><path d="M4 10V11C4 15.42 7.58 19 12 19C16.42 19 20 15.42 20 11V10" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
            <div className="input-disclaimer">
              HeritageGraph có thể mắc lỗi. Kiểm tra thông tin. · 100% local
            </div>
          </div>
        </>
      )}

      <button className="help-btn" aria-label="Trợ giúp">
        <QuestionCircleOutlined />
      </button>
    </div>
  );
}
