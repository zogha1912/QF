# api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databse.database import SessionLocal
from models.models import Employee
from schemas.schemas import EmployeeLogin, EmployeeCreate
from tools.auth import verify_password, create_access_token, hash_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(employee.password)
    new_employee = Employee(**employee.dict(exclude={"password"}), password=hashed_pw)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {"msg": "Employee registered successfully"}

@router.post("/login/form")
def login_with_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == form_data.username).first()
    if not employee or not verify_password(form_data.password, employee.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": employee.email, "role": employee.role})
    return {
    "access_token": token,
    "token_type": "bearer",
    "user": {
        "id": employee.id,
        "email": employee.email,
        "role": employee.role,
        "name": f"{employee.first_name} {employee.last_name}"
    }
    }


