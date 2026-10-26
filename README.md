# Students Database CRUD Application (+ Ollama AI Extension)
### Python Backend Development Internship Assignment | EWB Edu Tech Pvt. Ltd.

A robust, production-grade Python backend application built with **FastAPI** and **SQLite** for managing student records via full **CRUD** (Create, Read, Update, Delete) operations, paired with an intelligent **Local AI Assistant powered by Ollama (`llama3.2:1b`)** and an interactive single-page web dashboard.

---

## 🌟 Features & Highlights

1. **Full CRUD Operations**:
   - **Create**: Add new student records with email uniqueness checks and strict Pydantic v2 schema validations.
   - **Read**: Fetch paginated records, sort dynamically, and filter by course, name, email, phone, or date of birth ranges.
   - **Update**: Update existing records via full replace (`PUT`) or partial modification (`PATCH`).
   - **Delete**: Safely delete student records with relational integrity.
2. **Persistent Storage with SQLite & SQLAlchemy**:
   - SQLite persistent database with SQLAlchemy ORM models, connection pooling, and automatic migration on startup.
3. **Optional Bonus: Local AI Assistant (Ollama `llama3.2:1b`)**:
   - Natural language queries such as *"How many students are there?"*, *"List students born after 2005"*, or *"How many students in Computer Science?"*.
   - **Strict Security Grounding**: The LLM is **never** permitted to generate or execute arbitrary SQL. All context is fetched safely in Python code and passed to the model as verified ground-truth data.
   - **Graceful Offline Fallback**: If Ollama is offline or not installed, a built-in deterministic analyzer answers queries accurately directly from database records without crashing.
4. **Interactive Single-Page Web Dashboard**:
   - Served directly from FastAPI at `http://127.0.0.1:8000/`.
   - Real-time table view, modal forms for adding/editing students, search, filtering, and a live AI assistant prompt box.
5. **Interactive OpenAPI / Swagger Documentation**:
   - Fully documented Swagger UI (`/docs`) and ReDoc (`/redoc`).
6. **100% Automated Pytest Coverage**:
   - Comprehensive test suite covering every CRUD endpoint, edge cases, error codes (404, 409, 422), and AI assistant behavior.

---

## 📂 Project Structure

```text
d:\intern_project_ewb\
├── app/
│   ├── __init__.py
│   ├── config.py              # Application settings & environment variables
│   ├── database.py            # SQLite connection engine & SessionLocal dependency
│   ├── models.py              # SQLAlchemy Student ORM model
│   ├── schemas.py             # Pydantic v2 validation schemas
│   ├── crud.py                # Repository functions for database operations
│   ├── ai_service.py          # Ollama LLM integration & safe grounding engine
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── students.py        # Student CRUD API routes
│   │   └── ai.py              # Ollama AI Assistant endpoints
│   ├── static/                # Single-page web dashboard
│   │   ├── index.html         # Responsive HTML5 interface
│   │   ├── style.css          # Modern UI stylesheet
│   │   └── app.js             # Client-side API interactions
│   └── main.py                # FastAPI app initialization, CORS, and routing
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Isolated in-memory SQLite fixtures for Pytest
│   ├── test_students_crud.py  # Unit & integration tests for all CRUD endpoints
│   └── test_ai_service.py     # Tests for AI querying & context grounding
├── seed_data.py               # Pre-populates database with 10 dummy student records
├── run.py                     # Convenience script to start Uvicorn server
├── requirements.txt           # Project dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Standard Python/SQLite gitignore
└── README.md                  # Comprehensive assignment documentation
```

---

## 📋 Student Record Schema

| Field Name | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Auto (PK) | Unique auto-incrementing student identifier |
| `name` | String | **Yes** | Student's full name (min 2 characters) |
| `date_of_birth` | Date | **Yes** | Birth date in `YYYY-MM-DD` format |
| `email` | String | **Yes** | Valid, unique student email address |
| `phone` | String | **Yes** | Contact telephone / mobile number |
| `course` | String | *Optional* | Enrolled course or department (e.g. `Computer Science`) |
| `address` | String | *Optional* | Residential / campus address |
| `enrollment_date` | Date | *Optional* | Date enrolled (defaults to current date) |
| `created_at` | DateTime | Auto | UTC timestamp of record creation |
| `updated_at` | DateTime | Auto | UTC timestamp of last update |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Pip package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed Sample Dummy Data
Pre-load 10 realistic dummy student records across multiple courses:
```bash
python seed_data.py
```

### 4. Start the Application Server
Run using the convenience runner:
```bash
python run.py
```
Or directly using Uvicorn:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Access the Application
- **Interactive UI Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Interactive API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints Reference

