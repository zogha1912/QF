from fastapi import FastAPI
from api.routes import classify
from api.routes import recruiter_input_routes
from api.routes.knowledge_management_routes import router as knowledge_router


app = FastAPI()
app.include_router(classify.router)
app.include_router(knowledge_router)
app.include_router(recruiter_input_routes.router)