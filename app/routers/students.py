import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import StudentCreate, StudentUpdate, StudentResponse, StudentStatsResponse
from app import crud

router = APIRouter(
    prefix="/students",
    tags=["Students CRUD"]
)

@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
    description="Add a new student record to the database. Student email must be unique."
)
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db)
):
    existing = crud.get_student_by_email(db, student_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A student with email '{student_in.email}' already exists."
        )
    return crud.create_student(db, student_in)

@router.get(
    "",
    response_model=List[StudentResponse],
    summary="List and filter students",
    description="Retrieve all students with optional search, course filter, date filters, sorting and pagination."
)
def list_students(
    response: Response,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(50, ge=1, le=500, description="Number of records to return"),
    course: Optional[str] = Query(None, description="Filter by course (partial or exact)"),
    search: Optional[str] = Query(None, description="Search by name, email, or phone"),
    born_after: Optional[datetime.date] = Query(None, description="Filter students born on or after this date"),
    born_before: Optional[datetime.date] = Query(None, description="Filter students born on or before this date"),
    enrolled_after: Optional[datetime.date] = Query(None, description="Filter students enrolled on or after this date"),
    enrolled_before: Optional[datetime.date] = Query(None, description="Filter students enrolled on or before this date"),
    sort_by: str = Query("id", pattern="^(id|name|date_of_birth|enrollment_date|course)$", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sorting direction ('asc' or 'desc')")
):
    students, total = crud.get_students(
        db=db,
        skip=skip,
        limit=limit,
        course=course,
        search=search,
        born_after=born_after,
        born_before=born_before,
        enrolled_after=enrolled_after,
        enrolled_before=enrolled_before,
        sort_by=sort_by,
        order=order
    )
    # Include total count in standard HTTP header for pagination awareness
    response.headers["X-Total-Count"] = str(total)
    return students

@router.get(
    "/stats/summary",
    response_model=StudentStatsResponse,
    summary="Get summary statistics",
    description="Get total student counts, course breakdowns, and enrollment boundaries."
)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_student_statistics(db)

@router.get(
    "/courses/list",
    response_model=List[str],
    summary="Get list of existing courses",
    description="Retrieve distinct enrolled course titles."
)
def get_courses(db: Session = Depends(get_db)):
    return crud.get_distinct_courses(db)

@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="View a student by ID",
    description="Retrieve a single student profile by unique student ID."
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    return student

@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student (Full/Partial)",
    description="Modify an existing student's details by ID."
)
def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db)
):
    # Check if student exists
    db_student = crud.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )

    # Check for email conflicts
    if student_in.email and student_in.email.lower() != db_student.email.lower():
        existing = crud.get_student_by_email(db, student_in.email)
        if existing and existing.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{student_in.email}' is already in use by another student."
            )

    updated = crud.update_student(db, student_id, student_in)
    return updated

@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Patch a student's details",
    description="Partially modify specific fields of an existing student record."
)
def patch_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db)
):
    return update_student(student_id=student_id, student_in=student_in, db=db)

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a student",
    description="Remove a student record from the database by ID."
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    return {
        "success": True,
        "message": f"Student with ID {student_id} has been permanently deleted.",
        "student_id": student_id
    }
