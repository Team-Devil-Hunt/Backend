import psycopg2
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Database connection parameters
db_params = {
    'dbname': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USERNAME'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOSTNAME'),
    'port': os.getenv('DATABASE_PORT')
}

# Connect to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Get the current date for reference
current_date = datetime.now()

# Sample event data
events = [
    {
        "title": "Annual CSE Hackathon 2023",
        "description": "Join us for a 48-hour coding marathon where students compete to build innovative solutions to real-world problems. Prizes include cash rewards, internship opportunities, and more!",
        "type": "COMPETITION",
        "status": "UPCOMING",
        "start_date": (current_date + timedelta(days=15)).isoformat(),
        "end_date": (current_date + timedelta(days=17)).isoformat(),
        "venue": "CSE Building, 3rd Floor Lab Complex",
        "speaker": None,
        "organizer_role_id": 1,  # Assuming role_id 1 exists (e.g., "Faculty" or "Department")
        "max_participants": 150,
        "registered_count": 87,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=10)).isoformat(),
        "fee": 500,
        "external_link": "https://cse.du.ac.bd/hackathon2023",
        "tags": json.dumps(["hackathon", "coding", "competition", "prizes"])
    },
    {
        "title": "Machine Learning Workshop Series",
        "description": "A comprehensive 3-day workshop covering the fundamentals of machine learning, deep learning, and their applications. Perfect for beginners and intermediate learners.",
        "type": "WORKSHOP",
        "status": "REGISTRATION_OPEN",
        "start_date": (current_date + timedelta(days=7)).isoformat(),
        "end_date": (current_date + timedelta(days=9)).isoformat(),
        "venue": "CSE Seminar Room",
        "speaker": "Dr. Anisur Rahman",
        "organizer_role_id": 1,
        "max_participants": 50,
        "registered_count": 32,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=5)).isoformat(),
        "fee": 1000,
        "external_link": "https://cse.du.ac.bd/ml-workshop",
        "tags": json.dumps(["machine learning", "AI", "workshop", "hands-on"])
    },
    {
        "title": "Guest Lecture: Blockchain and Cryptocurrency",
        "description": "An insightful lecture on the future of blockchain technology and its impact on various industries. Learn about cryptocurrency, smart contracts, and decentralized applications.",
        "type": "SEMINAR",
        "status": "UPCOMING",
        "start_date": (current_date + timedelta(days=20)).isoformat(),
        "end_date": (current_date + timedelta(days=20)).isoformat(),
        "venue": "Arts Building Auditorium",
        "speaker": "Prof. Mahfuzur Rahman",
        "organizer_role_id": 1,
        "max_participants": 200,
        "registered_count": 45,
        "registration_required": False,
        "registration_deadline": None,
        "fee": 0,
        "external_link": None,
        "tags": json.dumps(["blockchain", "cryptocurrency", "lecture", "technology"])
    },
    {
        "title": "CSE Annual Conference 2023",
        "description": "The premier academic conference showcasing research work from students and faculty members. Topics include AI, cybersecurity, data science, and more.",
        "type": "CONFERENCE",
        "status": "REGISTRATION_OPEN",
        "start_date": (current_date + timedelta(days=45)).isoformat(),
        "end_date": (current_date + timedelta(days=47)).isoformat(),
        "venue": "University Senate Building",
        "speaker": None,
        "organizer_role_id": 1,
        "max_participants": 300,
        "registered_count": 120,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=30)).isoformat(),
        "fee": 2000,
        "external_link": "https://cse.du.ac.bd/conference2023",
        "tags": json.dumps(["conference", "research", "academic", "papers"])
    },
    {
        "title": "Freshers' Reception 2023",
        "description": "A warm welcome to the new batch of CSE students. Join us for an evening of cultural performances, games, and networking.",
        "type": "CULTURAL",
        "status": "UPCOMING",
        "start_date": (current_date + timedelta(days=25)).isoformat(),
        "end_date": (current_date + timedelta(days=25)).isoformat(),
        "venue": "TSC Auditorium",
        "speaker": None,
        "organizer_role_id": 1,
        "max_participants": 250,
        "registered_count": 180,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=20)).isoformat(),
        "fee": 0,
        "external_link": None,
        "tags": json.dumps(["freshers", "cultural", "reception", "networking"])
    },
    {
        "title": "Web Development Bootcamp",
        "description": "Intensive 5-day bootcamp covering HTML, CSS, JavaScript, React, and Node.js. Build real-world projects and enhance your portfolio.",
        "type": "WORKSHOP",
        "status": "UPCOMING",
        "start_date": (current_date + timedelta(days=30)).isoformat(),
        "end_date": (current_date + timedelta(days=35)).isoformat(),
        "venue": "CSE Building, Lab 301",
        "speaker": "Md. Tarikul Islam",
        "organizer_role_id": 1,
        "max_participants": 40,
        "registered_count": 25,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=25)).isoformat(),
        "fee": 1500,
        "external_link": "https://cse.du.ac.bd/webdev-bootcamp",
        "tags": json.dumps(["web development", "bootcamp", "coding", "frontend", "backend"])
    },
    {
        "title": "Programming Contest: Code Warriors",
        "description": "Test your programming skills in this competitive coding contest. Solve algorithmic problems and compete for exciting prizes.",
        "type": "COMPETITION",
        "status": "REGISTRATION_OPEN",
        "start_date": (current_date + timedelta(days=12)).isoformat(),
        "end_date": (current_date + timedelta(days=12)).isoformat(),
        "venue": "CSE Building, Lab Complex",
        "speaker": None,
        "organizer_role_id": 1,
        "max_participants": 100,
        "registered_count": 68,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=10)).isoformat(),
        "fee": 300,
        "external_link": "https://cse.du.ac.bd/code-warriors",
        "tags": json.dumps(["programming", "algorithms", "contest", "competitive coding"])
    },
    {
        "title": "Career Fair 2023",
        "description": "Connect with top tech companies and explore job opportunities. Bring your resume and be prepared for on-the-spot interviews.",
        "type": "ACADEMIC",
        "status": "UPCOMING",
        "start_date": (current_date + timedelta(days=60)).isoformat(),
        "end_date": (current_date + timedelta(days=60)).isoformat(),
        "venue": "University Gymnasium",
        "speaker": None,
        "organizer_role_id": 1,
        "max_participants": 500,
        "registered_count": 210,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=55)).isoformat(),
        "fee": 0,
        "external_link": "https://cse.du.ac.bd/career-fair",
        "tags": json.dumps(["career", "jobs", "recruitment", "networking"])
    },
    {
        "title": "Research Symposium: AI in Healthcare",
        "description": "A symposium focusing on the applications of artificial intelligence in healthcare. Featuring presentations from faculty members and industry experts.",
        "type": "SEMINAR",
        "status": "UPCOMING",
        "start_date": (current_date + timedelta(days=40)).isoformat(),
        "end_date": (current_date + timedelta(days=40)).isoformat(),
        "venue": "Medical Faculty Building, Conference Hall",
        "speaker": "Dr. Shahida Rafique",
        "organizer_role_id": 1,
        "max_participants": 150,
        "registered_count": 75,
        "registration_required": False,
        "registration_deadline": None,
        "fee": 0,
        "external_link": None,
        "tags": json.dumps(["AI", "healthcare", "research", "symposium"])
    },
    {
        "title": "Mobile App Development Workshop",
        "description": "Learn to build cross-platform mobile applications using Flutter. This hands-on workshop will guide you through building a complete app from scratch.",
        "type": "WORKSHOP",
        "status": "REGISTRATION_OPEN",
        "start_date": (current_date + timedelta(days=18)).isoformat(),
        "end_date": (current_date + timedelta(days=19)).isoformat(),
        "venue": "CSE Building, Lab 302",
        "speaker": "Tanvir Ahmed",
        "organizer_role_id": 1,
        "max_participants": 35,
        "registered_count": 22,
        "registration_required": True,
        "registration_deadline": (current_date + timedelta(days=15)).isoformat(),
        "fee": 800,
        "external_link": "https://cse.du.ac.bd/flutter-workshop",
        "tags": json.dumps(["mobile development", "Flutter", "app development", "workshop"])
    }
]

try:
    # Insert events into the database
    for event in events:
        cur.execute("""
            INSERT INTO events (
                title, description, type, status, start_date, end_date, venue, speaker,
                organizer_role_id, max_participants, registered_count, registration_required,
                registration_deadline, fee, external_link, tags, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            event["title"],
            event["description"],
            event["type"],
            event["status"],
            event["start_date"],
            event["end_date"],
            event["venue"],
            event["speaker"],
            event["organizer_role_id"],
            event["max_participants"],
            event["registered_count"],
            event["registration_required"],
            event["registration_deadline"],
            event["fee"],
            event["external_link"],
            event["tags"],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
    
    # Commit the transaction
    conn.commit()
    print("Successfully inserted 10 events into the database.")

except Exception as e:
    # Roll back in case of error
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
