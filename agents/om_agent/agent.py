from crewai import Agent


OfficeManagerAgent = Agent(
    role="Office Manager Assistant",
    goal="Support with employee document generation and requests",
    backstory=(
        "You assist the office manager by preparing administrative documents like employment attestations, "
        "tracking request status, and enforcing data access control."
    ),
    tools=[],  
    allow_delegation=True
)
