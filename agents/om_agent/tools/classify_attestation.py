# agents/office_manager/tools/classify_attestation.py

from llm.deepseek_client import call_deepseek
from sqlalchemy.orm import Session
from models.models import Employee

def classify_attestation_request(query: str, db: Session, user_email: str) -> dict:
    """
    Classify the attestation request using DeepSeek LLM.
    Returns:
      {
        "type": "self" | "other",
        "target_name": "Hassan Hassan"  # if 'other'
      }
    """

    # Get logged-in user info
    user = db.query(Employee).filter(Employee.email == user_email).first()
    user_full_name = f"{user.first_name} {user.last_name}"

    # Get all employee names (for better disambiguation)
    employees = db.query(Employee).all()
    employee_names = [f"{e.first_name} {e.last_name}" for e in employees]

    # Create the prompt
    prompt = f"""
You are an office assistant. A user is requesting an employment certificate ("attestation d'emploi").

You need to identify:
- Is the user asking for their own attestation (type = "self")
- Or asking for someone else's attestation (type = "other")

User's full name: {user_full_name}
List of employees: {employee_names}

User said: "{query}"

Return a JSON like:
{{"type": "self"}} or {{"type": "other", "target_name": "Employee Name"}}
"""

    # Call DeepSeek
    raw = call_deepseek(prompt, max_tokens=200)

    try:
        result = eval(raw.strip()) if isinstance(raw, str) else raw
    except Exception:
        result = {"type": "self"}

    return result
