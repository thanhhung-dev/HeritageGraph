"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import {
  SendOutlined,
  PlusOutlined,
  SettingOutlined,
  QuestionCircleOutlined,
} from "@ant-design/icons";

type Source = {
  text: string;
  doc?: string;
  url?: string;
  heading?: string;
  chunk_id?: string;
};

type Message = {
  content: string;
  sources?: Source[];
  role: "user" | "assistant";
};

const PROMPTS = [
  "Lăng Tự Đức được xây dựng năm nào?",
  "Cao lầu là món gì?",
  "Festival Huế tổ chức mấy năm một lần?",
  "Làng Non Nước nổi tiếng về gì?",
];

const SourceLink = ({ source }: { source: Source }) => (
  <a
    href={source.url || "#"}
    target="_blank"
    rel="noreferrer"
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      padding: "4px 10px",
      background: "var(--bg-input)",
      borderRadius: 16,
      fontSize: 13,
      color: "var(--text-default)",
      textDecoration: "none",
      border: "1px solid var(--border-default)",
      transition: "background 0.15s",
    }}
    onMouseEnter={(e) => { e.currentTarget.style.background = "var(--bg-muted)"; }}
    onMouseLeave={(e) => { e.currentTarget.style.background = "var(--bg-input)"; }}
  >
    📄 {source.doc || "Nguồn"}
  </a>
);

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const hasMessages = messages.length > 0;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = useCallback(
    async (text?: string) => {
      const userMsg = text || input;
      if (!userMsg.trim() || loading) return;

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
      } catch {
        setMessages((m) => [
          ...m,
          { role: "assistant", content: "Đã xảy ra lỗi khi kết nối tới máy chủ." },
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

  const MistralLogo = () => (
    <svg
      width="48"
      height="34"
      viewBox="0 0 212.121 151.515"
      style={{ shapeRendering: "crispEdges" }}
    >
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
  );

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        background: "var(--bg-default)",
        fontFamily: "var(--font-sans)",
        position: "relative",
      }}
    >
      {/* Top bar */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "12px 24px",
          zIndex: 10,
        }}
      >
        <div style={{ display: "flex", gap: 4 }}>
          <button className="btn-icon" aria-label="Cài đặt" style={{ width: 36, height: 36 }}>
            <SettingOutlined style={{ fontSize: 18 }} />
          </button>
          <button className="btn-icon" aria-label="Quyền riêng tư" style={{ width: 36, height: 36 }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M22 13.5V10.5L18.6914 8.13674L18.2991 4.08973L15.701 2.58973L12 4.27343L8.29904 2.58975L5.70096 4.08975L5.3086 8.13672L2 10.5V12V13.5L5.30858 15.8633L5.70095 19.9103L8.29903 21.4103L12 19.7266L15.701 21.4103L18.299 19.9103L18.6914 15.8633L22 13.5Z" strokeLinecap="square" />
              <path d="M15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12Z" />
            </svg>
          </button>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn-ghost" style={{ height: 32, padding: "0 12px", fontSize: 14, borderRadius: 8 }}>
            Đăng nhập
          </button>
          <button className="btn-dark" style={{ height: 32, padding: "0 16px", fontSize: 14, borderRadius: 8 }}>
            Đăng ký
          </button>
        </div>
      </div>

      {/* Main content */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          maxWidth: 720,
          width: "100%",
          margin: "0 auto",
          padding: "0 24px",
        }}
      >
        {!hasMessages ? (
          /* Landing state: logo + input centered */
          <>
            <div style={{ flex: 1 }} />
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 32 }}>
              <MistralLogo />
            </div>

            {/* Input bar */}
            <div
              style={{
                background: "var(--bg-card)",
                border: "1px solid var(--border-default)",
                borderRadius: 14,
                padding: "12px 16px",
                boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
                transition: "box-shadow 0.15s",
              }}
            >
              <div style={{ display: "flex", alignItems: "flex-start", gap: 8 }}>
                <button className="btn-icon" aria-label="Thêm" style={{ marginTop: 2, width: 32, height: 32, flexShrink: 0 }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square">
                    <path d="M3 12H21" /><path d="M12 3V21" />
                  </svg>
                </button>
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Hỏi về di sản Đà Nẵng – Huế…"
                  rows={1}
                  style={{
                    flex: 1,
                    border: "none",
                    outline: "none",
                    resize: "none",
                    fontSize: 16,
                    fontFamily: "var(--font-sans)",
                    fontWeight: 400,
                    lineHeight: 1.5,
                    color: "var(--text-default)",
                    background: "transparent",
                    minHeight: 24,
                    maxHeight: 120,
                  }}
                />
                <div style={{ display: "flex", alignItems: "center", gap: 4, flexShrink: 0, marginTop: 2 }}>
                  <button
                    className="btn-icon"
                    aria-label="Nhanh"
                    style={{
                      background: "var(--bg-input)",
                      borderRadius: 8,
                      height: 32,
                      padding: "0 10px",
                      display: "flex",
                      alignItems: "center",
                      gap: 4,
                      fontSize: 13,
                      fontWeight: 400,
                      color: "var(--text-default)",
                    }}
                  >
                    ⚡ <span style={{ display: "none" }}>Nhanh</span>
                  </button>
                  <button
                    className="btn-icon"
                    aria-label="Giọng nói"
                    style={{
                      background: "var(--orange-500)",
                      color: "var(--zinc-00)",
                      borderRadius: 8,
                      width: 32,
                      height: 32,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 22V19" /><path d="M8 6C8 3.79 9.79 2 12 2C14.21 2 16 3.79 16 6V11C16 13.21 14.21 15 12 15C9.79 15 8 13.21 8 11V6Z" /><path d="M4 10V11C4 15.42 7.58 19 12 19C16.42 19 20 15.42 20 11V10" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Suggestions */}
            <div style={{ marginTop: 16, display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
              {PROMPTS.map((p) => (
                <button
                  key={p}
                  onClick={() => send(p)}
                  style={{
                    padding: "6px 14px",
                    background: "var(--bg-input)",
                    border: "1px solid var(--border-default)",
                    borderRadius: 16,
                    fontSize: 13,
                    color: "var(--text-default)",
                    cursor: "pointer",
                    fontFamily: "var(--font-sans)",
                    fontWeight: 400,
                    transition: "background 0.15s",
                  }}
                  onMouseEnter={(e) => { e.currentTarget.style.background = "var(--bg-muted)"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = "var(--bg-input)"; }}
                >
                  {p}
                </button>
              ))}
            </div>

            <div style={{ flex: 1 }} />
          </>
        ) : (
          /* Chat state: messages + input below */
          <>
            <div style={{ height: 64 }} />

            <div style={{ flex: 1, overflowY: "auto", paddingBottom: 24 }}>
              {messages.map((msg, i) => (
                <div key={i} style={{ marginBottom: 24 }}>
                  <div
                    style={{
                      fontWeight: 400,
                      fontSize: 13,
                      color: "var(--text-subtle)",
                      marginBottom: 8,
                      paddingLeft: msg.role === "user" ? "auto" : 0,
                      textAlign: msg.role === "user" ? "right" : "left",
                    }}
                  >
                    {msg.role === "user" ? "Bạn" : "HeritageGraph"}
                  </div>
                  {msg.role === "user" ? (
                    <div
                      style={{
                        background: "var(--bg-input)",
                        color: "var(--text-default)",
                        borderRadius: "16px 16px 4px 16px",
                        padding: "12px 16px",
                        fontSize: 16,
                        lineHeight: 1.5,
                        maxWidth: "80%",
                        marginLeft: "auto",
                      }}
                    >
                      {msg.content}
                    </div>
                  ) : (
                    <div>
                      <div style={{ fontSize: 16, lineHeight: 1.6, color: "var(--text-default)" }}>
                        {msg.content}
                      </div>
                      {msg.sources && msg.sources.length > 0 && (
                        <div style={{ marginTop: 12, display: "flex", flexWrap: "wrap", gap: 8 }}>
                          {msg.sources.map((s, j) => (
                            <SourceLink key={j} source={s} />
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div style={{ marginBottom: 24 }}>
                  <div style={{ fontSize: 13, color: "var(--text-subtle)", marginBottom: 8 }}>HeritageGraph</div>
                  <div style={{ fontSize: 16, color: "var(--text-subtle)" }}>Đang suy nghĩ…</div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input bar at bottom */}
            <div style={{ paddingBottom: 24, paddingTop: 12, position: "sticky", bottom: 0, background: "linear-gradient(to bottom, transparent, var(--bg-default) 20%)" }}>
              <div
                style={{
                  background: "var(--bg-card)",
                  border: "1px solid var(--border-default)",
                  borderRadius: 14,
                  padding: "12px 16px",
                  boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
                }}
              >
                <div style={{ display: "flex", alignItems: "flex-start", gap: 8 }}>
                  <button className="btn-icon" aria-label="Thêm" style={{ marginTop: 2, width: 32, height: 32, flexShrink: 0 }}>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square">
                      <path d="M3 12H21" /><path d="M12 3V21" />
                    </svg>
                  </button>
                  <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Hỏi thêm…"
                    rows={1}
                    style={{
                      flex: 1,
                      border: "none",
                      outline: "none",
                      resize: "none",
                      fontSize: 16,
                      fontFamily: "var(--font-sans)",
                      fontWeight: 400,
                      lineHeight: 1.5,
                      color: "var(--text-default)",
                      background: "transparent",
                      minHeight: 24,
                      maxHeight: 120,
                    }}
                  />
                  <div style={{ display: "flex", alignItems: "center", gap: 4, flexShrink: 0, marginTop: 2 }}>
                    <button
                      className="btn-icon"
                      aria-label="Nhanh"
                      style={{
                        background: "var(--bg-input)",
                        borderRadius: 8,
                        height: 32,
                        padding: "0 10px",
                        display: "flex",
                        alignItems: "center",
                        gap: 4,
                        fontSize: 13,
                        fontWeight: 400,
                        color: "var(--text-default)",
                      }}
                    >
                      ⚡
                    </button>
                    <button
                      className="btn-icon"
                      aria-label="Giọng nói"
                      style={{
                        background: input.trim() ? "var(--orange-500)" : "var(--bg-input)",
                        color: input.trim() ? "var(--zinc-00)" : "var(--text-default)",
                        borderRadius: 8,
                        width: 32,
                        height: 32,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        cursor: input.trim() ? "pointer" : "default",
                      }}
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
              </div>
              <div style={{ marginTop: 8, textAlign: "center", fontSize: 12, color: "var(--text-muted)" }}>
                HeritageGraph có thể mắc lỗi. Kiểm tra thông tin. · 100% local
              </div>
            </div>
          </>
        )}
      </div>

      {/* Help button */}
      <button
        className="btn-icon"
        aria-label="Trợ giúp"
        style={{
          position: "fixed",
          bottom: 16,
          right: 16,
          width: 40,
          height: 40,
          borderRadius: "50%",
          background: "var(--bg-card)",
          border: "1px solid var(--border-default)",
          boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 16,
          zIndex: 20,
        }}
      >
        <QuestionCircleOutlined />
      </button>
    </div>
  );
}
