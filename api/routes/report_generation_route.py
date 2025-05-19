

from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from agents.recruitment_agent.tools.generate_report import generate_candidate_report
from tools.file_utils import extract_text_from_pdf_ocr
import io

router = APIRouter()

@router.post("/generate-reports/")
async def generate_reports_from_pdfs(
    files: List[UploadFile] = File(...),
    position: str = Form(...)
):
    reports = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            return {"error": f"File {file.filename} is not a PDF."}
        
        content = await file.read()
        pdf_text = extract_text_from_pdf_ocr(content)

        report = generate_candidate_report(pdf_text, position)
        reports.append({
            "filename": file.filename,
            "report": report
        })

    return {"reports": reports}
