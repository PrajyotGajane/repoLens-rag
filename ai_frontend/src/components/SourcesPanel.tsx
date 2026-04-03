import { useState } from "react";
import type { Source } from "../types";

export default function SourcesPanel({ sources }: { sources: Source[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 border border-white/10 rounded-lg p-2 bg-black/30">
      <div className="text-xs text-zinc-400 mb-2">Sources</div>

      {sources.map((src, i) => (
        <div key={i} className="mb-2">
          <div
            className="cursor-pointer text-sm text-emerald-400 hover:underline"
            onClick={() => setOpenIndex(openIndex === i ? null : i)}
          >
            📄 {src.file}
          </div>

          {openIndex === i && (
            <pre className="mt-1 p-2 text-xs bg-black/50 rounded overflow-x-auto">
              <code>{src.snippet}</code>
            </pre>
          )}
        </div>
      ))}
    </div>
  );
}