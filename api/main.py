from fastapi import FastAPI
from api.routes import classify
from api.routes import recruiter_input_routes
from api.routes.knowledge_management_routes import router as knowledge_router
from api.routes.report_generation_route import router as report_generation
from databse.database import Base, engine
from api.routes import authentification  
from api.routes import attestations
from databse.database import init_db

init_db()

app = FastAPI()
app.include_router(classify.router)
app.include_router(knowledge_router)
app.include_router(recruiter_input_routes.router)
app.include_router(report_generation)
app.include_router(authentification.router, prefix="/auth", tags=["auth"])
app.include_router(attestations.router)