"""Seed script to populate the SQLite database with realistic dummy student records."""
import datetime
from app.database import SessionLocal, Base, engine
from app.models import Student

DUMMY_STUDENTS = [
    {
        "name": "Aarav Sharma",
        "date_of_birth": datetime.date(2004, 5, 14),
        "email": "aarav.sharma@example.com",
        "phone": "+91-98765-43210",
        "course": "Computer Science",
        "address": "42 Tech Boulevard, Bangalore, Karnataka",
        "enrollment_date": datetime.date(2022, 8, 1)
    },
    {
        "name": "Diya Patel",
        "date_of_birth": datetime.date(2005, 11, 23),
        "email": "diya.patel@example.com",
        "phone": "+91-98234-56789",
        "course": "Data Science",
        "address": "15 Green Valley, Ahmedabad, Gujarat",
        "enrollment_date": datetime.date(2023, 7, 15)
    },
    {
        "name": "Rohan Verma",
        "date_of_birth": datetime.date(2006, 2, 10),
        "email": "rohan.verma@example.com",
        "phone": "+91-97123-45678",
        "course": "Computer Science",
        "address": "88 Civil Lines, Delhi",
        "enrollment_date": datetime.date(2024, 8, 10)
    },
    {
        "name": "Ananya Iyer",
        "date_of_birth": datetime.date(2003, 9, 18),
        "email": "ananya.iyer@example.com",
        "phone": "+91-99887-76655",
        "course": "Mechanical Engineering",
        "address": "204 Temple View, Chennai, Tamil Nadu",
        "enrollment_date": datetime.date(2021, 9, 1)
    },
    {
        "name": "Kabir Mehta",
        "date_of_birth": datetime.date(2006, 7, 30),
        "email": "kabir.mehta@example.com",
        "phone": "+91-98345-67890",
        "course": "Artificial Intelligence",
        "address": "77 Marine Drive, Mumbai, Maharashtra",
        "enrollment_date": datetime.date(2024, 8, 5)
    },
    {
        "name": "Sneha Roy",
        "date_of_birth": datetime.date(2004, 12, 5),
        "email": "sneha.roy@example.com",
        "phone": "+91-97456-12345",
        "course": "Electrical Engineering",
        "address": "12 Park Street, Kolkata, West Bengal",
        "enrollment_date": datetime.date(2022, 8, 20)
    },
    {
        "name": "Vikram Singh",
        "date_of_birth": datetime.date(2005, 4, 12),
        "email": "vikram.singh@example.com",
        "phone": "+91-96543-21098",
        "course": "Data Science",
        "address": "55 Pink City Heights, Jaipur, Rajasthan",
        "enrollment_date": datetime.date(2023, 8, 1)
    },
    {
        "name": "Pooja Hegde",
        "date_of_birth": datetime.date(2006, 1, 25),
        "email": "pooja.hegde@example.com",
        "phone": "+91-98111-22334",
        "course": "Biotechnology",
        "address": "33 Hilltop Colony, Pune, Maharashtra",
        "enrollment_date": datetime.date(2024, 7, 22)
    },
    {
        "name": "Aditya Rao",
        "date_of_birth": datetime.date(2003, 3, 14),
        "email": "aditya.rao@example.com",
        "phone": "+91-99000-11223",
        "course": "Computer Science",
        "address": "100 Jubilee Hills, Hyderabad, Telangana",
        "enrollment_date": datetime.date(2021, 8, 15)
    },
    {
        "name": "Meera Nambiar",
        "date_of_birth": datetime.date(2005, 8, 8),
        "email": "meera.nambiar@example.com",
        "phone": "+91-98777-66554",
        "course": "Artificial Intelligence",
        "address": "9 Ocean Breeze, Kochi, Kerala",
        "enrollment_date": datetime.date(2023, 9, 5)
    }
]

def seed_database():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        existing_count = db.query(Student).count()
        print(f"Current student records in database: {existing_count}")
        
        added_count = 0
        for data in DUMMY_STUDENTS:
            existing = db.query(Student).filter(Student.email == data["email"]).first()
            if not existing:
                student = Student(**data)
                db.add(student)
                added_count += 1
        
        db.commit()
        print(f"Successfully added {added_count} new dummy student records!")
        print(f"Total student records now in database: {db.query(Student).count()}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
