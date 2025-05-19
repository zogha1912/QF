from crewai.tools import BaseTool
from llm.prompts.classification_prompt import get_classification_prompt
from llm.deepseek_client import call_deepseek

class ClassifyRecruiterInput(BaseTool):
    name: str = "classify_recruiter_input"
    description : str = "Classifies recruiter input as VAGUE or DETAILED"

    def _run(self, text: str):
        prompt = get_classification_prompt(text)
        result = call_deepseek(prompt, max_tokens=20)
        return result.strip().upper()
