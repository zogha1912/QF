from fastapi import APIRouter, UploadFile, File
from typing import List
from tools.file_utils import extract_texts_from_multiple_pdfs
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from agents.recruitment_agent.tools.classify_candidate import classify_candidate

router = APIRouter()

@router.post("/classify-multiple")
async def classify_multiple_cvs(
    files: List[UploadFile] = File(...), 
    job_desc: str = ""
):
    file_bytes = [await file.read() for file in files]
    cv_texts = extract_texts_from_multiple_pdfs(file_bytes)

    results = []
    for idx, text in enumerate(cv_texts):
        classification = classify_candidate(text, job_desc)
        results.append({
            "file_name": files[idx].filename,
            "classification": classification
        })

    return {"results": results}
