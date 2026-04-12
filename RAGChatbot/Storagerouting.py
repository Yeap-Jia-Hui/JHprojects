import os
import glob
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic                  
from langchain_core.messages import HumanMessage, SystemMessage

# ── CONFIG ──────────────────────────────────────────────────────
ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]           
MODEL             = "claude-3-5-haiku-20241022"               

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50,
    separators=["\n## ", "\n### ", "\n\n", "\n", " "]
)
llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model=MODEL)  

# ── SIDEBAR: Upload .md files ──────────────────────────────────
st.set_page_config(page_title="Obsidian RAG", page_icon="📓")
st.title(" Obsidian RAG Chatbot (Claude)")

uploaded_files = st.sidebar.file_uploader(
    "Upload your Obsidian `.md` notes",
    type=["md"],
    accept_multiple_files=True
)

TEMP_DIR = "/tmp/obsidian_notes"
os.makedirs(TEMP_DIR, exist_ok=True)

if uploaded_files:
    for f in uploaded_files:
        with open(os.path.join(TEMP_DIR, f.name), "wb") as out:
            out.write(f.read())
    st.sidebar.success(f" {len(uploaded_files)} notes loaded")

# ── HELPERS ────────────────────────────────────────────────────
def get_all_note_paths():
    return glob.glob(os.path.join(TEMP_DIR, "**", "*.md"), recursive=True)

def find_relevant_files(question, all_paths):
    keywords = [w.lower() for w in question.split() if len(w) > 3]
    scored = [(sum(1 for kw in keywords if kw in os.path.basename(p).lower()), p) for p in all_paths]
    scored.sort(reverse=True)
    top = [p for s, p in scored if s > 0][:5]
    return top or sorted(all_paths, key=os.path.getmtime, reverse=True)[:5]

def read_and_retrieve(file_paths, question):
    from langchain_community.embeddings import HuggingFaceEmbeddings
    all_docs = []
    for path in file_paths:
        try:
            all_docs.extend(TextLoader(path, encoding="utf-8").load())
        except:
            pass
    if not all_docs:
        return [], []
    chunks    = splitter.split_documents(all_docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    store     = Chroma.from_documents(chunks, embeddings, collection_name="temp")
    retriever = store.as_retriever(search_kwargs={"k": 4})
    results   = retriever.invoke(question)
    store.delete_collection()
    sources   = list(set([os.path.basename(d.metadata.get("source", "")) for d in results]))
    return results, sources

# ── CHAT UI ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your notes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        all_paths = get_all_note_paths()
        if not all_paths:
            st.warning(" Please upload your Obsidian `.md` notes in the sidebar first.")
        else:
            with st.spinner(" Searching your notes..."):
                matched          = find_relevant_files(prompt, all_paths)
                results, sources = read_and_retrieve(matched, prompt)

            if not results:
                st.warning("No relevant content found in your notes.")
            else:
                context  = "\n\n---\n\n".join([d.page_content for d in results])
                messages = [
                    SystemMessage(content=(
                        "You are a helpful assistant. Answer using ONLY the "
                        "Obsidian notes below. Mention note names where relevant. "
                        "If the notes don't have enough info, say so clearly."
                    )),
                    HumanMessage(content=f"Notes:\n{context}\n\nQuestion: {prompt}")
                ]
                answer = llm.invoke(messages).content
                st.markdown(answer)
                st.caption(f"📓 Sources: {', '.join(sources)}")
                st.session_state.messages.append({"role": "assistant", "content": answer})