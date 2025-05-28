from crewai import Crew


from agents.om_agent.agent import OfficeManagerAgent
from agents.km_agent.agent import get_knowledge_agent
from agents.recruitment_agent.agent import get_recruitment_agent

# Instantiate agents
knowledge_agent = get_knowledge_agent()
recruitment_agent = get_recruitment_agent()
office_manager_agent = OfficeManagerAgent  

# Define the Crew
business_crew = Crew(
    agents=[
        office_manager_agent,
        knowledge_agent,
        recruitment_agent
    ],
    verbose=True,
    memory=True  
)

# Function to get the crew 
def get_crew():
    return business_crew
