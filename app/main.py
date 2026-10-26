import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import students, ai
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create SQLite database tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="""
## Student Management System CRUD Backend (+ Ollama AI Extension)
Built with **FastAPI**, **SQLite**, and **Ollama (llama3.2:1b)** for the **EWB Edu Tech Pvt. Ltd.** Python Backend Internship Assignment.

### Features
* **Create (POST /students)**: Enroll new student profiles with duplicate email checks.
* **Read (GET /students & GET /students/{id})**: List, paginate, sort, and filter students by course, name, email, or date of birth.
* **Update (PUT / PATCH /students/{id})**: Modify student details with full or partial updates.
* **Delete (DELETE /students/{id})**: Remove student records from persistent storage.
* **Local AI Assistant (POST /ai/ask)**: Natural language queries grounded in student records via local Ollama `llama3.2:1b` (with safe offline analyzer fallback).
* **Interactive UI**: Visit `/` to test the full CRUD system and AI assistant directly in your browser.
    """,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(students.router)
app.include_router(ai.router)

# Mount Static Files & Serve UI Dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def serve_ui():
    """Serves the interactive single-page application dashboard."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": f"Welcome to {settings.APP_NAME}. View docs at /docs"}

@app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }
