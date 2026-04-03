export type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export type Source = {
  file: string;
  snippet: string;
};


export type Status = "idle" | "processing" | "ready";