def get_classification_prompt(text: str) -> str:
    return f"""
Classify the recruiter input below as either "DETAILED" or "VAGUE".

Input:
\"\"\"{text}\"\"\"

Respond with one word only: DETAILED or VAGUE.
"""
