### app/schemas/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from models.models import RoleEnum, StatusEnum

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    job_title: str
    department: str
    start_date: date
    contract_type: str
    email: EmailStr
    role: RoleEnum

class EmployeeCreate(EmployeeBase):
    password: str  # 🔒 Add this

class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str

class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

class AttestationRequestCreate(BaseModel):
    employee_id: int
    request_date: date
    
class NLRequest(BaseModel):
    user_input: str    

class AttestationRequestOut(BaseModel):
    id: int
    employee_id: int
    status: StatusEnum
    request_date: date
    attestation_type: str

    class Config:
        orm_mode = True

