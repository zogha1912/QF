# routes/knowledge_management_routes.py
from fastapi import APIRouter, UploadFile, File
from agents.km_agent.extract_text import extract_text_from_pdf
from agents.km_agent.categorize import categorize_document
from agents.km_agent.embed_store import store_embedding, load_faiss_index, save_faiss_index
from agents.km_agent.search import search_knowledge_base, generate_answer
from agents.km_agent.models.schemas import QueryRequest
import shutil
import os

router = APIRouter()
faiss_index, doc_store = load_faiss_index()

@router.post("/knowledge/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(file_path)
    doc_type, category, summary = categorize_document(text)


    metadata = {
        "filename": file.filename,
        "content": text,
        "category": category,
        "summary": summary,
        "type": doc_type,
    }

    store_embedding(text, metadata, faiss_index, doc_store)
    save_faiss_index(faiss_index, doc_store)

    return {"message": "Document processed", "category": category, "summary": summary}


@router.post("/knowledge/query")
def query_documents(query: QueryRequest):
    context_docs = search_knowledge_base(query.query, faiss_index, doc_store)
    answer = generate_answer(query.query, context_docs)
    return {"answer": answer, "sources": context_docs}
