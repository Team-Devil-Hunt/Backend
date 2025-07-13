"""
Script to update faculty images in the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Faculty, User
from config import settings

# Create database connection
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_faculty_images():
    """Update faculty images based on their names."""
    # Create a session
    db = SessionLocal()
    
    try:
        # Image mapping based on faculty names
        image_mapping = {
            "Dr. Mohammad Shoyaib": "/assets/teacher/Palash_Roy.jpg",
            "Dr. Md. Mustafizur Rahman": "/assets/teacher/ashraful_alam.jpeg",
            "Dr. Anisur Rahman": "/assets/teacher/farhan_ahmed.jpg",
            "Dr. Sadia Sharmin": "/assets/teacher/suraiya_parvin.jpg",
            "Dr. Md. Shariful Islam": "/assets/teacher/hasan_babu.jpg"
        }
        
        # Get all faculty
        faculty_records = db.query(Faculty).all()
        
        for faculty in faculty_records:
            user = db.query(User).filter(User.id == faculty.id).first()
            if not user:
                continue
                
            # Update image based on name
            if user.name in image_mapping:
                faculty.image = image_mapping[user.name]
                print(f"Updated image for {user.name}: {faculty.image}")
            else:
                # Default image if no match
                faculty.image = "/assets/teacher/shabbir_ahmed.jpg"
                print(f"Set default image for {user.name}")
        
        db.commit()
        print("Faculty images updated successfully")
            
    except Exception as e:
        print(f"Error updating faculty images: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_faculty_images()
