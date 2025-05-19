from crewai.tools import BaseTool
from llm.prompts.extraction_prompt import get_extraction_prompt
from llm.deepseek_client import call_deepseek
import json

class ExtractJobDetails(BaseTool):
    name : str = "extract_job_details"
    description : str = "Extracts structured job info from detailed recruiter input"

    def _run(self, text: str):
        prompt = get_extraction_prompt(text)
        response = call_deepseek(prompt, max_tokens=300)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON", "raw": response}
