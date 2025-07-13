from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Event, EventType, EventStatus, Role
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid

# Load environment variables
load_dotenv()

# Database connection
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_events_table():
    # Create the events table
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have events data
        existing_events = db.query(Event).count()
        
        # Check if faculty role exists for organizer reference
        faculty_role = db.query(Role).filter(Role.name == "FACULTY").first()
        if not faculty_role:
            faculty_role = Role(name="FACULTY")
            db.add(faculty_role)
            db.commit()
            db.refresh(faculty_role)
        
        # Check if student role exists for organizer reference
        student_role = db.query(Role).filter(Role.name == "STUDENT").first()
        if not student_role:
            student_role = Role(name="STUDENT")
            db.add(student_role)
            db.commit()
            db.refresh(student_role)
        
        if existing_events == 0:
            print("Adding sample events...")
            
            # Current date for reference
            now = datetime.utcnow()
            
            # Sample events with different dates and statuses
            events = [
                Event(
                    title="Annual CSE Tech Fest",
                    description="Join us for the biggest tech festival of the year featuring coding competitions, hackathons, and tech talks from industry leaders.",
                    type=EventType.COMPETITION,
                    status=EventStatus.UPCOMING,
                    start_date=now + timedelta(days=30),
                    end_date=now + timedelta(days=32),
                    venue="CSE Building, University of Dhaka",
                    organizer_role_id=faculty_role.id,
                    max_participants=500,
                    registered_count=0,
                    registration_required=True,
                    registration_deadline=now + timedelta(days=25),
                    fee=500.0,
                    tags=["competition", "hackathon", "tech fest", "coding"]
                ),
                Event(
                    title="Machine Learning Workshop",
                    description="A hands-on workshop on machine learning fundamentals and practical applications using Python and TensorFlow.",
                    type=EventType.WORKSHOP,
                    status=EventStatus.REGISTRATION_OPEN,
                    start_date=now + timedelta(days=15),
                    end_date=now + timedelta(days=15),
                    venue="Lab 2, CSE Department",
                    speaker="Dr. Palash Roy",
                    organizer_role_id=faculty_role.id,
                    max_participants=50,
                    registered_count=12,
                    registration_required=True,
                    registration_deadline=now + timedelta(days=10),
                    fee=0.0,
                    tags=["machine learning", "workshop", "python", "tensorflow"]
                ),
                Event(
                    title="Research Methodology Seminar",
                    description="Learn about research methodologies, paper writing, and publication strategies for graduate students.",
                    type=EventType.SEMINAR,
                    status=EventStatus.UPCOMING,
                    start_date=now + timedelta(days=7),
                    end_date=now + timedelta(days=7),
                    venue="Seminar Room, CSE Department",
                    speaker="Dr. Ismat Rahman",
                    organizer_role_id=faculty_role.id,
                    max_participants=100,
                    registered_count=0,
                    registration_required=True,
                    registration_deadline=now + timedelta(days=5),
                    fee=0.0,
                    tags=["research", "seminar", "academic", "publication"]
                ),
                Event(
                    title="International Conference on Computer Science",
                    description="Annual international conference featuring research presentations, keynote speeches, and networking opportunities.",
                    type=EventType.CONFERENCE,
                    status=EventStatus.REGISTRATION_OPEN,
                    start_date=now + timedelta(days=60),
                    end_date=now + timedelta(days=62),
                    venue="Senate Building, University of Dhaka",
                    organizer_role_id=faculty_role.id,
                    max_participants=300,
                    registered_count=45,
                    registration_required=True,
                    registration_deadline=now + timedelta(days=45),
                    fee=1000.0,
                    external_link="https://iccs.du.ac.bd",
                    tags=["conference", "research", "international", "networking"]
                ),
                Event(
                    title="CSE Cultural Night",
                    description="Annual cultural program organized by CSE students featuring music, dance, and drama performances.",
                    type=EventType.CULTURAL,
                    status=EventStatus.UPCOMING,
                    start_date=now + timedelta(days=45),
                    end_date=now + timedelta(days=45),
                    venue="TSC Auditorium, University of Dhaka",
                    organizer_role_id=student_role.id,
                    max_participants=200,
                    registered_count=0,
                    registration_required=False,
                    fee=0.0,
                    tags=["cultural", "entertainment", "student activity"]
                ),
                Event(
                    title="Web Development Bootcamp",
                    description="Intensive 3-day bootcamp on modern web development technologies including React, Node.js, and MongoDB.",
                    type=EventType.WORKSHOP,
                    status=EventStatus.COMPLETED,
                    start_date=now - timedelta(days=15),
                    end_date=now - timedelta(days=13),
                    venue="Lab 3, CSE Department",
                    speaker="Dr. Farhan Ahmed",
                    organizer_role_id=faculty_role.id,
                    max_participants=40,
                    registered_count=40,
                    registration_required=True,
                    registration_deadline=now - timedelta(days=20),
                    fee=500.0,
                    tags=["web development", "react", "node.js", "mongodb", "bootcamp"]
                ),
                Event(
                    title="Competitive Programming Contest",
                    description="Monthly programming contest to enhance algorithmic problem-solving skills.",
                    type=EventType.COMPETITION,
                    status=EventStatus.ONGOING,
                    start_date=now - timedelta(days=1),
                    end_date=now + timedelta(days=1),
                    venue="Online (Codeforces)",
                    organizer_role_id=student_role.id,
                    max_participants=100,
                    registered_count=78,
                    registration_required=True,
                    registration_deadline=now - timedelta(days=2),
                    fee=0.0,
                    external_link="https://codeforces.com",
                    tags=["competitive programming", "algorithms", "contest", "online"]
                ),
                Event(
                    title="Industry-Academia Collaboration Seminar",
                    description="Seminar on bridging the gap between industry and academia in computer science education and research.",
                    type=EventType.SEMINAR,
                    status=EventStatus.REGISTRATION_CLOSED,
                    start_date=now + timedelta(days=5),
                    end_date=now + timedelta(days=5),
                    venue="Conference Room, CSE Department",
                    speaker="Multiple Industry Leaders",
                    organizer_role_id=faculty_role.id,
                    max_participants=80,
                    registered_count=80,
                    registration_required=True,
                    registration_deadline=now - timedelta(days=1),
                    fee=0.0,
                    tags=["industry", "academia", "collaboration", "career"]
                )
            ]
            
            db.add_all(events)
            db.commit()
            
            print("Sample events added successfully!")
        else:
            print("Events table already has data. Skipping sample data creation.")
            
    except Exception as e:
        print(f"Error setting up events table: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_events_table()
