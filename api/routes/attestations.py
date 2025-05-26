# routers/attestation.py (example route)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from agents.om_agent.tools.classify_attestation import classify_attestation_request
from schemas.schemas import NLRequest
from models.models import Employee
from dependencies import get_current_user  
from databse.database import get_db
from fastapi.responses import FileResponse
from agents.om_agent.tools.generate_attestation_with_llm import generate_attestation_with_llm
from tools.doc_generator import create_attestation_docx


router = APIRouter()
@router.post("/attestation/classify/")
def classify_attestation(req: NLRequest, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    classification_result = classify_attestation_request(
    query=req.user_input,
    db=db,
    user_email=current_user.email
)

    classification_type = classification_result.get("type") if isinstance(classification_result, dict) else classification_result

    if classification_type == "self":
        attestation_text = generate_attestation_with_llm(current_user)
        file_path = create_attestation_docx(attestation_text)
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="attestation.docx"
        )

    return {"classification": classification_result}

""" @router.post("/attestation/generate/")
def generate_attestation(req: NLRequest, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    employee = current_user
    attestation_text = generate_attestation_with_llm(employee)
    file_path = create_attestation_docx(attestation_text)
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="attestation.docx") """
