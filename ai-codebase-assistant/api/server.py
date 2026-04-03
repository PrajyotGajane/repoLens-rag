from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import threading

from ingest.ingest_service import ingest_repository
from embeddings.pipeline import process_documents
from vectordb.chroma_store import store_embeddings
from graph.workflow import create_workflow

from vectordb.retriever import retrieve_chunks 
from vectordb.reranker import simple_rerank
from vectordb.context_builder import build_context
from rag.generator import generate_answer_stream
from fastapi.responses import StreamingResponse  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development (we'll tighten later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Global State ----
app_state: Dict = {
    "is_processing": False,
    "is_ready": False,
    "current_repo": None,
    "workflow": None
}


# ---- Request Models ----
class IngestRequest(BaseModel):
    repo_url: str


class QueryRequest(BaseModel):
    query: str


# ---- Routes ----

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest_repo(req: IngestRequest):
    if app_state["is_processing"]:
        raise HTTPException(status_code=400, detail="Already processing a repo")

    def background_ingest():
        try:
            app_state["is_processing"] = True
            app_state["is_ready"] = False

            # Step 1: Ingest
            docs = ingest_repository(req.repo_url)

            # Step 2: Chunk + Embed
            embedded_docs = process_documents(docs)

            # Step 3: Store
            store_embeddings(embedded_docs)

            # Step 4: Prepare workflow
            app_state["workflow"] = create_workflow()

            app_state["is_ready"] = True
        except Exception as e:
            print(f"[ERROR] Ingestion failed: {e}")
        finally:
            app_state["is_processing"] = False

    threading.Thread(target=background_ingest).start()

    return {"status": "processing"}


@app.post("/query")
def query_repo(req: QueryRequest):
    if not app_state["is_ready"]:
        raise HTTPException(status_code=400, detail="Repo not ready yet")

    def stream():
        try:
            chunks = retrieve_chunks(req.query, top_k=10)
            reranked = simple_rerank(req.query, chunks)
            context = build_context(reranked)

            # prepare sources
            sources = [
                {
                    "file": c["metadata"]["file"],
                    "snippet": c["content"][:300]
                }
                for c in reranked[:3]
            ]

            # stream answer
            for token in generate_answer_stream(req.query, context):
                yield token

            # send sources as JSON marker
            import json
            yield f"\n[SOURCES]{json.dumps(sources)}"

        except Exception as e:
            yield f"\n[ERROR]: {str(e)}"

    return StreamingResponse(stream(), media_type="text/plain")

@app.get("/status")
def status():
    return {
        "is_processing": app_state["is_processing"],
        "is_ready": app_state["is_ready"]
    }

