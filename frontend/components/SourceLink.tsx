"use client";

import { useState } from "react";

interface SourceLinkProps {
  source: {
    doc?: string;
    url?: string;
    heading?: string;
  };
}

export function SourceLink({ source }: SourceLinkProps) {
  const [hovered, setHovered] = useState(false);
  return (
    <a
      href={source.url || "#"}
      target="_blank"
      rel="noreferrer"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="source-link"
      style={{ background: hovered ? "var(--bg-muted)" : "var(--bg-input)" }}
    >
      <span className="source-link-icon">📄</span>
      <span className="source-link-text">{source.doc || "Nguồn"}</span>
      {source.heading && <span className="source-link-heading">— {source.heading}</span>}
    </a>
  );
}

interface SourceListProps {
  sources: Array<{
    doc?: string;
    url?: string;
    heading?: string;
  }>;
}

export function SourceList({ sources }: SourceListProps) {
  if (!sources || sources.length === 0) return null;
  return (
    <div className="source-list">
      {sources.map((s, i) => (
        <SourceLink key={i} source={s} />
      ))}
    </div>
  );
}
