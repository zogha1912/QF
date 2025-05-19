def get_extraction_prompt(text: str) -> str:
    return f"""
Extract the following fields in JSON format from this recruiter input:

Fields:
- Job Title
- Skills
- Experience
- Location

Input:
\"\"\"{text}\"\"\"
"""
