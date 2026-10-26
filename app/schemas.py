import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the student", examples=["Aarav Sharma"])
    date_of_birth: datetime.date = Field(..., description="Date of birth (YYYY-MM-DD)", examples=["2004-05-15"])
    email: EmailStr = Field(..., description="Valid student email address", examples=["aarav.sharma@example.com"])
    phone: str = Field(..., min_length=7, max_length=25, description="Contact phone number", examples=["+91-9876543210"])
    course: Optional[str] = Field(None, max_length=100, description="Enrolled program or course", examples=["Computer Science"])
    address: Optional[str] = Field(None, max_length=255, description="Residential or campus address", examples=["42 Silicon Valley Road, Bangalore"])
    enrollment_date: Optional[datetime.date] = Field(default_factory=datetime.date.today, description="Date enrolled (YYYY-MM-DD)")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    date_of_birth: Optional[datetime.date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=25)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    enrollment_date: Optional[datetime.date] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedStudentResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    students: List[StudentResponse]

class StudentStatsResponse(BaseModel):
    total_students: int
    courses_breakdown: Dict[str, int]
    earliest_enrollment: Optional[datetime.date] = None
    latest_enrollment: Optional[datetime.date] = None

class AIQueryRequest(BaseModel):
    question: str = Field(..., min_length=2, description="Natural language question about student records", examples=["How many students are enrolled in Computer Science?"])

class AIQueryResponse(BaseModel):
    question: str
    answer: str
    model: str
    grounded_records_count: int
    ollama_available: bool
    context_summary: Optional[str] = None
