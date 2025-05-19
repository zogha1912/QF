def get_km_enrichment_prompt(job_data: dict) -> str:
    return f"""
You are a knowledge base assistant.

Given this structured job profile:
{job_data}

Suggest improvements, detect missing fields, and enrich the profile with helpful context or suggestions.
"""
