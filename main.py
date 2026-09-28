from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path


app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="Google Gemini powered educational assistant",
    version="1.0.0"
)


# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QuizRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    difficulty: str = Field(
        default="medium"
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class LearningRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = Field(
        default="beginner"
    )

    weeks: int = Field(
        default=4,
        ge=1,
        le=12
    )


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie",
        "version": "1.0.0"
    }


# ---------------------------------------------------------
# Question & Answer
# ---------------------------------------------------------

@app.post("/qa")
async def qa(request: TextRequest):

    answer = answer_question(
        request.text
    )

    return {
        "success": True,
        "question": request.text,
        "answer": answer
    }


# ---------------------------------------------------------
# Concept Explanation
# ---------------------------------------------------------

@app.post("/explain")
async def explain(request: TextRequest):

    explanation = explain_concept(
        request.text
    )

    return {
        "success": True,
        "topic": request.text,
        "explanation": explanation
    }


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(request: QuizRequest):

    result = generate_quiz(
        topic=request.topic,
        difficulty=request.difficulty,
        count=request.count
    )

    return {
        "success": True,
        "topic": request.topic,
        "difficulty": request.difficulty,
        "count": result.get(
            "count",
            0
        ),
        "quiz": result.get(
            "quiz",
            {
                "questions": []
            }
        ),
        "error": result.get(
            "error"
        )
    }


# ---------------------------------------------------------
# Summarization
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):

    summary = summarize_text(
        request.text
    )

    return {
        "success": True,
        "summary": summary
    }


# ---------------------------------------------------------
# Learning Path
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningRequest
):

    recommendations = generate_learning_path(
        topic=request.topic,
        level=request.level,
        weeks=request.weeks
    )

    return {
        "success": True,
        "recommendations": recommendations
    }


# ---------------------------------------------------------
# Run Directly With Python
# ---------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )