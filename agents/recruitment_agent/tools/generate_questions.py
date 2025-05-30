# tools/generate_questions.py
from llm.prompts.recruitment_prompts import get_interview_prompt
from llm.deepseek_client import call_deepseek
from crewai.tools import tool

@tool
def generate_interview_questions(cv_text: str, job_desc: str = "") -> str:
    """
    Generates a interview questions for a candidate based on provided data.
    """
    prompt = get_interview_prompt(cv_text, job_desc)
    return call_deepseek(prompt, max_tokens=300)