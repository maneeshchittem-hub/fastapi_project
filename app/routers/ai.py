from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AIQueryRequest, AIQueryResponse
from app.config import settings
from app import ai_service

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant (Ollama)"]
)

@router.post(
    "/ask",
    response_model=AIQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question about students in natural language",
    description="Processes natural-language queries (e.g. 'How many students are enrolled in Computer Science?') by safely grounding them against the SQLite database records and querying Ollama (or offline analyzer fallback)."
)
def ask_ai_question(
    query_in: AIQueryRequest,
    db: Session = Depends(get_db)
):
    result = ai_service.query_student_assistant(question=query_in.question, db=db)
    return result

@router.get(
    "/status",
    summary="Check Ollama status",
    description="Inspect whether the local Ollama daemon is reachable and which model is configured."
)
def get_ai_status():
    online = ai_service.is_ollama_online()
    return {
        "ollama_online": online,
        "configured_model": settings.OLLAMA_MODEL,
        "ollama_url": settings.OLLAMA_BASE_URL,
        "instructions": (
            "Local Ollama is connected!" if online else
            f"Ollama is offline. To enable live LLM inference: install Ollama from https://ollama.com and run 'ollama run {settings.OLLAMA_MODEL}'."
        )
    }
