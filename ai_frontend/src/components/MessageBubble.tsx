import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Message } from "../types";
import { assistantMarkdownComponents } from "./markdownComponents";
import SourcesPanel from "./SourcesPanel";

export default function MessageBubble({ msg }: { msg: Message }) {
  return (
    <div
      className={[
        "max-w-3xl w-full",
        msg.role === "user" ? "ml-auto" : "mr-auto",
      ].join(" ")}
    >
      <div
        className={[
          "rounded-2xl px-4 py-3 text-sm leading-relaxed",
          msg.role === "user"
            ? "bg-blue-600 text-white"
            : "border border-white/10 bg-white/5 text-zinc-100",
        ].join(" ")}
      >
        {msg.role === "assistant" ? (
          <div className="min-w-0 text-left">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={assistantMarkdownComponents}
            >
              {msg.content.trim() === "" ? "\u00a0" : msg.content}
            </ReactMarkdown>
          </div>
        ) : (
          <div className="whitespace-pre-wrap text-left">{msg.content}</div>
        )}
      </div>

      {msg.role === "assistant" && msg.sources && msg.sources.length > 0 ? (
        <SourcesPanel sources={msg.sources} />
      ) : null}
    </div>
  );
}
