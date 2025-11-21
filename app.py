import streamlit as st
import os
from typing import List, Dict
from pdf_utils import process_multiple_pdfs
from rag_pipeline import RAGPipeline
import config

st.set_page_config(
    page_title="ScholarGPT",
    page_icon="📚",
    layout="wide"
)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = None
    if "documents_processed" not in st.session_state:
        st.session_state.documents_processed = False
    if "vectorstore_info" not in st.session_state:
        st.session_state.vectorstore_info = None
    if "pdf_metadata" not in st.session_state:
        st.session_state.pdf_metadata = []

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("🔑 API Key")
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value="",
            help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
        )
        
        api_key = api_key_input if api_key_input else os.environ.get("OPENAI_API_KEY", "")
        
        if api_key:
            st.success("✓ API Key configured")
        else:
            st.warning("⚠️ API Key required")
        
        st.divider()
        
        st.subheader("🤖 Model Settings")
        embedding_model = st.selectbox(
            "Embedding Model",
            ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"],
            index=0,
            help="Model used to create embeddings from text"
        )
        
        llm_model = st.selectbox(
            "LLM Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0,
            help="Model used to generate answers"
        )
        
        st.divider()
        
        with st.expander("🔧 Advanced RAG Parameters"):
            chunk_size = st.slider(
                "Chunk Size",
                min_value=500,
                max_value=2000,
                value=config.DEFAULT_CHUNK_SIZE,
                step=100,
                help="Size of text chunks for embedding"
            )
            
            chunk_overlap = st.slider(
                "Chunk Overlap",
                min_value=0,
                max_value=500,
                value=config.DEFAULT_CHUNK_OVERLAP,
                step=50,
                help="Overlap between consecutive chunks"
            )
            
            top_k = st.slider(
                "Top-K Retrieved Documents",
                min_value=1,
                max_value=10,
                value=config.DEFAULT_TOP_K,
                help="Number of document chunks to retrieve for each question"
            )
        
        st.divider()
        
        if st.session_state.documents_processed:
            st.success("✓ Documents loaded")
            if st.button("🔄 Reset & Upload New PDFs"):
                st.session_state.messages = []
                st.session_state.rag_pipeline = None
                st.session_state.documents_processed = False
                st.session_state.vectorstore_info = None
                st.session_state.pdf_metadata = []
                st.rerun()
    
    return api_key, embedding_model, llm_model, chunk_size, chunk_overlap, top_k

def render_header():
    st.title("📚 ScholarGPT")
    st.markdown("**Chat with your academic papers** - Upload research PDFs and ask questions about them")
    st.divider()

def render_pdf_upload(api_key, embedding_model, llm_model, chunk_size, chunk_overlap, top_k):
    st.subheader("📄 Upload Academic PDFs")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more research papers in PDF format"
    )
    
    if uploaded_files and not st.session_state.documents_processed:
        if not api_key:
            st.error("❌ Please provide an OpenAI API key in the sidebar to continue")
            return
        
        if st.button("🚀 Process PDFs", type="primary"):
            process_pdfs(uploaded_files, api_key, embedding_model, llm_model, chunk_size, chunk_overlap, top_k)
    
    if st.session_state.documents_processed and st.session_state.pdf_metadata:
        render_document_info()

def process_pdfs(uploaded_files, api_key, embedding_model, llm_model, chunk_size, chunk_overlap, top_k):
    with st.status("Processing PDFs...", expanded=True) as status:
        st.write("📖 Extracting text from PDFs...")
        try:
            documents, metadata = process_multiple_pdfs(uploaded_files)
            st.session_state.pdf_metadata = metadata
            
            if not documents:
                st.error("❌ No text could be extracted from the uploaded PDFs")
                return
            
            st.write(f"✓ Extracted text from {len(uploaded_files)} PDF(s)")
            
            st.write("🔢 Creating text chunks...")
            rag_pipeline = RAGPipeline(
                openai_api_key=api_key,
                embedding_model=embedding_model,
                llm_model=llm_model,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                top_k=top_k
            )
            
            st.write("🧮 Generating embeddings and building vector store...")
            vectorstore_info = rag_pipeline.create_vectorstore(documents)
            st.session_state.vectorstore_info = vectorstore_info
            
            st.write("🤖 Initializing QA chain...")
            rag_pipeline.create_qa_chain()
            
            st.session_state.rag_pipeline = rag_pipeline
            st.session_state.documents_processed = True
            
            status.update(label="✅ Processing complete!", state="complete")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error processing PDFs: {str(e)}")
            status.update(label="❌ Processing failed", state="error")

def render_document_info():
    st.success("✅ Documents successfully processed!")
    
    with st.expander("📊 View Document Details", expanded=False):
        for meta in st.session_state.pdf_metadata:
            if "error" in meta:
                st.error(f"**{meta['filename']}**: {meta['error']}")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("File", meta['filename'])
                with col2:
                    st.metric("Pages", meta['total_pages'])
                with col3:
                    st.metric("Characters", f"{meta['total_text_length']:,}")
        
        if st.session_state.vectorstore_info:
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Text Chunks", st.session_state.vectorstore_info['num_chunks'])
            with col2:
                st.metric("Vector Store", st.session_state.vectorstore_info['vectorstore_type'])

def render_chat_interface():
    if not st.session_state.documents_processed:
        st.info("👆 Please upload and process PDF documents to start chatting")
        return
    
    st.subheader("💬 Ask Questions")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "sources" in message:
                render_sources(message["sources"])
    
    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.rag_pipeline.answer_question(prompt)
                    answer = result["answer"]
                    sources = result["sources"]
                    
                    st.markdown(answer)
                    render_sources(sources)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error generating answer: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

def render_sources(sources: List[Dict]):
    if sources:
        with st.expander(f"📚 View Sources ({len(sources)} chunks retrieved)"):
            for i, source in enumerate(sources, 1):
                st.markdown(f"**Source {i}** - {source['metadata'].get('source', 'Unknown')} (Page {source['metadata'].get('page', 'N/A')})")
                st.text(source['content'])
                st.divider()

def main():
    initialize_session_state()
    
    api_key, embedding_model, llm_model, chunk_size, chunk_overlap, top_k = render_sidebar()
    
    render_header()
    
    render_pdf_upload(api_key, embedding_model, llm_model, chunk_size, chunk_overlap, top_k)
    
    st.divider()
    
    render_chat_interface()
    
    st.divider()
    st.caption("Built with Streamlit, LangChain, FAISS, and OpenAI")

if __name__ == "__main__":
    main()
