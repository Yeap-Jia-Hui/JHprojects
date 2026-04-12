import os, glob, base64, requests
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document

# ── Load ONCE at startup using Streamlit's cache ─────────────────

@st.cache_resource   # cached for entire session lifetime
def load_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def load_llm():
    return ChatAnthropic(
        api_key=st.secrets["ANTHROPIC_API_KEY"],
        model="claude-3-5-haiku-20241022"
    )

@st.cache_resource
def load_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )

embeddings = load_embeddings()   # ← loads ONCE, reused every question
llm        = load_llm()
splitter   = load_splitter()

# ── Fetch vault ONCE every 5 mins ────────────────────────────────

@st.cache_data(ttl=300)
def fetch_vault_from_github():
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    GITHUB_REPO  = st.secrets["GITHUB_REPO"]
    headers      = {"Authorization": f"token {GITHUB_TOKEN}"}
    url          = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/main?recursive=1"
    resp         = requests.get(url, headers=headers)

    if resp.status_code != 200:
        st.error(f"GitHub fetch failed: {resp.status_code}")
        return []

    tree     = resp.json().get("tree", [])
    md_files = [f for f in tree if f["path"].endswith(".md")]
    notes    = []

    for f in md_files:
        blob    = requests.get(f["url"], headers=headers).json()
        content = base64.b64decode(blob["content"]).decode("utf-8", errors="ignore")
        notes.append({
            "name":    os.path.basename(f["path"]),
            "path":    f["path"],
            "content": content
        })

    return notes

# ── Retrieve chunks (embeddings already loaded, no re-download) ───

def retrieve_chunks(matched_notes, question):
    docs    = [Document(page_content=n["content"], metadata={"source": n["name"]}) for n in matched_notes]
    chunks  = splitter.split_documents(docs)
    store   = Chroma.from_documents(chunks, embeddings, collection_name="temp_vault")
    results = store.as_retriever(search_kwargs={"k": 4}).invoke(question)
    store.delete_collection()
    return results