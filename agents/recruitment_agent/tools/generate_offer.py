# recruitment_agent/tools/generate_offer.py
from llm.prompts.recruitment_prompts import get_offer_prompt
from llm.deepseek_client import call_deepseek
from crewai.tools import tool

@tool
def generate_offer(hr_input: str) -> str:
    """
    Generates an offer  for a job based on provided data.
    """
    prompt = get_offer_prompt(hr_input)
    return call_deepseek(prompt, max_tokens=700)
