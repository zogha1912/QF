# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.models import Employee
from databse.database import get_db
from tools.auth import get_email_from_token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/form")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Employee:
    email = get_email_from_token(token)
    user = db.query(Employee).filter(Employee.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
