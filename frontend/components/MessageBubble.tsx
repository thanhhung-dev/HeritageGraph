import { Source } from "@/types/chat";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

export function MessageBubble({ role, content, sources }: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div className="message-bubble">
      <div className="message-bubble-label">
        {isUser ? "Bạn" : "HeritageGraph"}
      </div>
      {isUser ? (
        <div className="message-bubble-user">{content}</div>
      ) : (
        <div>
          <div className="message-bubble-assistant">{content}</div>
          {sources && sources.length > 0 && (
            <div className="message-bubble-sources">
              {sources.map((s, i) => (
                <SourceChip key={i} source={s} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SourceChip({ source }: { source: Source }) {
  return (
    <a
      href={source.url || "#"}
      target="_blank"
      rel="noreferrer"
      className="source-chip"
    >
      {source.doc || "Nguồn"}
    </a>
  );
}
