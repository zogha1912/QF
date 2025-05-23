# prompts/attestation.py

def get_attestation_extraction_prompt(user_input: str) -> str:
    return f"""
Extract the following info from the user's request in JSON format:
- intent: (e.g. request_attestation, query_status)
- employee_name: full name of employee the attestation is for
- requester_name: full name of requester if mentioned
- attestation_type: type of attestation requested (work, salary, etc)
- date: date mentioned or empty string

User request: \"\"\"{user_input}\"\"\"

Respond only with a JSON object.
"""
