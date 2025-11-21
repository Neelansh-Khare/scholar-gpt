# ScholarGPT 📚

A production-ready Streamlit web application that enables you to chat with your academic papers using Retrieval-Augmented Generation (RAG). Upload PDFs, ask questions, and get intelligent answers grounded in your documents.

## Features

- **Multi-PDF Upload**: Upload and process multiple academic papers simultaneously
- **Intelligent Text Extraction**: Uses PyMuPDF for robust PDF text extraction with page tracking
- **Vector Search**: FAISS-based vector store for efficient similarity search
- **RAG Pipeline**: LangChain-powered retrieval-augmented generation for accurate answers
- **Source Attribution**: See exactly which parts of your documents were used to generate answers
- **Configurable Parameters**: Adjust chunk size, overlap, retrieval count, and model settings
- **Chat History**: Maintains conversation context within your session
- **Clean UI**: Intuitive Streamlit interface designed for researchers

## Tech Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyMuPDF (fitz)
- **RAG Framework**: LangChain
- **Vector Database**: FAISS
- **Embeddings & LLM**: OpenAI (text-embedding-3-small, gpt-4o-mini)
- **Language**: Python 3.11+

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── pdf_utils.py        # PDF text extraction utilities
├── rag_pipeline.py     # LangChain RAG pipeline implementation
├── config.py           # Configuration constants
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Local Setup

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   You can either:
   
   - Set it as an environment variable:
     ```bash
     # On Linux/Mac
     export OPENAI_API_KEY='your-api-key-here'
     
     # On Windows (Command Prompt)
     set OPENAI_API_KEY=your-api-key-here
     
     # On Windows (PowerShell)
     $env:OPENAI_API_KEY='your-api-key-here'
     ```
   
   - Or enter it directly in the app's sidebar when you run it

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## Deployment

### Deploying on Replit

1. **Import the project** to Replit or create a new Repl and upload the files

2. **Add your API key** to Replit Secrets:
   - Open the "Secrets" tab (lock icon in the sidebar)
   - Add a new secret: `OPENAI_API_KEY` with your OpenAI API key as the value

3. **Run the application**:
   - The app will automatically start with the configured command
   - Or manually run: `streamlit run app.py --server.port=5000 --server.address=0.0.0.0`

4. **Access your app** through the Replit webview

### Deploying on Hugging Face Spaces

1. **Create a new Space** on Hugging Face:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Select **Streamlit** as the SDK

2. **Upload your files**:
   - Upload all Python files (`app.py`, `pdf_utils.py`, `rag_pipeline.py`, `config.py`)
   - Upload `requirements.txt`

3. **Add your API key** as a secret:
   - Go to Space Settings → Repository Secrets
   - Add `OPENAI_API_KEY` with your OpenAI API key

4. **Your app will automatically build and deploy**

## Usage Guide

### Step 1: Configure Settings

In the sidebar:
- Enter your OpenAI API key (or use environment variable)
- Select embedding model (default: text-embedding-3-small)
- Select LLM model (default: gpt-4o-mini)
- Optionally adjust advanced RAG parameters:
  - **Chunk Size**: Size of text segments (default: 1000 characters)
  - **Chunk Overlap**: Overlap between chunks (default: 200 characters)
  - **Top-K**: Number of relevant chunks to retrieve (default: 4)

### Step 2: Upload PDFs

- Click "Browse files" or drag-and-drop PDF files
- You can upload multiple academic papers at once
- Click "Process PDFs" to extract text and create embeddings

### Step 3: Ask Questions

- Once processing is complete, use the chat interface to ask questions
- The system will:
  1. Find the most relevant sections from your documents
  2. Generate an answer based on those sections
  3. Show source attribution with page numbers
- View sources by expanding the "View Sources" section under each answer

### Step 4: Continue the Conversation

- Ask follow-up questions
- The chat history is maintained during your session
- Reset and upload new documents using the sidebar button

## Configuration Options

### Model Selection

**Embedding Models:**
- `text-embedding-3-small` (default) - Fast and cost-effective
- `text-embedding-3-large` - Higher quality embeddings
- `text-embedding-ada-002` - Legacy model

**LLM Models:**
- `gpt-4o-mini` (default) - Best balance of speed and quality
- `gpt-4o` - Most capable model
- `gpt-4-turbo` - High performance
- `gpt-3.5-turbo` - Fastest and cheapest

### RAG Parameters

Adjust these based on your documents:

- **Chunk Size (500-2000)**: Larger chunks = more context per chunk, but less precise retrieval
- **Chunk Overlap (0-500)**: Higher overlap = better continuity, but more redundancy
- **Top-K (1-10)**: More chunks = more context for LLM, but potentially more noise

## Error Handling

The application handles common errors gracefully:

- **Missing API Key**: Clear warning with instructions
- **Invalid PDFs**: Skips corrupted files, processes the rest
- **Empty Documents**: Alerts user if no text could be extracted
- **Processing Failures**: Detailed error messages for debugging

## Limitations

- **PDF Quality**: Text extraction quality depends on the source PDF
- **Scanned PDFs**: May not work well with image-based PDFs (OCR not included)
- **Large Files**: Very large PDFs may take longer to process
- **API Costs**: Usage incurs OpenAI API costs for embeddings and completions

## Cost Estimation

Approximate costs per paper (10-page academic paper, ~5000 words):

- Embedding creation: ~$0.001-0.002
- Each question/answer: ~$0.01-0.05 (depending on model)

Using gpt-4o-mini and text-embedding-3-small keeps costs very low.

## Troubleshooting

**Issue**: "No text could be extracted from PDFs"
- **Solution**: Ensure PDFs contain actual text (not just scanned images)

**Issue**: Slow processing
- **Solution**: Reduce chunk size or process fewer PDFs at once

**Issue**: Irrelevant answers
- **Solution**: Increase Top-K value to retrieve more context, or adjust chunk size

**Issue**: API errors
- **Solution**: Verify API key is correct and has available credits

## Contributing

Feel free to fork this project and submit improvements!

Potential enhancements:
- Support for additional document formats (DOCX, TXT, HTML)
- OCR support for scanned PDFs
- Conversation memory across sessions
- Document comparison features
- Export chat transcripts
- Alternative vector stores (ChromaDB, Pinecone)

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

**Happy Researching! 📚✨**
