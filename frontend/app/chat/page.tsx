"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Message } from "@/types/chat";
import { TopBar, HelpButton } from "@/components/TopBar";
import { ChatInput } from "@/components/ChatInput";
import { SuggestionList } from "@/components/Suggestion";
import { ChatView } from "@/components/ChatView";

const SUGGESTIONS = [
  "Lăng Tự Đức được xây dựng năm nào?",
  "Cao lầu là món gì?",
  "Festival Huế tổ chức mấy năm một lần?",
  "Làng Non Nước nổi tiếng về gì?",
  "Nhã nhạc cung đình Huế có gì đặc biệt?",
];

export default function Home() {
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

  return (
    <div className="app-shell">
      <TopBar />

      {!hasMessages ? (
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

          <div className="landing-input">
            <ChatInput
              value={input}
              onChange={setInput}
              onSubmit={() => send()}
              placeholder="Hỏi về di sản Đà Nẵng – Huế…"
            />
          </div>

          <div className="landing-suggestions">
            <p className="landing-suggestions-title">Câu hỏi gợi ý</p>
            <SuggestionList suggestions={SUGGESTIONS} onSelect={send} />
          </div>
        </div>
      ) : (
        <ChatView
          messages={messages}
          input={input}
          loading={loading}
          onInputChange={setInput}
          onSend={() => send()}
          messagesEndRef={messagesEndRef}
        />
      )}

      <HelpButton />
    </div>
  );
}
