from llm.prompts.recruitment_prompts import get_classification_prompt
from llm.deepseek_client import call_deepseek
from crewai.tools import tool

@tool
def classify_candidate(cv_text: str, job_desc: str = "") -> str:
    """
    Classify a candidate's CV text against a job description.
    Returns a classification string based on the prompt response.
    """
    prompt = get_classification_prompt(cv_text, job_desc)
    return call_deepseek(prompt, max_tokens=300)
