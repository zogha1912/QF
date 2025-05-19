# tools.py
from langchain.tools import tool
from .search import search_knowledge_base, generate_answer
from .embed_store import load_faiss_index

# Load once (or lazy load inside functions)
faiss_index, doc_store = load_faiss_index()

@tool
def retrieve_answer(query: str) -> str:
    """Search documents and return an AI-generated answer from company knowledge."""
    context_docs = search_knowledge_base(query, faiss_index, doc_store)
    return generate_answer(query, context_docs)
