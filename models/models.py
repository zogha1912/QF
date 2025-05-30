

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from databse.database import Base
import enum

class RoleEnum(str, enum.Enum):
    employee = "employee"
    office_manager = "office_manager"

class StatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    job_title = Column(String)
    department = Column(String)
    start_date = Column(Date)
    contract_type = Column(String)
    email = Column(String, unique=True)
    password = Column(String)  
    role = Column(Enum(RoleEnum))

    requests = relationship("AttestationRequest", back_populates="employee")

class AttestationRequest(Base):
    __tablename__ = "attestation_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    request_date = Column(Date)
    request_type = Column(String)
    file_path = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="requests")