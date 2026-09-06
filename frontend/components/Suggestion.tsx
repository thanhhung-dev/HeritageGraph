"use client";

interface SuggestionProps {
  text: string;
  onClick: () => void;
}

export function Suggestion({ text, onClick }: SuggestionProps) {
  return (
    <button className="suggestion-chip" onClick={onClick}>
      {text}
    </button>
  );
}

interface SuggestionListProps {
  suggestions: string[];
  onSelect: (text: string) => void;
}

export function SuggestionList({ suggestions, onSelect }: SuggestionListProps) {
  return (
    <div className="suggestion-list">
      {suggestions.map((text) => (
        <Suggestion key={text} text={text} onClick={() => onSelect(text)} />
      ))}
    </div>
  );
}
