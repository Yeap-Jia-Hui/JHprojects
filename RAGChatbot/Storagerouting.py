import os
import glob
from langchain_community.document_loaders import ObsidianLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# ── CONFIG ──────────────────────────────────────────────────────
VAULT_PATH   = r"C:\Users\yeapj\OneDrive\Documents\Obsidian\claude-repo" # ← change this
OLLAMA_MODEL = "llama3"
TOP_N_FILES  = 5   # how many files to load per question

splitter   = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n## ", "\n### ", "\n\n", "\n", " "]
)
embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
llm        = ChatOllama(model=OLLAMA_MODEL)

# ── STEP 1: Index just filenames (no file content loaded) ────────
def get_all_note_paths(vault_path):
    return glob.glob(os.path.join(vault_path, "**", "*.md"), recursive=True)

def find_relevant_files(question: str, all_paths: list, top_n: int = TOP_N_FILES):
    """
    Cheap keyword match against filenames and folder names only.
    No file content is read here — just paths.
    """
    keywords = [w.lower() for w in question.split() if len(w) > 3]
    scored = []
    for path in all_paths:
        name = os.path.basename(path).lower().replace(".md", "")
        folder = os.path.dirname(path).lower()
        score = sum(1 for kw in keywords if kw in name or kw in folder)
        scored.append((score, path))

    # Sort by score, take top N, fall back to most recently modified if no keyword match
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [p for s, p in scored if s > 0][:top_n]

    if not top:
        # fallback: pick most recently modified notes
        top = sorted(all_paths, key=os.path.getmtime, reverse=True)[:top_n]
        print(f"   No keyword match — using {top_n} most recent notes as fallback")

    return top

# ── STEP 2: Load + embed only the selected files ─────────────────
def load_and_retrieve(file_paths: list, question: str):
    from langchain_community.document_loaders import TextLoader

    docs = []
    for path in file_paths:
        try:
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
        except Exception as e:
            print(f"   ⚠️ Could not load {path}: {e}")

    if not docs:
        return []

    chunks = splitter.split_documents(docs)

    # Temporary in-memory vector store — no disk write, freed after each question
    temp_store = Chroma.from_documents(
        chunks,
        embeddings,
        collection_name="temp_query"   # overwritten each time
    )
    retriever = temp_store.as_retriever(search_kwargs={"k": 4})
    return retriever.invoke(question)

# ── STEP 3: Ask function ─────────────────────────────────────────
def ask(question: str, all_paths: list):
    print(f"\n🔍 Scanning {len(all_paths)} filenames...")
    relevant_files = find_relevant_files(question, all_paths)

    print(f"   Loading {len(relevant_files)} matched notes:")
    for f in relevant_files:
        print(f"   - {os.path.basename(f)}")

    results = load_and_retrieve(relevant_files, question)

    if not results:
        print("⚠️  Nothing useful found in matched notes.\n")
        return

    sources = list(set([os.path.basename(doc.metadata.get("source", "")) for doc in results]))
    context = "\n\n---\n\n".join([doc.page_content for doc in results])

    messages = [
        SystemMessage(content="Answer using only the user's Obsidian notes below. If unsure, say so."),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}")
    ]
    answer = llm.invoke(messages)
    print(f"\n📓 Sources: {', '.join(sources)}")
    print(f"\n{answer.content}\n")

# ── STEP 4: Chat loop ─────────────────────────────────────────────
all_paths = get_all_note_paths(VAULT_PATH)
print(f"📂 Found {len(all_paths)} notes in vault (filenames only, not loaded yet)")
print("💬 Type your question. Type 'exit' to quit.\n")

while True:
    q = input("You: ").strip()
    if q.lower() in ("exit", "quit", "q"):
        break
    if q:
        ask(q, all_paths)