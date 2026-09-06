"use client";

import { useState } from "react";
import { MistralLogo } from "./MistralLogo";
import { ChatInput } from "./ChatInput";
import { SuggestionList } from "./Suggestion";
import { MessageBubble } from "./MessageBubble";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Array<{ doc?: string; url?: string; heading?: string }>;
}

interface ChatProps {
  messages: Message[];
  onSend: (text: string) => void;
  loading?: boolean;
}

export function Chat({ messages, onSend, loading }: ChatProps) {
  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-welcome">
            <div className="chat-welcome-logo">
              <MistralLogo size={48} />
            </div>
            <h1 className="chat-welcome-title">Xin chào!</h1>
            <p className="chat-welcome-desc">
              Hỏi tôi về di sản, ẩm thực, lễ hội, làng nghề Đà Nẵng – Huế
            </p>
          </div>
        ) : (
          messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              role={msg.role}
              content={msg.content}
              sources={msg.sources}
            />
          ))
        )}
        {loading && (
          <MessageBubble role="assistant" content="Đang suy nghĩ…" />
        )}
      </div>
    </div>
  );
}

interface LandingProps {
  onSend: (text: string) => void;
  suggestions: string[];
}

export function Landing({ onSend, suggestions }: LandingProps) {
  const [input, setInput] = useState("");

  return (
    <div className="landing">
      <div className="landing-logo">
        <MistralLogo size={64} />
      </div>

      <div className="landing-input">
        <ChatInput
          value={input}
          onChange={setInput}
          onSubmit={() => {
            if (input.trim()) {
              onSend(input);
              setInput("");
            }
          }}
          placeholder="Hỏi về di sản Đà Nẵng – Huế…"
        />
      </div>

      <div className="landing-suggestions">
        <p className="landing-suggestions-title">Câu hỏi gợi ý</p>
        <SuggestionList suggestions={suggestions} onSelect={onSend} />
      </div>
    </div>
  );
}
