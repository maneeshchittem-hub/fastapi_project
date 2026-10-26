"""Convenience runner script for the Student Management System."""
import uvicorn

if __name__ == "__main__":
    print("=" * 65)
    print("🚀 Starting Students Database CRUD Application + AI Assistant")
    print("📍 Interactive Dashboard: http://127.0.0.1:8000")
    print("📚 Swagger API Docs:      http://127.0.0.1:8000/docs")
    print("📖 ReDoc Documentation:   http://127.0.0.1:8000/redoc")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
