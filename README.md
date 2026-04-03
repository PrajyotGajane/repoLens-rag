## Implemented (Core Features)
- Clone and ingest GitHub repositories with file filtering and size constraints
- Parse code into structured documents (file, content, language)
- Chunk code using sliding window with overlap and metadata tracking
- Generate embeddings using OpenAI (text-embedding-3-small)
- Store and query vectors efficiently using ChromaDB (persistent)
- Perform semantic retrieval + lexical reranking (hybrid search)
- Build structured, file-aware context with size constraints
- Generate context-grounded answers using LLM (gpt-4.1-mini)
- Stream responses token-by-token via FastAPI (StreamingResponse)
- React + TypeScript UI with chat interface, live streaming, repo ingestion flow, and source attribution panel

## Next (High-Impact Improvements)
- Replace [SOURCES] parsing with proper SSE-based structured streaming
- Integrate LangGraph with streaming for multi-step reasoning
- Improve retrieval using hybrid search (BM25 + vector) or ML reranker
- Add code intelligence (AST parsing, symbol-level retrieval)
- Build file explorer + syntax-highlighted code viewer