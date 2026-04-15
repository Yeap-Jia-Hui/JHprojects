import streamlit as st

from rag_app.services.qa import answer_question, build_context, collect_sources
from rag_app.services.resources import load_embeddings, load_llm, load_splitter
from rag_app.services.retrieval import find_relevant_notes, retrieve_chunks
from rag_app.services.vault import fetch_vault_from_github


def render_sidebar():
    with st.sidebar:
        st.title("Obsidian RAG")
        st.markdown("---")

        if st.button("Refresh vault from GitHub"):
            st.cache_data.clear()
            st.rerun()

        notes, error = fetch_vault_from_github()

        if error:
            st.error(error)
            st.stop()
        if not notes:
            st.warning("No `.md` files found in repo")
            st.stop()

        st.success(f"{len(notes)} notes loaded")
        with st.expander("View loaded notes"):
            for note in notes:
                st.text(f"- {note['name']}")

        st.markdown("---")
        st.caption("Notes refresh every 5 minutes automatically.")
        st.caption("Push to your vault repo to update notes.")

        return notes


def render_chat(notes, embeddings, llm, splitter):
    st.title("Chat with your Obsidian Vault")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                st.caption(f"Sources: {message['sources']}")

    prompt = st.chat_input("Ask anything about your notes...")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching your vault..."):
            matched_notes = find_relevant_notes(prompt, notes)
            results = retrieve_chunks(matched_notes, prompt, embeddings, splitter)

        if not results:
            no_results_message = "No relevant content found in your notes for this question."
            st.warning(no_results_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": no_results_message}
            )
            return

        context = build_context(results)
        sources = collect_sources(results)
        answer = answer_question(llm, prompt, context)

        st.markdown(answer)
        st.caption(f"Sources: {', '.join(sources)}")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": ", ".join(sources),
            }
        )


def main():
    st.set_page_config(page_title="Obsidian RAG", page_icon=":books:", layout="wide")

    embeddings = load_embeddings()
    llm = load_llm()
    splitter = load_splitter()

    notes = render_sidebar()
    render_chat(notes, embeddings, llm, splitter)


if __name__ == "__main__":
    main()
