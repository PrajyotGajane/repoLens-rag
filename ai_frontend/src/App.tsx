import { useEffect, useState } from "react";
import RepoInput from "./components/RepoInput";
import ChatWindow from "./components/ChatWindow";
import { getStatus } from "./services/api";
import type { Status } from "./types"

export default function App() {
  const [status, setStatus] = useState<Status>("idle");
  const [isRepoOpen, setIsRepoOpen] = useState(false);

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await getStatus();

      if (data.is_processing) setStatus("processing");
      else if (data.is_ready) setStatus("ready");
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-dvh bg-zinc-950 text-zinc-100 flex flex-col">
      <header className="sticky top-0 z-10 border-b border-white/10 bg-zinc-950/80 backdrop-blur">
        <div className="mx-auto max-w-4xl px-4 py-3 flex items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="text-sm font-medium leading-tight truncate">AI Chat</div>
            <div className="text-xs text-zinc-400">
              Status:{" "}
              <span
                className={
                  status === "ready"
                    ? "text-emerald-400"
                    : status === "processing"
                      ? "text-amber-400"
                      : "text-zinc-400"
                }
              >
                {status}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setIsRepoOpen(true)}
              className="inline-flex items-center justify-center rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm hover:bg-white/10"
            >
              Repo
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 flex flex-col">
        <ChatWindow isReady={status === "ready"} />
      </main>

      {isRepoOpen ? (
        <div className="fixed inset-0 z-50">
          <div
            className="absolute inset-0 bg-black/60"
            onClick={() => setIsRepoOpen(false)}
          />
          <div className="absolute inset-x-0 top-14 mx-auto max-w-xl px-4">
            <div className="rounded-xl border border-white/10 bg-zinc-950 shadow-2xl">
              <div className="px-4 py-3 border-b border-white/10 flex items-center justify-between gap-3">
                <div className="text-sm font-medium">Repository ingestion</div>
                <button
                  type="button"
                  onClick={() => setIsRepoOpen(false)}
                  className="rounded-md px-2 py-1 text-sm text-zinc-300 hover:bg-white/10"
                >
                  Close
                </button>
              </div>
              <div className="p-4">
                <RepoInput setStatus={setStatus} />
                <div className="mt-2 text-xs text-zinc-400">
                  Paste a GitHub URL and ingest before asking questions.
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}