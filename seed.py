# seed.py
from sqlalchemy.orm import Session
from databse.database import SessionLocal
from models.models import Employee, RoleEnum
from passlib.context import CryptContext
from datetime import date


db: Session = SessionLocal()

def seed_users():
    employees = [
        Employee(
            first_name="Mohammed",
            last_name="Med",
            job_title="Quant analyst",
            department="IT",
            start_date=date(2023, 4, 1),
            contract_type="CDI",
            email="med@example.com",
            role=RoleEnum.employee
        ),
        Employee(
        first_name="Fatima",
        last_name="Zahra",
        job_title="Data Engineer",
        department="IT",
        start_date=date(2023, 4, 1),
        contract_type="CDI",
        email="fatima@example.com",
        role=RoleEnum.employee
    ),
    Employee(
        first_name="Ayoub",
        last_name="Nabil",
        job_title="Office Manager",
        department="Administration",
        start_date=date(2020, 1, 15),
        contract_type="CDD",
        email="nabil@example.com",
        role=RoleEnum.office_manager
    )
    ]

    db.add_all(employees)
    db.commit()
    db.close()
    
    
if __name__ == "__main__":
    seed_users()