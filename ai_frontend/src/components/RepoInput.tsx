import { useState } from "react";
import { ingestRepo } from "../services/api";

type Props = {
  setStatus: (s: "idle" | "processing" | "ready") => void;
};

export default function RepoInput({ setStatus }: Props) {
  const [repoUrl, setRepoUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleIngest = async () => {
    setStatus("processing");
    setIsSubmitting(true);
    try {
      await ingestRepo(repoUrl);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <input
        className="w-full rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm outline-none placeholder:text-zinc-500 focus:border-white/20"
        placeholder="Enter GitHub repo URL..."
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
      />
      <button
        onClick={handleIngest}
        className="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={!repoUrl.trim() || isSubmitting}
      >
        {isSubmitting ? "Ingesting…" : "Ingest"}
      </button>
    </div>
  );
}