from crewai.tools import BaseTool
from llm.prompts.km_enrichment_prompt import get_km_enrichment_prompt
from llm.deepseek_client import call_deepseek

class EnrichJobDataWithKM(BaseTool):
    name : str = "enrich_job_data"
    description : str = "Uses knowledge base to enrich extracted job info"

    def _run(self, job_json: dict):
        prompt = get_km_enrichment_prompt(job_json)
        return call_deepseek(prompt, max_tokens=300)
