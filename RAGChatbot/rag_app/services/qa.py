from langchain_core.messages import HumanMessage, SystemMessage

SYSTEM_PROMPT = (
    "You are a precise assistant that answers questions ONLY using the notes provided below. "
    "Rules you must follow:\n"
    "1. Base your answer STRICTLY on the provided notes. Do not use outside knowledge.\n"
    "2. If the notes do not contain enough information to answer, say exactly: "
    "'I could not find this in your notes.' Do not guess or fill in gaps.\n"
    "3. Always cite the note name (e.g. 'According to RAG-Chatbot.md...') for every claim.\n"
    "4. Provide a one to two sentence summary of the files sourced. Do not add commentary not found in the notes.\n"
    "5. If the question is ambiguous, answer what the notes most closely support.\n"
)


def build_context(results):
    return "\n\n---\n\n".join([doc.page_content for doc in results])


def collect_sources(results):
    return sorted({doc.metadata.get("source", "") for doc in results if doc.metadata.get("source")})


def answer_question(llm, prompt, context):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"My notes:\n\n{context}\n\nQuestion: {prompt}"),
    ]
    return llm.invoke(messages).content
