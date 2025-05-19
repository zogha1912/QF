# agents/recruitment_agent/tools/detect_internal_profile.py
from crewai.tools import BaseTool
from llm.prompts.detect_internal_prompt import get_internal_detection_prompt
from llm.deepseek_client import call_deepseek
from sentence_transformers import SentenceTransformer
import numpy as np
from agents.km_agent.embed_store import doc_store

model = SentenceTransformer("all-MiniLM-L6-v2")

class DetectInternalProfile(BaseTool):
    name : str = "DetectInternalProfile"
    description : str = "Checks if the recruiter's message refers to someone in the knowledge base."

    def _run(self, text: str):
        # Step 1: Check via LLM
        prompt = get_internal_detection_prompt(text)
        result = call_deepseek(prompt, max_tokens=10).strip().upper()
        print(f"[DetectInternalProfile] LLM result: '{result}'")

        if result == "YES":
            return "YES"

        # Step 2: Fallback to semantic similarity
        query_vec = model.encode(text)

        for doc in doc_store:
            doc_vec = doc["embedding"]
            sim = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec))
            print(f"[DetectInternalProfile] Similarity with {doc['metadata']['filename']}: {sim:.2f}")
            if sim > 0.8:
                return "YES"

        return "NO"
