import datetime
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, func
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate

def get_student_by_id(db: Session, student_id: int) -> Optional[Student]:
    """Retrieve a student record by unique ID."""
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    """Retrieve a student record by email address (for uniqueness check)."""
    return db.query(Student).filter(Student.email == email).first()

def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    course: Optional[str] = None,
    search: Optional[str] = None,
    born_after: Optional[datetime.date] = None,
    born_before: Optional[datetime.date] = None,
    enrolled_after: Optional[datetime.date] = None,
    enrolled_before: Optional[datetime.date] = None,
    sort_by: str = "id",
    order: str = "asc"
) -> Tuple[List[Student], int]:
    """
    List and filter students with pagination and sorting.
    Returns (students_list, total_count).
    """
    query = db.query(Student)

    # Filtering by Course
    if course:
        query = query.filter(Student.course.ilike(f"%{course.strip()}%"))

    # Search by Name or Email
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Student.name.ilike(search_pattern),
                Student.email.ilike(search_pattern),
                Student.phone.ilike(search_pattern)
            )
        )

    # Date of birth filters
    if born_after:
        query = query.filter(Student.date_of_birth >= born_after)
    if born_before:
        query = query.filter(Student.date_of_birth <= born_before)

    # Enrollment date filters
    if enrolled_after:
        query = query.filter(Student.enrollment_date >= enrolled_after)
    if enrolled_before:
        query = query.filter(Student.enrollment_date <= enrolled_before)

    total = query.count()

    # Dynamic sorting
    sort_column = getattr(Student, sort_by, Student.id)
    if order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    students = query.offset(skip).limit(limit).all()
    return students, total

def create_student(db: Session, student_data: StudentCreate) -> Student:
    """Create and persist a new student record."""
    db_student = Student(
        name=student_data.name.strip(),
        date_of_birth=student_data.date_of_birth,
        email=student_data.email.lower().strip(),
        phone=student_data.phone.strip(),
        course=student_data.course.strip() if student_data.course else None,
        address=student_data.address.strip() if student_data.address else None,
        enrollment_date=student_data.enrollment_date or datetime.date.today()
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_update: StudentUpdate) -> Optional[Student]:
    """Update fields on an existing student (PUT or PATCH)."""
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None

    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "email" and value is not None:
            setattr(db_student, field, value.lower().strip())
        elif isinstance(value, str):
            setattr(db_student, field, value.strip())
        else:
            setattr(db_student, field, value)

    db_student.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int) -> bool:
    """Remove a student record from the database."""
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True

def get_distinct_courses(db: Session) -> List[str]:
    """Retrieve list of distinct courses currently enrolled in."""
    courses = db.query(Student.course).filter(Student.course.isnot(None)).distinct().all()
    return sorted([c[0] for c in courses if c[0]])

def get_student_statistics(db: Session) -> Dict[str, Any]:
    """Retrieve statistical aggregations for analytics / AI grounding."""
    total = db.query(func.count(Student.id)).scalar() or 0
    courses_query = db.query(Student.course, func.count(Student.id)).group_by(Student.course).all()
    courses_breakdown = {c[0] or "Unassigned": c[1] for c in courses_query}
    
    earliest = db.query(func.min(Student.enrollment_date)).scalar()
    latest = db.query(func.max(Student.enrollment_date)).scalar()

    return {
        "total_students": total,
        "courses_breakdown": courses_breakdown,
        "earliest_enrollment": earliest,
        "latest_enrollment": latest
    }
