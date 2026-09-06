"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import {
  Bubble,
  Sender,
  Welcome,
  Prompts,
} from "@ant-design/x";
import {
  PlusOutlined,
  DeleteOutlined,
  SearchOutlined,
  StarOutlined,
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

type Conversation = {
  id: string;
  title: string;
  messages: Message[];
};


const PROMPT_ITEMS = [
  { key: "1", label: "Di tích", description: "Lăng Tự Đức được xây dựng năm nào?" },
  { key: "2", label: "Ẩm thực", description: "Cao lầu là món gì?" },
  { key: "3", label: "Lễ hội", description: "Festival Huế tổ chức mấy năm một lần?" },
  { key: "4", label: "Làng nghề", description: "Làng Non Nước nổi tiếng về gì?" },
  { key: "5", label: "Nghệ thuật", description: "Nhã nhạc cung đình Huế có gì đặc biệt?" },
];

export default function ChatBot() {
  const [conversations, setConversations] = useState<Conversation[]>([
    { id: "1", title: "Cuộc trò chuyện mới", messages: [] },
  ]);
  const [activeId, setActiveId] = useState("1");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activeConv = conversations.find((c) => c.id === activeId) ?? conversations[0];
  const messages = activeConv?.messages ?? [];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = useCallback(
    async (text?: string) => {
      const userMsg = text || input;
      if (!userMsg.trim() || loading) return;

      const userMessage: Message = { role: "user", content: userMsg };
      setConversations((prev) =>
        prev.map((c) =>
          c.id === activeId
            ? { ...c, messages: [...c.messages, userMessage], title: c.messages.length === 0 ? userMsg : c.title }
            : c
        )
      );
      setInput("");
      setLoading(true);

      try {
        const res = await fetch("http://localhost:8000/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userMsg, use_rag: true }),
        });
        const data = await res.json();
        const botMessage: Message = {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        };
        setConversations((prev) =>
          prev.map((c) =>
            c.id === activeId
              ? { ...c, messages: [...c.messages, botMessage] }
              : c
          )
        );
      } catch {
        const errMsg: Message = {
          role: "assistant",
          content: "Đã xảy ra lỗi khi kết nối tới máy chủ.",
        };
        setConversations((prev) =>
          prev.map((c) =>
            c.id === activeId
              ? { ...c, messages: [...c.messages, errMsg] }
              : c
          )
        );
      } finally {
        setLoading(false);
      }
    },
    [input, loading, activeId]
  );

  const newConversation = () => {
    const id = Date.now().toString();
    setConversations((prev) => [
      ...prev,
      { id, title: "Cuộc trò chuyện mới", messages: [] },
    ]);
    setActiveId(id);
  };

  const deleteConversation = (id: string) => {
    setConversations((prev) => {
      const next = prev.filter((c) => c.id !== id);
      if (next.length === 0) {
        next.push({ id: Date.now().toString(), title: "Cuộc trò chuyện mới", messages: [] });
        setActiveId(next[0].id);
      } else if (id === activeId) {
        setActiveId(next[0].id);
      }
      return next;
    });
  };

  const renderBubble = (msg: Message, index: number) => {
    const isUser = msg.role === "user";
    return (
      <Bubble
        key={index}
        placement={isUser ? "end" : "start"}
        avatar={isUser ? undefined : <span style={{ fontSize: 20, lineHeight: 1 }}>🏛️</span>}
        style={{ marginBottom: 4 }}
        content={
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {isUser ? (
              <div className="bubble-user" style={{ whiteSpace: "pre-wrap", lineHeight: "22px" }}>
                {msg.content}
              </div>
            ) : (
              <div style={{ whiteSpace: "pre-wrap", lineHeight: "22px" }}>
                {msg.content}
              </div>
            )}
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources-box">
                <div className="sources-box-title">
                  📚 Nguồn tham khảo ({msg.sources.length})
                </div>
                {msg.sources.map((s, j) => (
                  <div key={j} className="sources-box-item">
                    • {s.doc || "Không rõ nguồn"}
                    {s.heading && <span style={{ color: "#888" }}> — {s.heading}</span>}
                    {s.url && (
                      <a
                        href={s.url}
                        target="_blank"
                        rel="noreferrer"
                        className="sources-box-link"
                      >
                        [xem nguồn]
                      </a>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        }
      />
    );
  };

  const filteredConversations = searchQuery
    ? conversations.filter((c) =>
        c.title.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : conversations;

  return (
    <div className="chat-shell">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">HeritageGraph</div>
          <button className="btn-new" onClick={newConversation} aria-label="Cuộc trò chuyện mới">
            <PlusOutlined style={{ fontSize: 12 }} />
            Mới
          </button>
        </div>

        <div className="sidebar-search">
          <div className="sidebar-search-inner">
            <SearchOutlined style={{ color: "var(--text-subtle)", fontSize: 13 }} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Tìm kiếm cuộc trò chuyện..."
            />
          </div>
        </div>


        <div className="sidebar-conversations">
          <div className="sidebar-section-title">Gần đây</div>
          {filteredConversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setActiveId(conv.id)}
              className={`sidebar-conversation ${conv.id === activeId ? "active" : ""}`}
            >
              <span className="sidebar-conversation-title">{conv.title}</span>
              <button
                className="sidebar-conversation-delete"
                onClick={(e) => { e.stopPropagation(); deleteConversation(conv.id); }}
                aria-label={`Xóa ${conv.title}`}
              >
                <DeleteOutlined />
              </button>
            </div>
          ))}
        </div>

        <div className="sidebar-footer">
          100% local · RAG + LoRA · Qwen2.5-3B
        </div>
      </aside>

      {/* Main */}
      <main className="chat-main">
        <div className="chat-topbar">
          <div className="chat-topbar-title">{activeConv?.title || "Cuộc trò chuyện mới"}</div>
          <div className="chat-topbar-actions">
            <button className="btn-icon" aria-label="Yêu thích">
              <StarOutlined />
            </button>
            <button
              className="btn-ghost"
              onClick={() => {
                setConversations((prev) =>
                  prev.map((c) => (c.id === activeId ? { ...c, messages: [] } : c))
                );
              }}
              aria-label="Xóa tin nhắn"
            >
              Xóa
            </button>
          </div>
        </div>

        <div className="chat-messages" aria-live="polite" aria-label="Lịch sử trò chuyện">
          {messages.length === 0 && (
            <div className="chat-welcome">
              <Welcome
                icon={<span style={{ fontSize: 40, lineHeight: 1 }}>🏛️</span>}
                title={<span style={{ color: "var(--text-default)", fontSize: 18, fontWeight: 600 }}>Xin chào!</span>}
                description={
                  <span style={{ color: "var(--text-subtle)", fontSize: 14, textAlign: "center" }}>
                    Hỏi tôi về di sản, ẩm thực, lễ hội, làng nghề Đà Nẵng – Huế
                  </span>
                }
              />
              <Prompts
                title={<span style={{ color: "var(--text-subtle)", fontSize: 12, textTransform: "uppercase", letterSpacing: "0.05em" }}>Câu hỏi gợi ý</span>}
                items={PROMPT_ITEMS}
                vertical
                onItemClick={(info) => send(info.data.description as string)}
              />
            </div>
          )}
          {messages.map((m, i) => renderBubble(m, i))}
          {loading && (
            <Bubble
              placement="start"
              avatar={<span style={{ fontSize: 20, lineHeight: 1 }}>🏛️</span>}
              content={<span style={{ color: "var(--text-subtle)" }}>Đang suy nghĩ…</span>}
              typing
            />
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <Sender
            value={input}
            onChange={setInput}
            onSubmit={() => send()}
            placeholder="Nhập câu hỏi về di sản Đà Nẵng – Huế…"
            loading={loading}
          />
         
        </div>
      </main>
    </div>
  );
}
