# agents/recruitment/tools/generate_report.py
from llm.prompts.recruitment_prompts import get_report_prompt
from llm.deepseek_client import call_deepseek
from crewai.tools import tool

@tool
def generate_candidate_report(cv_text: str, position: str) -> str:
    """
    Generates a report for a candidate based on provided data.
    """
    prompt = get_report_prompt(cv_text, position)
    return call_deepseek(prompt, max_tokens=600)