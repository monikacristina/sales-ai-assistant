from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app.models import QuestionRequest
from app.assistant import process_question

app = FastAPI(
    title="AI Sales Analytics Assistant",
    description="An AI-powered assistant for sales data analysis",
    version="1.0.0"
)

from pathlib import Path

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app")
def serve_frontend():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Sales Analytics Assistant!"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        result = process_question(request.question)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise

    except Exception as error:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Unable to process your question."
        )
