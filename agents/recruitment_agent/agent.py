from crewai import Agent
from .tools.classify_candidate import classify_candidate
from .tools.generate_report import generate_candidate_report
from .tools.generate_offer import generate_offer
from .tools.generate_questions import generate_interview_questions

from .tools.classify_input import ClassifyRecruiterInput
from .tools.generate_clarifications import GenerateClarificationQuestions
from .tools.extract_job_details import ExtractJobDetails
from agents.km_agent.enrich_job_data import EnrichJobDataWithKM

def get_recruitment_agent():
    agent = Agent(
        role="Recruitment Agent",
        goal="Streamline and automate the recruitment process",
        backstory="An experienced recruiter...",
        tools=[
            ClassifyRecruiterInput(),
            GenerateClarificationQuestions(),
            ExtractJobDetails(),
            EnrichJobDataWithKM(),
            classify_candidate,
            generate_candidate_report,
            generate_offer,
            generate_interview_questions
        ],
        verbose=True,
        allow_delegation=False
    )
    return agent
