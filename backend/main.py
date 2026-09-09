from fastapi import FastAPI

from backend.routes import assessment
from backend.routes import learning


app = FastAPI(
    title="EduPilot API",
    description="Agentic AI Personalized Learning System",
    version="1.0.0"
)


app.include_router(
    assessment.router
)

app.include_router(
    learning.router
)


@app.get("/")
def root():

    return {
        "message": "EduPilot API is running"
    }