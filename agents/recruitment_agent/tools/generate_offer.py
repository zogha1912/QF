# recruitment_agent/tools/generate_offer.py
from llm.prompts.recruitment_prompts import get_offer_prompt
from llm.deepseek_client import call_deepseek

def generate_offer(hr_input: str) -> str:
    prompt = get_offer_prompt(hr_input)
    return call_deepseek(prompt, max_tokens=700)
