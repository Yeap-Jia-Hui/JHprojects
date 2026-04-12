#!/usr/bin/env python3
"""
Deployment check script for RAG Chatbot
Run this to verify all imports work before deploying to Streamlit
"""

def check_imports():
    """Check if all required imports are available"""
    imports = [
        ("streamlit", "streamlit"),
        ("langchain_community.document_loaders", "TextLoader"),
        ("langchain_text_splitters", "RecursiveCharacterTextSplitter"),
        ("langchain_community.vectorstores", "Chroma"),
        ("langchain_openai", "OpenAIEmbeddings, ChatOpenAI"),
        ("langchain_core.messages", "HumanMessage, SystemMessage"),
        ("openai", "openai"),
    ]

    failed = []
    for module, components in imports:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
            failed.append(module)

    if failed:
        print(f"\n❌ {len(failed)} imports failed. Please install missing packages:")
        print("pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ All {len(imports)} imports successful!")
        return True

def check_versions():
    """Check versions of key packages"""
    try:
        import streamlit as st
        print(f"Streamlit version: {st.__version__}")
    except:
        pass

    try:
        import langchain
        print(f"LangChain version: {langchain.__version__}")
    except:
        pass

    try:
        import openai
        print(f"OpenAI version: {openai.__version__}")
    except:
        pass

if __name__ == "__main__":
    print("🔍 Checking RAG Chatbot deployment requirements...\n")

    success = check_imports()
    print("\n📦 Package versions:")
    check_versions()

    if success:
        print("\n🚀 Ready for deployment to Streamlit Cloud!")
        print("Main file: RAGChatbot/streamlit_app.py")
    else:
        print("\n❌ Fix import issues before deploying.")