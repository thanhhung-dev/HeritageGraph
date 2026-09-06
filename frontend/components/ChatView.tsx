"use client";

import { Message } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { ChatInput } from "./ChatInput";

interface ChatViewProps {
  messages: Message[];
  input: string;
  loading: boolean;
  onInputChange: (value: string) => void;
  onSend: () => void;
  messagesEndRef: React.Ref<HTMLDivElement>;
}

export function ChatView({
  messages,
  input,
  loading,
  onInputChange,
  onSend,
  messagesEndRef,
}: ChatViewProps) {
  return (
    <>
      <div className="chat-messages">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            sources={msg.sources}
          />
        ))}
        {loading && (
          <MessageBubble role="assistant" content="Đang suy nghĩ…" />
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <div className="input-area-inner">
          <ChatInput
            value={input}
            onChange={onInputChange}
            onSubmit={onSend}
            placeholder="Hỏi thêm…"
          />
          <div className="input-area-disclaimer">
            HeritageGraph có thể mắc lỗi. Kiểm tra thông tin. · 100% local
          </div>
        </div>
      </div>
    </>
  );
}
