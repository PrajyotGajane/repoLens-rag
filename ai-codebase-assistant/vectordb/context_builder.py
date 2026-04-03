def build_context(chunks, max_chars=4000):
    context = ""
    seen_files = set()

    for chunk in chunks:
        file = chunk["metadata"]["file"]

        if file not in seen_files:
            context += f"\n\n### FILE: {file}\n"
            seen_files.add(file)

        snippet = chunk["content"]

        if len(context) + len(snippet) > max_chars:
            break

        context += snippet + "\n"

    return context