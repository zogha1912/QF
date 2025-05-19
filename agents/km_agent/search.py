#search.py
from agents.km_agent import embed_store
import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_URL")

def search_knowledge_base(query, index, doc_store, top_k=3, filter_type=None):
    print(f"[KM AGENT] Searching knowledge base for query: {query}")
    query_vec = embed_store.model.encode([query])[0]
    D, I = index.search(np.array([query_vec]), top_k)
    results = []
    for i in I[0]:
        if i < len(doc_store):
            doc = doc_store[i]
            if not filter_type or doc["metadata"].get("type") == filter_type:
                results.append(doc)
    return results


def generate_answer(query, context_docs):
    print(f"[KM AGENT] Generating answer from context. Context docs count: {len(context_docs)}")
    context = "\n---\n".join([doc["content"][:1000] for doc in context_docs])

    prompt = f"""
    You are a helpful AI assistant with access to company documents.

    Context:
    {context}

    Question: {query}

    Provide a clear, concise answer based on the context above.Answer only using the context. If the answer is not present in the context, say: "I'm sorry I don't have the information you're asking for." 
    """

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]
