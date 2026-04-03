const BASE_URL = "http://localhost:8000";

export async function ingestRepo(repoUrl: string) {
  await fetch(`${BASE_URL}/ingest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ repo_url: repoUrl }),
  });
}

export async function getStatus() {
  const res = await fetch(`${BASE_URL}/status`);
  return res.json();
}

export async function streamQuery(
  query: string,
  onChunk: (chunk: string) => void
) {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  const reader = res.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) return;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    onChunk(chunk);
  }
}