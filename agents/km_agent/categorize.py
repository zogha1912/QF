import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_URL")

def categorize_document(content):
    prompt = f"""
    You are a highly accurate document classification assistant.

    Your tasks are:

    1. **Categorize** the document based on its purpose and structure, not just its content.
    - Choose only one category from: HR, Legal, Finance, Technical, Sales, Administrative, Research, Operations, Other.

    2. **Determine the document type**, e.g., Resume, Contract, Invoice, Report, Email, Presentation, etc.
    - If the document is a **Resume or CV**, always set the **Category to HR**, even if the person has technical or financial skills.

    3. **Provide a short, concise summary** of the document's content.

    Document:
    {content[:500]}

    Return the result in the following format:
    Category: <category>
    Type: <document_type>
    Summary: <summary>
    
    """

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    result = response.json()
    output = result["choices"][0]["message"]["content"]
    print("LLM raw output:\n", output)  # Pour debug

    try:
        lines = output.splitlines()
        category = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("category:")), "Other")
        summary = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("summary:")), "No summary")

        # Mappage pour le type de document
        if category.lower() == "hr":
            doc_type = "candidate"
        elif category.lower() in ["technical", "finance", "operations"]:
            doc_type = "client"
        else:
            doc_type = "other"

        return doc_type, category, summary

    except Exception as e:
        print("Parsing failed:", e)
        return "other", "Other", "Failed to parse summary"
