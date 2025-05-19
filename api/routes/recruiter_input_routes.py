from fastapi import APIRouter
from pydantic import BaseModel

from agents.recruitment_agent.tools.classify_input import ClassifyRecruiterInput
from agents.recruitment_agent.tools.generate_clarifications import GenerateClarificationQuestions
from agents.recruitment_agent.tools.extract_job_details import ExtractJobDetails
from agents.km_agent.enrich_job_data import EnrichJobDataWithKM
from agents.recruitment_agent.tools.detect_internal_profile import DetectInternalProfile
from agents.km_agent.embed_store import store_embedding, load_faiss_index, save_faiss_index
from agents.km_agent.search import search_knowledge_base, generate_answer
from agents.km_agent.models.schemas import QueryRequest


router = APIRouter()
faiss_index, doc_store = load_faiss_index()
class RecruiterInput(BaseModel):
    text: str

@router.post("/recruiter/process")
def process_recruiter_input(data: RecruiterInput):
    print(f"Received input: {data.text}")
    input_text = data.text

    # Step 1: Classify input
    classifier = ClassifyRecruiterInput()
    input_type = classifier._run(input_text)

    # Step 2: Check if it's internal
    detector = DetectInternalProfile()
    is_internal = detector._run(input_text)

    if is_internal == "YES":
        # Enrich using KM Agent
        context_docs = search_knowledge_base(input_text, faiss_index, doc_store)
        enriched_answer = generate_answer(input_text, context_docs)

        return {
            "input_type": "INTERNAL",
            "enriched_from_km": enriched_answer,
            "sources": context_docs
        }

    # Step 3: Handle vague input
    if input_type == "VAGUE":
        clarification_tool = GenerateClarificationQuestions()
        questions = clarification_tool._run(input_text)
        return {
            "input_type": "VAGUE",
            "clarification_questions": questions
        }

    # Step 4: Handle detailed input
    elif input_type == "DETAILED":
        extractor = ExtractJobDetails()
        job_data = extractor._run(input_text)

        enricher = EnrichJobDataWithKM()
        enriched = enricher._run(job_data)

        return {
            "input_type": "DETAILED",
            "job_data": job_data,
            "enriched_data": enriched
        }

    return {"error": "Unable to classify input"}
