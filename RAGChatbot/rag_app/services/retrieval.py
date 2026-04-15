from typing import Callable, Iterable

from langchain.schema import Document
from langchain_community.vectorstores import FAISS


# Intent-based hard routing to specific vault sources.
PRIORITY_RULES = [
    {
        "keywords": ["project", "projects", "portfolio", "what have you made", "built"],
        "source": "Jia Hui's network/Perplexity/Master-Project-List.md",
    },
    {
        "keywords": ["who am i", "about me", "my profile", "my name", "tell me about"],
        "source": "Jia Hui's network/Claude/About J.md",
    },
]

# Semantic tag hints used for filtered retrieval.
TAG_KEYWORD_MAP = {
    "who am i": ["profile", "about", "personal", "identity"],
    "my name": ["profile", "about"],
    "my skills": ["skills", "expertise"],
    "my projects": ["projects", "portfolio"],
}

QUERY_REWRITE_RULES = {
    "who am i": ["about me", "my profile", "personal identity", "my name"],
    "my name": ["who am i", "about me", "profile"],
    "my skills": ["skills", "expertise", "tech stack", "what am i good at"],
    "my projects": ["projects", "portfolio", "things i built", "my work"],
}

NAME_REWRITE_RULES = {
    "jia hui": ["I am", "my name is", "about me", "profile"],
}

# Lowered threshold to allow more candidate chunks through.
MIN_RELEVANCE_SCORE = 0.15


def infer_tags(note):
    haystack = f"{note['path']} {note['name']} {note['content'][:1000]}".lower()
    tags = set()

    if any(token in haystack for token in ["profile", "about", "personal", "identity", "bio", "me"]):
        tags.update(["profile", "about", "personal", "identity"])
    if any(token in haystack for token in ["skill", "skills", "expertise", "technology", "stack"]):
        tags.update(["skills", "expertise"])
    if any(token in haystack for token in ["project", "projects", "portfolio", "build", "built"]):
        tags.update(["projects", "portfolio"])

    return sorted(tags)


def _dedupe_keep_order(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _query_contains_any(query: str, keywords: list[str]) -> bool:
    q_lower = query.lower()
    return any(keyword in q_lower for keyword in keywords)


def _make_source_filter(source: str) -> Callable:
    def source_filter(metadata):
        return metadata.get("source") == source

    return source_filter


def _make_tags_filter(tags: list[str]) -> Callable:
    def tags_filter(metadata):
        metadata_tags = metadata.get("tags", [])
        return any(tag in metadata_tags for tag in tags)

    return tags_filter


def search_with_debug_scores(query, vectorstore, k=5, filter_fn=None):
    docs_with_scores = vectorstore.similarity_search_with_relevance_scores(
        query,
        k=k,
        filter=filter_fn,
    )

    for doc, score in docs_with_scores:
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"Score: {score:.4f} | {preview}")

    return [doc for doc, score in docs_with_scores if score >= MIN_RELEVANCE_SCORE]


def get_priority_sources(query: str) -> list[str]:
    sources = [
        rule["source"]
        for rule in PRIORITY_RULES
        if _query_contains_any(query, rule["keywords"])
    ]
    return _dedupe_keep_order(sources)


def priority_source_search(query: str, vectorstore, k=5):
    sources = get_priority_sources(query)
    if not sources:
        return []

    results = []
    seen = set()

    for source in sources:
        docs = search_with_debug_scores(
            query=query,
            vectorstore=vectorstore,
            k=k,
            filter_fn=_make_source_filter(source),
        )

        for doc in docs:
            doc_key = (doc.metadata.get("source", ""), doc.page_content)
            if doc_key in seen:
                continue
            seen.add(doc_key)
            results.append(doc)
            if len(results) >= k:
                return results

    return results


def smart_search(query: str, vectorstore, k=5):
    priority_docs = priority_source_search(query=query, vectorstore=vectorstore, k=k)
    if priority_docs:
        return priority_docs

    q_lower = query.lower()
    for keyword, tags in TAG_KEYWORD_MAP.items():
        if keyword in q_lower:
            docs = search_with_debug_scores(
                query=query,
                vectorstore=vectorstore,
                k=k,
                filter_fn=_make_tags_filter(tags),
            )
            if docs:
                return docs

    docs = search_with_debug_scores(query=query, vectorstore=vectorstore, k=k)
    if docs:
        return docs

    # Final fallback if threshold filtering removed everything.
    return vectorstore.similarity_search(query, k=k)


def rewrite_query(query: str) -> list[str]:
    """Expand a query into multiple semantic variations."""
    rewrites = [query]
    q_lower = query.lower()

    for phrase, aliases in QUERY_REWRITE_RULES.items():
        if phrase in q_lower:
            rewrites.extend(aliases)

    for name, aliases in NAME_REWRITE_RULES.items():
        if name in q_lower:
            rewrites.extend(aliases)

    return _dedupe_keep_order(rewrites)


def smart_retrieve(query, vectorstore, k=5):
    queries = rewrite_query(query)
    seen = set()
    results = []

    for rewritten_query in queries:
        docs = smart_search(rewritten_query, vectorstore, k=k)
        for doc in docs:
            source = doc.metadata.get("source", "")
            doc_key = (source, doc.page_content)
            if doc_key in seen:
                continue
            seen.add(doc_key)
            results.append(doc)
            if len(results) >= k:
                return results

    return results[:k]


def find_relevant_notes(question, notes, top_n=5):
    keywords = [word.lower() for word in question.split() if len(word) > 3]
    scored = []

    for note in notes:
        search_text = (
            note["name"].lower()
            + " "
            + note["path"].lower()
            + " "
            + note["content"][:500].lower()
        )
        score = sum(1 for keyword in keywords if keyword in search_text)
        scored.append((score, note))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_matches = [note for score, note in scored if score > 0][:top_n]

    if top_matches:
        return top_matches

    return [note for _, note in scored[:top_n]]


def get_priority_notes(query: str, notes: list) -> list:
    priority_sources = get_priority_sources(query)
    if not priority_sources:
        return []

    return [note for note in notes if note.get("path") in priority_sources]


def find_relevant_notes_with_priority(query: str, notes: list, top_n=5) -> list:
    priority_notes = get_priority_notes(query, notes)
    keyword_results = find_relevant_notes(query, notes, top_n=top_n)

    seen = {note["path"] for note in priority_notes}
    merged = priority_notes[:]
    for note in keyword_results:
        if note["path"] in seen:
            continue
        merged.append(note)
        seen.add(note["path"])

    return merged[:top_n]


def retrieve_chunks(matched_notes, question, embeddings, splitter, k=8):
    documents = [
        Document(
            page_content=note["content"],
            metadata={"source": note["path"], "tags": infer_tags(note)},
        )
        for note in matched_notes
    ]
    chunks = splitter.split_documents(documents)
    store = FAISS.from_documents(chunks, embeddings)
    return smart_retrieve(question, store, k=k)
