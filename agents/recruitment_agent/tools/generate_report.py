# agents/recruitment/tools/generate_report.py
from llm.prompts.recruitment_prompts import get_report_prompt
from llm.deepseek_client import call_deepseek

def generate_candidate_report(cv_text: str, position: str) -> str:
    prompt = get_report_prompt(cv_text, position)
    return call_deepseek(prompt, max_tokens=600)