from fastapi import FastAPI

from backend.routes.assessment import router as assessment_router
from backend.routes.learning import router as learning_router



app = FastAPI(
    title="EduPilot API"
)


app.include_router(
    assessment_router
)

app.include_router(
    learning_router
)


@app.get("/")
def root():

    return {
        "message": "EduPilot API is running"
    }