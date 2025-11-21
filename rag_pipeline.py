from typing import List, Dict, Any, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import config

class RAGPipeline:
    def __init__(
        self, 
        openai_api_key: str,
        embedding_model: str = config.DEFAULT_EMBEDDING_MODEL,
        llm_model: str = config.DEFAULT_LLM_MODEL,
        chunk_size: int = config.DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = config.DEFAULT_CHUNK_OVERLAP,
        top_k: int = config.DEFAULT_TOP_K
    ):
        self.openai_api_key = openai_api_key
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self.text_splitter = None
        
    def initialize_components(self):
        self.embeddings = OpenAIEmbeddings(
            model=self.embedding_model,
            openai_api_key=self.openai_api_key
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
    def create_vectorstore(self, documents: List[Document]) -> Dict[str, Any]:
        if not self.embeddings or not self.text_splitter:
            self.initialize_components()
        
        chunks = self.text_splitter.split_documents(documents)
        
        if not chunks:
            raise ValueError("No text chunks were created from the documents")
        
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        return {
            "num_chunks": len(chunks),
            "vectorstore_type": "FAISS",
            "embedding_model": self.embedding_model
        }
    
    def create_qa_chain(self):
        if not self.vectorstore:
            raise ValueError("Vector store has not been created. Please process documents first.")
        
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.top_k}
        )
        
        llm = ChatOpenAI(
            model=self.llm_model,
            openai_api_key=self.openai_api_key,
            temperature=0.7
        )
        
        system_prompt = (
            "You are a helpful research assistant. Use the following pieces of context from academic papers to answer the question.\n\n"
            "Important instructions:\n"
            "- Only use information from the provided context to answer the question\n"
            "- If you don't know the answer based on the context, say 'I couldn't find that information in the uploaded documents'\n"
            "- When citing information, mention the source like 'According to the paper...' or 'Based on the document...'\n"
            "- Be precise and scholarly in your responses\n"
            "- If the context contains page numbers, reference them in your answer\n\n"
            "Context:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        self.qa_chain = create_retrieval_chain(retriever, question_answer_chain)
        
    def answer_question(self, question: str) -> Dict[str, Any]:
        if not self.qa_chain:
            self.create_qa_chain()
        
        result = self.qa_chain.invoke({"input": question})
        
        sources = []
        for doc in result.get("context", []):
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })
        
        return {
            "answer": result["answer"],
            "sources": sources
        }
    
    def get_retriever(self):
        if not self.vectorstore:
            raise ValueError("Vector store has not been created")
        return self.vectorstore.as_retriever(search_kwargs={"k": self.top_k})
