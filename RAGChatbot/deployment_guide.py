#!/usr/bin/env python3
"""
Deployment guide for RAG Chatbot
Helps users choose the right file for their deployment method
"""

def main():
    print("🤖 RAG Chatbot Deployment Guide")
    print("=" * 40)

    print("\n📋 Available deployment options:")
    print("1. Streamlit Cloud (web app with OpenAI)")
    print("2. Local Streamlit (web app with OpenAI)")
    print("3. Local Ollama (terminal app with local LLM)")

    while True:
        try:
            choice = input("\nChoose your deployment method (1-3): ").strip()

            if choice == "1":
                print("\n🌐 Streamlit Cloud Deployment:")
                print("   📄 Main file: streamlit_app.py")
                print("   🔑 Requires: OpenAI API key")
                print("   🚀 Command: Upload to share.streamlit.io")
                print("   ⚠️  DO NOT use Storagerouting.py")

            elif choice == "2":
                print("\n💻 Local Streamlit Deployment:")
                print("   📄 Main file: streamlit_app.py")
                print("   🔑 Requires: OpenAI API key")
                print("   🚀 Command: streamlit run streamlit_app.py")
                print("   ⚠️  DO NOT use Storagerouting.py")

            elif choice == "3":
                print("\n🏠 Local Ollama Deployment:")
                print("   📄 Main file: Storagerouting.py")
                print("   🔑 Requires: Ollama installed locally")
                print("   🚀 Command: python Storagerouting.py")
                print("   ⚠️  ollama serve must be running")

            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                continue

            print("\n✅ Ready to deploy!")
            break

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()