from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import bcrypt

from models import Base, User, Faculty, FacultyDesignation, Role
from config import settings

# Create database connection
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_faculty():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if faculty role exists
        faculty_role = db.query(Role).filter(Role.name == "FACULTY").first()
        if not faculty_role:
            faculty_role = Role(name="FACULTY")
            db.add(faculty_role)
            db.commit()
            db.refresh(faculty_role)
        
        # Check if faculty table has data
        existing_faculty = db.query(Faculty).count()
        
        if existing_faculty == 0:
            print("Adding sample faculty data...")
            
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
                    "education": ["M.Sc. in Human-Computer Interaction, University of Washington", "B.Sc. in Computer Science, University of Dhaka"],
                    "courses": ["CSE 341: Human-Computer Interaction", "CSE 342: User Interface Design", "CSE 343: Mobile Application Development"],
                    "research_interests": ["Accessibility", "Mobile UX", "Interaction Design", "Usability Testing"]
                }
            ]
            
            for faculty_info in faculty_data:
                # Check if user already exists
                existing_user = db.query(User).filter(User.email == faculty_info["email"]).first()
                
                if not existing_user:
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
                        office=faculty_info["office"],
                        image=faculty_info["image"],
                        website=faculty_info["website"],
                        publications=faculty_info["publications"],
                        experience=faculty_info["experience"],
                        is_chairman=faculty_info["is_chairman"],
                        bio=faculty_info["bio"],
                        education=faculty_info["education"],
                        courses=faculty_info["courses"],
                        research_interests=faculty_info["research_interests"]
                    )
                    db.add(faculty)
                    db.commit()
                    
                    print(f"Added faculty: {faculty_info['name']}")
                else:
                    print(f"Faculty {faculty_info['name']} already exists")
            
            print(f"Added {len(faculty_data)} faculty members")
        else:
            print(f"Found {existing_faculty} existing faculty members, skipping sample data creation")
            
    except Exception as e:
        print(f"Error setting up faculty data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_faculty()
