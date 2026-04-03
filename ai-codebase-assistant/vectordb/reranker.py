def simple_rerank(query: str, chunks):
    query_terms = set(query.lower().split())

    def score(chunk):
        content_terms = set(chunk["content"].lower().split())
        return len(query_terms & content_terms)

    reranked = sorted(chunks, key=score, reverse=True)

    return reranked