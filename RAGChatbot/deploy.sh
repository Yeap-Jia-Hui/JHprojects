#!/bin/bash
# Streamlit deployment script for RAG Chatbot

echo "🚀 Deploying RAG Chatbot to Streamlit Cloud..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found!"
    exit 1
fi

echo "✅ Files found. Ready for deployment!"
echo ""
echo "📋 Deployment Steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Connect your GitHub account"
echo "3. Select this repository"
echo "4. Set main file path to: RAGChatbot/app.py"
echo "5. Deploy!"
echo ""
echo "🔑 Don't forget to add your OPENAI_API_KEY in app secrets!"