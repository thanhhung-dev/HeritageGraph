"use client";

import { useRef, KeyboardEvent } from "react";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading?: boolean;
  placeholder?: string;
}

export function ChatInput({
  value,
  onChange,
  onSubmit,
  placeholder = "Nhập câu hỏi…",
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="chat-input">
      <button className="chat-input-add" aria-label="Thêm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square">
          <path d="M3 12H21" /><path d="M12 3V21" />
        </svg>
      </button>
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        rows={1}
        className="chat-input-textarea"
      />
      <div className="chat-input-actions">
        <button className="chat-input-fast" aria-label="Nhanh">
          ⚡
        </button>
        <button
          className={`chat-input-send ${value.trim() ? "active" : ""}`}
          aria-label="Gửi"
          onClick={() => value.trim() && onSubmit()}
        >
          {value.trim() ? (
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
  );
}
