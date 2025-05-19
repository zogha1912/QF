# agent.py
from crewai import Agent
from .tools import retrieve_answer

def get_knowledge_agent():
    return Agent(
        role="Knowledge Base Agent",
        goal="Assist other agents by retrieving accurate information from internal documentation.",
        backstory=(
            "This agent is trained on the organization's internal documents and excels at answering "
            "questions using only verified sources from the knowledge base."
        ),
        tools=[retrieve_answer],
        verbose=True
    )
