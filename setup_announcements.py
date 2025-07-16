from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Announcement, AnnouncementType, PriorityLevel
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import settings

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_announcements_table():
    # Create the announcements table
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have announcements data
        existing_announcements = db.query(Announcement).count()
        
        if existing_announcements == 0:
            print("Adding sample announcements data...")
            
            # Current date for reference
            now = datetime.utcnow()
            
            # Sample announcements
            announcements = [
                Announcement(
                    title="Fall 2025 Registration Opens Next Week",
                    content="Registration for the Fall 2025 semester will open on July 20, 2025. Students are advised to check their registration time slots and prepare their course selections in advance. Please ensure all outstanding fees are cleared before registration.",
                    date=now - timedelta(days=2),
                    type=AnnouncementType.ACADEMIC,
                    priority=PriorityLevel.HIGH,
                    image="/assets/images/announcements/registration.jpg"
                ),
                Announcement(
                    title="New AI Research Lab Inauguration",
                    content="We are pleased to announce the inauguration of our new Artificial Intelligence Research Laboratory on August 5, 2025. The state-of-the-art facility is equipped with the latest hardware including NVIDIA A100 GPUs and specialized AI workstations. The lab will support advanced research in machine learning, computer vision, and natural language processing.",
                    date=now - timedelta(days=5),
                    type=AnnouncementType.GENERAL,
                    priority=PriorityLevel.MEDIUM,
                    image="/assets/images/announcements/ai-lab.jpg"
                ),
                Announcement(
                    title="Faculty Positions Available",
                    content="The Department of Computer Science and Engineering is seeking applications for Assistant Professor positions in the areas of Cybersecurity, Data Science, and Software Engineering. Candidates should have a PhD in Computer Science or a related field and a strong publication record. Application deadline is September 15, 2025.",
                    date=now - timedelta(days=7),
                    type=AnnouncementType.ADMIN,
                    priority=PriorityLevel.MEDIUM,
                    image=None
                ),
                Announcement(
                    title="Congratulations to Programming Contest Winners",
                    content="Congratulations to Team CodeBreakers for securing first place in the National Collegiate Programming Contest 2025! The team members - Anik Rahman, Fahmida Akter, and Tanvir Ahmed - solved 9 out of 10 problems in record time. They will represent Bangladesh in the upcoming ACM ICPC World Finals.",
                    date=now - timedelta(days=10),
                    type=AnnouncementType.GENERAL,
                    priority=PriorityLevel.LOW,
                    image="/assets/images/announcements/programming-contest.jpg"
                ),
                Announcement(
                    title="Mandatory Seminar for Final Year Students",
                    content="All final year students are required to attend the Career Preparation Seminar on July 25, 2025, from 10:00 AM to 1:00 PM at the CSE Auditorium. The seminar will cover resume building, interview preparation, and industry insights from alumni working at leading tech companies.",
                    date=now - timedelta(days=1),
                    type=AnnouncementType.ACADEMIC,
                    priority=PriorityLevel.HIGH,
                    image=None
                ),
                Announcement(
                    title="Summer Internship Opportunities",
                    content="Several leading tech companies including Google, Microsoft, and Samsung R&D are offering summer internships for CSE students. Interested students should submit their applications through the department portal by July 30, 2025. A minimum CGPA of 3.5 is required to apply.",
                    date=now - timedelta(days=3),
                    type=AnnouncementType.ACADEMIC,
                    priority=PriorityLevel.MEDIUM,
                    image="/assets/images/announcements/internship.jpg"
                ),
                Announcement(
                    title="Department Building Renovation Schedule",
                    content="The renovation of the east wing of the CSE building will take place from August 1 to August 15, 2025. During this period, classes scheduled in rooms E101-E110 will be temporarily relocated to the Science Building. Updated room assignments will be posted on the department website.",
                    date=now - timedelta(days=4),
                    type=AnnouncementType.ADMIN,
                    priority=PriorityLevel.HIGH,
                    image=None
                ),
                Announcement(
                    title="New Research Grant Awarded",
                    content="The department has been awarded a prestigious research grant of $500,000 from the National Science Foundation for the project 'Secure and Scalable IoT Systems for Smart Cities'. The project will be led by Dr. Palash Roy and will involve opportunities for graduate students to participate in cutting-edge research.",
                    date=now - timedelta(days=8),
                    type=AnnouncementType.GENERAL,
                    priority=PriorityLevel.LOW,
                    image="/assets/images/announcements/research-grant.jpg"
                )
            ]
            
            db.add_all(announcements)
            db.commit()
            
            print("Sample announcements data added successfully!")
        else:
            print("Announcements table already has data. Skipping sample data creation.")
            
    except Exception as e:
        print(f"Error setting up announcements table: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_announcements_table()
