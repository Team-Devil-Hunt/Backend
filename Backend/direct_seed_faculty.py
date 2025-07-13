"""
Direct seed script for faculty data.
This script directly inserts faculty data into the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import bcrypt
import json

from models import Base, User, Faculty, FacultyDesignation, Role
from config import settings

# Create database connection
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_faculty():
    """Seed faculty data directly into the database."""
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if faculty role exists
        faculty_role = db.query(Role).filter(Role.name == "FACULTY").first()
        if not faculty_role:
            print("Creating FACULTY role...")
            faculty_role = Role(name="FACULTY")
            db.add(faculty_role)
            db.commit()
            db.refresh(faculty_role)
        
        # Clear existing faculty data
        print("Clearing existing faculty data...")
        faculty_count = db.query(Faculty).count()
        if faculty_count > 0:
            # Get all faculty IDs
            faculty_ids = [f.id for f in db.query(Faculty).all()]
            
            # Delete faculty records
            db.query(Faculty).delete()
            db.commit()
            
            # Delete associated user records
            for user_id in faculty_ids:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    db.delete(user)
            db.commit()
            print(f"Deleted {faculty_count} existing faculty records")
        
        # Sample faculty data
        faculty_data = [
            {
                "name": "Dr. Palash Roy",
                "email": "palash.roy@cse.du.ac.bd",
                "password": "password123",
                "designation": FacultyDesignation.PROFESSOR,
                "department": "Computer Science and Engineering",
                "expertise": ["Machine Learning", "Artificial Intelligence", "Data Mining", "Computer Vision"],
                "office": "Room 301, CSE Building",
                "image": "/assets/images/faculty/palash-roy.jpg",
                "website": "https://example.com/palash-roy",
                "publications": 45,
                "experience": 15,
                "is_chairman": True,
                "bio": "Dr. Palash Roy is a Professor and Chairman of the Department of Computer Science and Engineering at the University of Dhaka. He has over 15 years of experience in teaching and research in the field of Artificial Intelligence and Machine Learning.",
                "short_bio": "Leading researcher in machine learning and AI.",
                "education": ["Ph.D. in Computer Science, MIT", "M.Sc. in Computer Science, Stanford University", "B.Sc. in Computer Science, University of Dhaka"],
                "courses": ["CSE 401: Artificial Intelligence", "CSE 402: Machine Learning", "CSE 403: Data Mining"],
                "research_interests": ["Deep Learning", "Computer Vision", "Natural Language Processing", "Pattern Recognition"]
            },
            {
                "name": "Dr. Ismat Rahman",
                "email": "ismat.rahman@cse.du.ac.bd",
                "password": "password123",
                "designation": FacultyDesignation.ASSOCIATE_PROFESSOR,
                "department": "Computer Science and Engineering",
                "expertise": ["Software Engineering", "Database Systems", "Web Technologies"],
                "office": "Room 302, CSE Building",
                "image": "/assets/images/faculty/ismat-rahman.jpg",
                "website": "https://example.com/ismat-rahman",
                "publications": 28,
                "experience": 10,
                "is_chairman": False,
                "bio": "Dr. Ismat Rahman is an Associate Professor at the Department of Computer Science and Engineering, University of Dhaka. Her research focuses on software engineering methodologies and database systems.",
                "short_bio": "Expert in software engineering methodologies and web.",
                "education": ["Ph.D. in Computer Science, University of California", "M.Sc. in Computer Science, University of Dhaka", "B.Sc. in Computer Science, University of Dhaka"],
                "courses": ["CSE 301: Database Systems", "CSE 302: Software Engineering", "CSE 303: Web Technologies"],
                "research_interests": ["Software Testing", "Database Optimization", "Web Security", "Cloud Computing"]
            },
            {
                "name": "Dr. Anik Ahmed",
                "email": "anik.ahmed@cse.du.ac.bd",
                "password": "password123",
                "designation": FacultyDesignation.ASSISTANT_PROFESSOR,
                "department": "Computer Science and Engineering",
                "expertise": ["Computer Networks", "Cybersecurity", "Internet of Things"],
                "office": "Room 303, CSE Building",
                "image": "/assets/images/faculty/anik-ahmed.jpg",
                "website": "https://example.com/anik-ahmed",
                "publications": 15,
                "experience": 7,
                "is_chairman": False,
                "bio": "Dr. Anik Ahmed is an Assistant Professor specializing in Computer Networks and Cybersecurity. His current research focuses on securing IoT devices and network protocols.",
                "short_bio": "Specialist in network security and IoT.",
                "education": ["Ph.D. in Computer Networks, ETH Zurich", "M.Sc. in Computer Science, University of Dhaka", "B.Sc. in Computer Science, University of Dhaka"],
                "courses": ["CSE 321: Computer Networks", "CSE 322: Network Security", "CSE 323: Internet of Things"],
                "research_interests": ["Network Security", "IoT Security", "Wireless Networks", "Blockchain"]
            },
            {
                "name": "Nusrat Jahan",
                "email": "nusrat.jahan@cse.du.ac.bd",
                "password": "password123",
                "designation": FacultyDesignation.LECTURER,
                "department": "Computer Science and Engineering",
                "expertise": ["Human-Computer Interaction", "User Experience", "Mobile Interfaces"],
                "office": "Room 304, CSE Building",
                "image": "/assets/images/faculty/nusrat-jahan.jpg",
                "website": "https://example.com/nusrat-jahan",
                "publications": 5,
                "experience": 3,
                "is_chairman": False,
                "bio": "Nusrat Jahan is a Lecturer with expertise in Human-Computer Interaction and User Experience Design. She is passionate about creating accessible and intuitive interfaces.",
                "short_bio": "Passionate about UX design and accessibility.",
                "education": ["M.Sc. in Human-Computer Interaction, University of Washington", "B.Sc. in Computer Science, University of Dhaka"],
                "courses": ["CSE 341: Human-Computer Interaction", "CSE 342: User Interface Design", "CSE 343: Mobile Application Development"],
                "research_interests": ["Accessibility", "Mobile UX", "Interaction Design", "Usability Testing"]
            },
            {
                "name": "Dr. Shabbir Ahmed",
                "email": "shabbir.ahmed@cse.du.ac.bd",
                "password": "password123",
                "designation": FacultyDesignation.PROFESSOR,
                "department": "Computer Science and Engineering",
                "expertise": ["Distributed Systems", "Cloud Computing", "Big Data"],
                "office": "Room 305, CSE Building",
                "image": "/assets/images/faculty/shabbir-ahmed.jpg",
                "website": "https://example.com/shabbir-ahmed",
                "publications": 38,
                "experience": 12,
                "is_chairman": False,
                "bio": "Dr. Shabbir Ahmed is a Professor specializing in Distributed Systems and Cloud Computing. He has contributed significantly to the field of Big Data processing frameworks.",
                "short_bio": "Expert in distributed systems and cloud computing.",
                "education": ["Ph.D. in Computer Science, University of Toronto", "M.Sc. in Computer Science, University of Dhaka", "B.Sc. in Computer Science, University of Dhaka"],
                "courses": ["CSE 411: Distributed Systems", "CSE 412: Cloud Computing", "CSE 413: Big Data Analytics"],
                "research_interests": ["Distributed Algorithms", "Cloud Security", "Big Data Processing", "Edge Computing"]
            }
        ]
        
        # Add faculty data
        for faculty_info in faculty_data:
            # Hash password
            hashed_password = bcrypt.hashpw(faculty_info["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Create user
            user = User(
                name=faculty_info["name"],
                email=faculty_info["email"],
                password=hashed_password,
                role_id=faculty_role.id,
                created_at=datetime.utcnow()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create faculty profile
            faculty = Faculty(
                id=user.id,
                designation=faculty_info["designation"],
                department=faculty_info["department"],
                expertise=faculty_info["expertise"],
                office=faculty_info.get("office"),
                image=faculty_info.get("image"),
                website=faculty_info.get("website"),
                publications=faculty_info.get("publications", 0),
                experience=faculty_info.get("experience", 0),
                rating=4.5,  # Default rating
                is_chairman=faculty_info.get("is_chairman", False),
                bio=faculty_info.get("bio"),
                short_bio=faculty_info.get("short_bio"),
                education=faculty_info.get("education", []),
                courses=faculty_info.get("courses", []),
                research_interests=faculty_info.get("research_interests", []),
                recent_publications=[],  # Empty list for now
                awards=[],  # Empty list for now
                office_hours="Monday-Thursday: 10:00 AM - 12:00 PM"  # Default office hours
            )
            db.add(faculty)
            db.commit()
            
            print(f"Added faculty: {faculty_info['name']}")
        
        print(f"Added {len(faculty_data)} faculty members")
            
    except Exception as e:
        print(f"Error seeding faculty data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_faculty()
