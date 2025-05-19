from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
index_path = "data/faiss_index.faiss"
meta_path = "data/metadata.pkl"

faiss_dim = 384

def load_faiss_index():
    if os.path.exists(index_path) and os.path.exists(meta_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            doc_store = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(faiss_dim)
        doc_store = []
    return index, doc_store

#  Global init using the function
index, doc_store = load_faiss_index()

def save_faiss_index(index, doc_store):
    os.makedirs("data", exist_ok=True)
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(doc_store, f)

def store_embedding(text, metadata, index, doc_store):
    embedding = model.encode([text])[0]
    index.add(np.array([embedding]))
    doc_store.append({
        "embedding": embedding.tolist(),
        "metadata": metadata,
        "content": text
    })
