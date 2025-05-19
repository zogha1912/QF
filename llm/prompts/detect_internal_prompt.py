from agents.km_agent.embed_store import doc_store

def get_internal_detection_prompt(text: str) -> str:
    # Get names from the knowledge base
    known_people = "\n".join([
        f"- {doc['metadata'].get('name', doc['metadata'].get('filename', 'Unknown'))}"
        for doc in doc_store
    ])

    return f"""
You are an assistant that helps detect internal references in recruiter messages.

Here is a list of internal team members or employees:
{known_people}

Now, determine if the following recruiter input refers to one of the above internal profiles:

\"\"\"{text}\"\"\"

Answer YES if the message clearly refers to an internal team member (by name or role), otherwise answer NO.
"""
