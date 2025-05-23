# routers/attestation.py (example route)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from agents.om_agent.tools.classify_attestation import classify_attestation_request
from schemas.schemas import NLRequest
from models.models import Employee
from dependencies import get_current_user  
from databse.database import get_db

router = APIRouter()
@router.post("/attestation/classify/")
def classify_attestation(req: NLRequest, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    return classify_attestation_request(
        query=req.user_input,
        db=db,
        user_email=current_user.email
    )
