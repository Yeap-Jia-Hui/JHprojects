from langchain.schema import Document
from langchain_community.vectorstores import FAISS


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


def retrieve_chunks(matched_notes, question, embeddings, splitter, k=8):
    documents = [
        Document(page_content=note["content"], metadata={"source": note["path"]})
        for note in matched_notes
    ]
    chunks = splitter.split_documents(documents)
    store = FAISS.from_documents(chunks, embeddings)
    return store.as_retriever(search_kwargs={"k": k}).invoke(question)
