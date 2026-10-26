import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    phone = Column(String(30), nullable=False)
    course = Column(String(100), nullable=True, index=True)
    address = Column(String(255), nullable=True)
    enrollment_date = Column(Date, nullable=True, default=datetime.date.today)
    
    created_at = Column(
        DateTime, 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        nullable=False
    )
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc), 
        nullable=False
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, name='{self.name}', course='{self.course}')>"
