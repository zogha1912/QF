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
from agents.recruitment_agent.tools.generate_offer import generate_offer

from uuid import uuid4

clarification_store = {} 

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
        
        # Generate a unique ID and store the original input and questions
        clarification_id = str(uuid4())
        clarification_store[clarification_id] = {
            "original_input": input_text,
            "questions": questions
        }
        return {
            "input_type": "VAGUE",
            "clarification_id": clarification_id,
            "clarification_questions": questions,
            
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

class ClarificationResponse(BaseModel):
    clarification_id: str
    answers: str  # Free-form answer from recruiter (single field or full paragraph)

@router.post("/recruiter/clarification/respond")
def handle_clarification_response(data: ClarificationResponse):
    entry = clarification_store.get(data.clarification_id)
    if not entry:
        return {"error": "Invalid or expired clarification ID."}

    original_input = entry["original_input"]

    # Merge original vague message with the new recruiter input
    combined = f"""
        The recruiter originally said:
        \"\"\"{original_input}\"\"\"

        They clarified with:
        \"\"\"{data.answers}\"\"\"
            """.strip()

    # Run same flow
    classifier = ClassifyRecruiterInput()
    input_type = classifier._run(combined)

    if input_type == "DETAILED":
        extractor = ExtractJobDetails()
        job_data = extractor._run(combined)

        enricher = EnrichJobDataWithKM()
        enriched = enricher._run(job_data)
        
        job_offer = generate_offer(combined)

        return {
            "input_type": "DETAILED_AFTER_CLARIFICATION",
            "job_data": job_data,
            "enriched_data": enriched,
            "job_offer": job_offer
        }

    return {"message": "Clarification insufficient.", "input_type": input_type}
