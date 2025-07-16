import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DATABASE_HOSTNAME")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASS = os.getenv("DATABASE_PASSWORD")

# Connect to the database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

# Create a cursor
cur = conn.cursor()

# Function to clear existing data
def clear_existing_data():
    print("Clearing existing announcement data...")
    cur.execute("DELETE FROM announcements")
    conn.commit()
    print("Existing announcement data cleared.")

# Function to seed announcements
def seed_announcements():
    print("Seeding announcements...")
    
    # Announcement types and priority levels
    types = ["ACADEMIC", "ADMIN", "GENERAL"]
    priorities = ["HIGH", "MEDIUM", "LOW"]
    
    # Sample announcement data
    announcements = [
        {
            "title": "Fall 2025 Registration Deadline Extended",
            "content": "The registration deadline for Fall 2025 semester has been extended to August 15, 2025. All students must complete their registration by this date. Please contact the Registrar's Office if you have any questions or need assistance with the registration process.",
            "date": datetime.now() - timedelta(days=1),
            "type": "ACADEMIC",
            "priority": "HIGH",
            "image": "/assets/images/announcements/registration.jpg"
        },
        {
            "title": "Faculty Meeting: Curriculum Review",
            "content": "All faculty members are invited to attend the curriculum review meeting on July 20, 2025 at 2:00 PM in Room 301. The meeting will focus on updating the undergraduate curriculum to incorporate the latest developments in computer science and engineering.",
            "date": datetime.now() - timedelta(days=2),
            "type": "ADMIN",
            "priority": "MEDIUM",
            "image": None
        },
        {
            "title": "Campus Wi-Fi Maintenance",
            "content": "The campus Wi-Fi network will be undergoing maintenance on July 18, 2025 from 10:00 PM to 2:00 AM. During this time, internet connectivity may be intermittent or unavailable. We apologize for any inconvenience this may cause.",
            "date": datetime.now() - timedelta(days=3),
            "type": "GENERAL",
            "priority": "LOW",
            "image": None
        },
        {
            "title": "Final Examination Schedule Released",
            "content": "The final examination schedule for Spring 2025 has been released. Please check the department website for your exam dates and times. If you have any scheduling conflicts, please contact the Examination Committee as soon as possible.",
            "date": datetime.now() - timedelta(days=4),
            "type": "ACADEMIC",
            "priority": "HIGH",
            "image": "/assets/images/announcements/exam.jpg"
        },
        {
            "title": "Scholarship Application Deadline",
            "content": "The deadline for applying to the Merit Scholarship Program for the upcoming academic year is July 31, 2025. Eligible students must have a minimum GPA of 3.5 and demonstrate financial need. Application forms are available at the Office of Financial Aid.",
            "date": datetime.now() - timedelta(days=5),
            "type": "ACADEMIC",
            "priority": "MEDIUM",
            "image": "/assets/images/announcements/scholarship.jpg"
        },
        {
            "title": "New Research Lab Opening",
            "content": "We are pleased to announce the opening of our new Artificial Intelligence and Machine Learning Research Lab. The lab is equipped with state-of-the-art computing resources and will support advanced research in AI, machine learning, and data science.",
            "date": datetime.now() - timedelta(days=6),
            "type": "GENERAL",
            "priority": "MEDIUM",
            "image": "/assets/images/announcements/lab.jpg"
        },
        {
            "title": "Department Picnic",
            "content": "The annual department picnic will be held on July 25, 2025 at Central Park. All faculty, staff, and students are invited to attend. Food and refreshments will be provided. Please RSVP by July 20 to ensure we have enough supplies for everyone.",
            "date": datetime.now() - timedelta(days=7),
            "type": "GENERAL",
            "priority": "LOW",
            "image": "/assets/images/announcements/picnic.jpg"
        },
        {
            "title": "Guest Lecture: Advances in Quantum Computing",
            "content": "Dr. Sarah Johnson from MIT will be giving a guest lecture on 'Recent Advances in Quantum Computing' on July 22, 2025 at 3:00 PM in the Main Auditorium. All interested students and faculty are encouraged to attend this informative session.",
            "date": datetime.now() - timedelta(days=8),
            "type": "ACADEMIC",
            "priority": "MEDIUM",
            "image": "/assets/images/announcements/lecture.jpg"
        },
        {
            "title": "Library Hours Extended During Finals Week",
            "content": "The university library will extend its hours during finals week (August 1-7, 2025). The library will be open from 7:00 AM to 2:00 AM to provide students with additional study space and resources during this critical period.",
            "date": datetime.now() - timedelta(days=9),
            "type": "GENERAL",
            "priority": "MEDIUM",
            "image": None
        },
        {
            "title": "Software License Renewal",
            "content": "The department's licenses for various software packages (MATLAB, Visual Studio, etc.) will be renewed on July 31, 2025. Please make sure to update your software after this date to continue using these resources without interruption.",
            "date": datetime.now() - timedelta(days=10),
            "type": "ADMIN",
            "priority": "LOW",
            "image": None
        }
    ]
    
    # Insert announcements
    for announcement in announcements:
        cur.execute(
            """
            INSERT INTO announcements (title, content, date, type, priority, image, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                announcement["title"],
                announcement["content"],
                announcement["date"],
                announcement["type"],
                announcement["priority"],
                announcement["image"],
                datetime.now(),
                datetime.now()
            )
        )
    
    conn.commit()
    print(f"Seeded {len(announcements)} announcements.")

# Main execution
try:
    clear_existing_data()
    seed_announcements()
    print("Announcement data seeding completed successfully!")
except Exception as e:
    conn.rollback()
    print(f"Error seeding announcement data: {e}")
finally:
    cur.close()
    conn.close()
