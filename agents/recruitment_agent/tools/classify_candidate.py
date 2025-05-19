# agents/recruitment/tools/classify_candidate.py
from llm.prompts.recruitment_prompts import get_classification_prompt
from llm.deepseek_client import call_deepseek

def classify_candidate(cv_text: str, job_desc: str = "") -> str:
    prompt = get_classification_prompt(cv_text, job_desc)
    return call_deepseek(prompt, max_tokens=300)
