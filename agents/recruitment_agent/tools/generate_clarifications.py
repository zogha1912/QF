from crewai.tools import BaseTool
from llm.prompts.clarification_prompt import get_clarification_prompt
from llm.deepseek_client import call_deepseek

class GenerateClarificationQuestions(BaseTool):
    name : str = "generate_clarification_questions"
    description : str = "Generates follow-up questions for vague recruiter inputs"

    def _run(self, text: str):
        prompt = get_clarification_prompt(text)
        return call_deepseek(prompt, max_tokens=150)
