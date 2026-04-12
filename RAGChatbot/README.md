# RAG Chatbot with Document Q&A

A Streamlit web application that allows you to upload documents and chat with them using Retrieval-Augmented Generation (RAG).

## 🚨 Deployment Quick Reference

| Deployment Method | Main File | Requirements |
|------------------|-----------|--------------|
| **Streamlit Cloud** | `streamlit_app.py` | OpenAI API key |
| **Local with Ollama** | `Storagerouting.py` | Ollama installed locally |
| **Local Streamlit** | `streamlit_app.py` | OpenAI API key |

**❌ Don't deploy `Storagerouting.py` to Streamlit Cloud** - it requires local Ollama which isn't available in the cloud.

## Features

- 📁 Upload multiple text/markdown files
- 🤖 Chat with your documents using OpenAI GPT models
- 🔍 Semantic search through document chunks
- 📄 Source attribution for answers
- 💾 Persistent chat history during session

## Local Development

### For Streamlit Web App (Recommended):
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### For Local Ollama (Requires Ollama installed):
```bash
pip install -r requirements.txt
# Make sure Ollama is running: ollama serve
python Storagerouting.py
```

Open your browser to `http://localhost:8501`

## Streamlit Cloud Deployment

### ⚠️ IMPORTANT: Use the Correct File!

**For Streamlit Cloud deployment, use `streamlit_app.py` as your main file.**

**❌ DO NOT use `Storagerouting.py` for Streamlit Cloud** - it's designed for local Ollama usage only.

### Method 1: Direct GitHub Deployment

1. **Fork or upload this repository to GitHub**

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Connect your GitHub account** and select this repository

4. **Configure the app**:
   - **Main file path**: `RAGChatbot/streamlit_app.py` ⚠️
   - **URL slug**: (optional, leave blank for auto-generated)

5. **Add secrets** (optional, for production):
   - Go to your app settings
   - Add `OPENAI_API_KEY` in the secrets section

6. **Deploy!** Click "Deploy"

### Method 2: Manual Upload

1. **Create a zip file** containing:
   - `streamlit_app.py` ⚠️
   - `requirements.txt`
   - `.streamlit/config.toml`
   - Any other necessary files

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Upload the zip file** instead of connecting GitHub

## Usage

1. **Enter your OpenAI API key** in the sidebar
2. **Upload your documents** (txt, md, pdf files)
3. **Wait for processing** (embeddings will be created)
4. **Start chatting!** Ask questions about your documents

## Configuration Options

- **Embedding Model**: Choose between `text-embedding-3-small` or `text-embedding-3-large`
- **Chat Model**: Select from `gpt-3.5-turbo`, `gpt-4`, or `gpt-4-turbo`
- **Chunk Size**: Adjust how documents are split (200-2000 characters)
- **Chunk Overlap**: Set overlap between chunks (0-200 characters)

## Deployment Checklist

Before deploying to Streamlit Cloud, run:

```bash
python check_deployment.py
```

This will verify all required packages are installed.

## Important Notes

- **API Key Required**: You need an OpenAI API key for both embeddings and chat
- **File Size Limits**: Streamlit has file upload limits (usually 200MB total)
- **Cost**: OpenAI API calls will incur costs based on usage
- **Privacy**: Documents are processed in memory and not stored permanently

## Troubleshooting

### Import Errors
If you get import errors, make sure all requirements are installed:
```bash
pip install --upgrade -r requirements.txt
```

### API Key Issues
- Make sure your OpenAI API key is valid and has sufficient credits
- Check that the key has access to the selected models

### File Processing Errors
- Ensure your files are valid text/markdown format
- Check file encoding (UTF-8 recommended)
- Try smaller files if processing fails

### Streamlit Cloud Issues
- Make sure you're using `streamlit_app.py` as the main file, **NOT** `Storagerouting.py`
- Check that all files are in the `RAGChatbot/` directory
- Verify your `requirements.txt` includes all dependencies
- If you get `langchain_ollama` errors, you're using the wrong file for deployment

## Local Ollama Version

If you prefer to use Ollama locally instead of OpenAI, use the `Storagerouting.py` file. Note that Ollama won't work on Streamlit Cloud since it's a local service.

## License

MIT License - feel free to modify and distribute!