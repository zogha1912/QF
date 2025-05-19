def get_clarification_prompt(text: str) -> str:
    return f"""
The following recruiter message is vague:

\"\"\"{text}\"\"\"

Generate 3 specific clarification questions about:
- the job title
- required skills
- experience or location

Keep them concise and to the point.
"""
