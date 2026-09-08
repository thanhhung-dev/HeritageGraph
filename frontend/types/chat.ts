export interface Source {
  text?: string;
  doc?: string;
  url?: string;
  heading?: string;
  chunk_id?: string;
}

export interface Suggestion {
  original: string;
  suggested: string;
  score: number;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  correctedFrom?: string;
  correctedTo?: string;
  needsUserChoice?: boolean;
  suggestions?: Suggestion[];
}
