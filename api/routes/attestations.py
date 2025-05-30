# routers/attestation.py (example route)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from agents.om_agent.tools.classify_attestation import classify_attestation_request
from schemas.schemas import NLRequest
from models.models import Employee, AttestationRequest, StatusEnum, RoleEnum
from dependencies import get_current_user  
from databse.database import get_db
from fastapi.responses import FileResponse
from agents.om_agent.tools.generate_attestation_with_llm import generate_attestation_with_llm
from tools.doc_generator import create_attestation_docx
from agents.om_agent.tools.notifier_simulation import notify_office_manager
from llm.prompts.attestation import get_attestation_extraction_prompt
from llm.deepseek_client import call_deepseek
import json


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
        """ attestation_text = generate_attestation_with_llm(current_user)
        file_path = create_attestation_docx(attestation_text) """
        
        attestation_request = AttestationRequest(
            employee_id=current_user.id,
            status=StatusEnum.pending,
            request_date=date.today(),
            request_type="self"
        )
        db.add(attestation_request)
        db.commit()
        db.refresh(attestation_request)
        
        
        """ notify_office_manager(
            employee_email=current_user.email,
            attestation_file_path=file_path
        )
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="attestation.docx"
        ) """

    return {"classification": classification_result}

""" @router.post("/attestation/generate/")
def generate_attestation(req: NLRequest, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    employee = current_user
    attestation_text = generate_attestation_with_llm(employee)
    file_path = create_attestation_docx(attestation_text)
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="attestation.docx") """

""" @router.post("/attestations/approve/{attestation_id}")
def approve_attestation(attestation_id: int, db: Session = Depends(get_db)):
    attestation = db.query(AttestationRequest).filter(AttestationRequest.id == attestation_id).first()
    if not attestation:
        raise HTTPException(status_code=404, detail="Attestation not found")

    attestation.status = StatusEnum.approved
    db.commit()
    return {"message": "Attestation approved successfully."} """

@router.post("/attestation/query-status")
def query_attestation_status(req: NLRequest, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):

    prompt = get_attestation_extraction_prompt(req.user_input)
    result = call_deepseek(prompt)
    print("DEBUG result type:", type(result))
    print("DEBUG result content:", result)
    import re

    def clean_json_string(s):
        # Enlève les balises ```json et ```
        return re.sub(r"```(?:json)?\s*|\s*```", "", s).strip()
    cleaned_result = clean_json_string(result)
    

    
    try:
        parsed = json.loads(cleaned_result)  # parse la string JSON en dict
    except json.JSONDecodeError:
        raise ValueError(f"Le contenu reçu n'est pas un JSON valide : {repr(result)}")

    if parsed.get("intent") != "query_status":
        return {"message": "Je ne comprends pas la requête."}

    #Fetch most recent request
    attestation = (
        db.query(AttestationRequest)
        .filter(AttestationRequest.employee_id == current_user.id)
        .order_by(AttestationRequest.request_date.desc())
        .first()
    )

    if not attestation:
        return {"message": "Aucune attestation trouvée."}

    return {
        "status": attestation.status,
        "message": f"Votre attestation est actuellement : {attestation.status}."
    }
@router.get("/attestation/pending")
def get_pending_attestations(db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    if current_user.role != RoleEnum.office_manager:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    requests = (
        db.query(AttestationRequest)
        .filter(AttestationRequest.status == StatusEnum.pending)
        .all()
    )

    response = []
    for req in requests:
        last_request = (
            db.query(AttestationRequest)
            .filter(
                AttestationRequest.employee_id == req.employee_id,
                AttestationRequest.id != req.id
            )
            .order_by(AttestationRequest.request_date.desc())
            .first()
        )

        response.append({
            "request_id": req.id,
            "employee_id": req.employee.id,
            "employee_name": f"{req.employee.first_name} {req.employee.last_name}",
            "job_title": req.employee.job_title,
            "department": req.employee.department,
            "current_request_date": req.request_date.isoformat(),
            "last_request_date": last_request.request_date.isoformat() if last_request else None,
        })

    return response
@router.post("/attestation/approve/{attestation_id}")
def approve_attestation(attestation_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    if current_user.role != RoleEnum.office_manager:
        raise HTTPException(status_code=403, detail="Not authorized")

    request = db.query(AttestationRequest).filter(AttestationRequest.id == attestation_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    employee = request.employee

    # Generate attestation
    attestation_text = generate_attestation_with_llm(employee)
    file_path = create_attestation_docx(attestation_text)

    request.status = StatusEnum.approved
    request.file_path = file_path
    db.commit()
    attestation_text = generate_attestation_with_llm(employee)
    file_path = create_attestation_docx(attestation_text)
    return FileResponse(
    path=file_path,
    filename="attestation.docx",
    media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@router.post("/attestation/reject/{attestation_id}")
def reject_attestation(attestation_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    if current_user.role != RoleEnum.office_manager:
        raise HTTPException(status_code=403, detail="Not authorized")

    attestation = db.query(AttestationRequest).filter(AttestationRequest.id == attestation_id).first()
    if not attestation:
        raise HTTPException(status_code=404, detail="Attestation not found")

    attestation.status = StatusEnum.rejected
    db.commit()
    return {"message": "Attestation rejected successfully."}
