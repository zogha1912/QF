
## models/schemas.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
