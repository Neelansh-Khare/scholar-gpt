import os
from typing import Dict, Any

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_LLM_MODEL = "gpt-4o-mini"
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 4

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

RAG_PROMPT_TEMPLATE = """You are a helpful research assistant. Use the following pieces of context from academic papers to answer the question at the end. 

Important instructions:
- Only use information from the provided context to answer the question
- If you don't know the answer based on the context, say "I couldn't find that information in the uploaded documents"
- When citing information, mention the source like "According to the paper..." or "Based on the document..."
- Be precise and scholarly in your responses
- If the context contains page numbers, reference them in your answer

Context:
{context}

Question: {question}

Answer: """

def get_config() -> Dict[str, Any]:
    return {
        "embedding_model": DEFAULT_EMBEDDING_MODEL,
        "llm_model": DEFAULT_LLM_MODEL,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
        "top_k": DEFAULT_TOP_K,
        "openai_api_key_env": OPENAI_API_KEY_ENV,
        "prompt_template": RAG_PROMPT_TEMPLATE
    }