### Students CRUD Endpoints (`/students`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/students` | Create a new student record (Validates unique email) |
| `GET` | `/students` | List all students with query filters, sorting, and pagination |
| `GET` | `/students/{student_id}` | Retrieve a student profile by ID (Returns 404 if not found) |
| `PUT` | `/students/{student_id}` | Full update of student details |
| `PATCH` | `/students/{student_id}` | Partial update of specific student fields |
| `DELETE` | `/students/{student_id}` | Remove a student record from the database |
| `GET` | `/students/courses/list` | Retrieve list of distinct active courses |
| `GET` | `/students/stats/summary` | Summary metrics (totals, course breakdowns, date boundaries) |

### AI Assistant Endpoints (`/ai`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/ai/ask` | Submit natural-language question grounded in database records |
| `GET` | `/ai/status` | Check local Ollama health status and configured model |

---

## 💡 Example cURL Requests

### 1. Create a Student
```bash
curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maya Patel",
    "date_of_birth": "2005-09-12",
    "email": "maya.patel@example.com",
    "phone": "+91-9876501234",
    "course": "Computer Science",
    "address": "404 Cyber City, Hyderabad",
    "enrollment_date": "2023-08-01"
  }'
```

### 2. List & Filter Students
```bash
# Filter by Course
curl -X GET "http://127.0.0.1:8000/students?course=Computer%20Science"

# Filter students born after 2005
curl -X GET "http://127.0.0.1:8000/students?born_after=2005-01-01"

# Search keyword across name, email, or phone
curl -X GET "http://127.0.0.1:8000/students?search=Sharma"

# Dynamic sorting (name ascending) with pagination
curl -X GET "http://127.0.0.1:8000/students?sort_by=name&order=asc&skip=0&limit=10"
```

### 3. Get Student by ID
```bash
curl -X GET "http://127.0.0.1:8000/students/1"
```

### 4. Update Student Details
```bash
# Partial update using PATCH
curl -X PATCH "http://127.0.0.1:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{
    "course": "Artificial Intelligence",
    "phone": "+91-9988776655"
  }'
```

### 5. Delete a Student
```bash
curl -X DELETE "http://127.0.0.1:8000/students/1"
```

### 6. Query the AI Assistant
```bash
curl -X POST "http://127.0.0.1:8000/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many students are there in Computer Science?"
  }'
```

---

## 🤖 Bonus: Local AI with Ollama

### Model Configuration
- **Model**: `llama3.2:1b` (default, lightweight and fast)
- **Base URL**: `http://localhost:11434` (configurable via `OLLAMA_BASE_URL`)

### Running Ollama Locally
If you want to run the live local LLM:
1. Download and install Ollama from [https://ollama.com](https://ollama.com).
2. Pull and start the recommended model:
   ```bash
   ollama run llama3.2:1b
   ```
3. The API will automatically detect the live instance and generate responses grounded on SQLite records.

### Grounding & Security Safeguards
Per assignment guidelines:
- **No Unrestricted SQL**: The model is **never** given access to run raw SQL queries.
- **Backend Context Fetching**: Context records and aggregate counts are gathered safely inside Python via SQLAlchemy ORM.
- **Zero Hallucination Guardrail**: The system prompt instructs the model to rely solely on the provided verified records.
- **Privacy & Safety**: All records are dummy synthetic profiles.

---

## 🧪 Automated Testing

The project includes 14 automated tests covering all CRUD operations, edge cases, error codes, and the AI assistant.

Run the test suite with:
```bash
python -m pytest -v
```

**Test Results**:
```text
tests/test_ai_service.py::test_ai_status_endpoint PASSED                 [  7%]
tests/test_ai_service.py::test_ai_ask_how_many_students PASSED           [ 14%]
tests/test_ai_service.py::test_ai_ask_born_after_filter PASSED           [ 21%]
tests/test_ai_service.py::test_ai_ask_course_breakdown PASSED            [ 28%]
tests/test_students_crud.py::test_create_student_success PASSED          [ 35%]
tests/test_students_crud.py::test_create_student_duplicate_email PASSED  [ 42%]
tests/test_students_crud.py::test_create_student_validation_errors PASSED [ 50%]
tests/test_students_crud.py::test_get_student_by_id PASSED               [ 57%]
tests/test_students_crud.py::test_get_student_not_found PASSED           [ 64%]
tests/test_students_crud.py::test_list_and_filter_students PASSED        [ 71%]
tests/test_students_crud.py::test_update_student_put PASSED              [ 78%]
tests/test_students_crud.py::test_patch_student_partial PASSED           [ 85%]
tests/test_students_crud.py::test_delete_student PASSED                  [ 92%]
tests/test_students_crud.py::test_courses_and_stats PASSED               [100%]

======================= 14 passed in 18.98s =======================
```

---

## 📄 License & Attribution
Prepared as an Individual Backend Development Assignment for **EWB Edu Tech Pvt. Ltd.**
Designed & Developed following industry best practices with FastAPI, SQLAlchemy, SQLite, Pydantic v2, and Ollama.
