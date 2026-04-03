import { useEffect, useRef, useState } from "react";
import type { Message } from "../types";
import MessageBubble from "./MessageBubble";
import { streamQuery } from "../services/api";

export default function ChatWindow({ isReady }: { isReady: boolean }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, isStreaming]);

  const handleQuery = async () => {
    if (!query.trim() || !isReady || isStreaming) return;
    const userText = query.trim();
    setError(null);
    setQuery("");

    let assistantContent = "";

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userText },
      { role: "assistant", content: "" },
    ]);

    setIsStreaming(true);
    try {
      await streamQuery(userText, (chunk) => {
        // 🔥 Detect sources payload
        if (chunk.includes("[SOURCES]")) {
          const jsonPart = chunk.split("[SOURCES]")[1];

          try {
            const sources = JSON.parse(jsonPart);

            setMessages((prev) => {
              const updated = [...prev];
              const lastMsg = updated[updated.length - 1];

              if (lastMsg.role === "assistant") {
                lastMsg.sources = sources;
              }

              return updated;
            });
          } catch (e) {
            console.error("Failed to parse sources", e);
          }

          return; // stop processing this chunk as text
        }

        // ✅ Normal streaming
        assistantContent += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1].content = assistantContent;
          return updated;
        });
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <>
      {/* Chat */}
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-4xl px-4 py-6 space-y-4">
          {messages.length === 0 ? (
            <div className="pt-10 text-center">
              <div className="text-xl font-semibold">Ask about your repo</div>
              <div className="mt-2 text-sm text-zinc-400">
                Click <span className="text-zinc-200">Repo</span> to ingest,
                then ask questions here.
              </div>
            </div>
          ) : null}

          {messages.map((msg, i) => (
            <MessageBubble key={i} msg={msg} />
          ))}

          {error ? (
            <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">
              {error}
            </div>
          ) : null}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-white/10 bg-zinc-950">
        <div className="mx-auto max-w-4xl px-4 py-4">
          <div className="flex items-center gap-2">
            <div className="flex-1">
              <textarea
                className="w-full resize-none rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm outline-none placeholder:text-zinc-500 focus:border-white/20 h-[42px]"
                placeholder={isReady ? "Message…" : "Ingest a repo to start…"}
                value={query}
                rows={2}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    void handleQuery();
                  }
                }}
                disabled={!isReady || isStreaming}
              />
            </div>
            <button
              onClick={() => void handleQuery()}
              className="h-[40px] inline-flex items-center justify-center rounded-lg bg-emerald-600 px-4 text-sm font-medium hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={!isReady || isStreaming || !query.trim()}
            >
              {isStreaming ? "Sending…" : "Send"}
            </button>
          </div>
          <div className="mt-2 text-xs text-zinc-500">
            Enter to send, Shift+Enter for newline
          </div>
        </div>
      </div>
    </>
  );
}
