from sqlalchemy.orm import Session
from database import get_db
from models import User, Role
from datetime import datetime
import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def add_test_faculty():
    db = next(get_db())
    
    # Get faculty role
    faculty_role = db.query(Role).filter(Role.name == "FACULTY").first()
    
    if not faculty_role:
        print("Faculty role not found. Please run seed_users.py first.")
        return
    
    # Check if test faculty already exists
    test_faculty = db.query(User).filter(User.email == "test.faculty@csedu.edu").first()
    
    if test_faculty:
        print(f"Test faculty already exists with ID: {test_faculty.id}")
        print(f"Email: test.faculty@csedu.edu")
        print(f"Password: password123")
        return
    
    # Create test faculty user with a known password
    test_faculty = User(
        name="Test Faculty User",
        email="test.faculty@csedu.edu",
        password=hash_password("password123"),
        role_id=faculty_role.id,
        username="testfaculty",
        contact="01712345678",
        created_at=datetime.utcnow()
    )
    
    db.add(test_faculty)
    db.commit()
    db.refresh(test_faculty)
    
    print(f"Test faculty created successfully with ID: {test_faculty.id}")
    print(f"Email: test.faculty@csedu.edu")
    print(f"Password: password123")

if __name__ == "__main__":
    add_test_faculty()
