import os
import sys
from datetime import datetime, timedelta
import random

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the models
from database import SessionLocal, engine
from models import Base, Exam, User

def setup_exams():
    db = SessionLocal()
    
    # Check if exams already exist
    existing_exams = db.query(Exam).count()
    if existing_exams > 0:
        print("Exams already exist. Skipping creation.")
        db.close()
        return
    
    print("Creating sample exams...")
    
    # Get some faculty users to use as invigilators
    faculty_users = db.query(User).filter(User.role_id == 2).limit(10).all()  # Assuming role_id 2 is for faculty
    if not faculty_users:
        print("No faculty users found. Creating exams with placeholder invigilators.")
        invigilator_names = [
            "Dr. Rashid Ahmed", 
            "Ms. Fatima Khan",
            "Prof. Hasanul Karim", 
            "Dr. Tahmina Akter",
            "Dr. Shahid Hasan", 
            "Ms. Nusrat Jahan",
            "Prof. Mahmud Hasan", 
            "Dr. Aisha Begum",
            "Dr. Kamal Uddin", 
            "Ms. Sabina Yasmin"
        ]
    else:
        invigilator_names = [user.name for user in faculty_users]
    
    # Sample exam data
    exams_data = [
        {
            "courseCode": "CSE-401",
            "courseTitle": "Artificial Intelligence",
            "semester": 4,
            "batch": "25",
            "examType": "midterm",
            "date": datetime.now() + timedelta(days=2),
            "startTime": "10:00",
            "endTime": "12:00",
            "room": "Room 301",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Bring your student ID and calculator."
        },
        {
            "courseCode": "CSE-303",
            "courseTitle": "Database Systems",
            "semester": 3,
            "batch": "25",
            "examType": "final",
            "date": datetime.now() + timedelta(days=7),
            "startTime": "09:00",
            "endTime": "12:00",
            "room": "Room 201",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Open book exam. Bring your textbook and notes."
        },
        {
            "courseCode": "CSE-205",
            "courseTitle": "Data Structures",
            "semester": 2,
            "batch": "26",
            "examType": "midterm",
            "date": datetime.now() - timedelta(days=3),
            "startTime": "14:00",
            "endTime": "16:00",
            "room": "Room 102",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "completed",
            "notes": "No electronic devices allowed."
        },
        {
            "courseCode": "CSE-501",
            "courseTitle": "Advanced Machine Learning",
            "semester": 5,
            "batch": "24",
            "examType": "final",
            "date": datetime.now() + timedelta(days=12),
            "startTime": "10:00",
            "endTime": "13:00",
            "room": "Room 401",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Bring your laptop with required software installed."
        },
        {
            "courseCode": "CSE-103",
            "courseTitle": "Introduction to Programming",
            "semester": 1,
            "batch": "27",
            "examType": "final",
            "date": datetime.now() - timedelta(days=1),
            "startTime": "09:00",
            "endTime": "11:00",
            "room": "Room 101",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "completed",
            "notes": "Bring your student ID."
        },
        {
            "courseCode": "CSE-307",
            "courseTitle": "Operating Systems",
            "semester": 3,
            "batch": "25",
            "examType": "midterm",
            "date": datetime.now() - timedelta(days=5),
            "startTime": "11:00",
            "endTime": "13:00",
            "room": "Room 201",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "completed",
            "notes": "Closed book exam."
        },
        {
            "courseCode": "CSE-407",
            "courseTitle": "Computer Networks",
            "semester": 4,
            "batch": "24",
            "examType": "improvement",
            "date": datetime.now() + timedelta(days=17),
            "startTime": "14:00",
            "endTime": "16:00",
            "room": "Room 302",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Only for students who registered for improvement."
        },
        {
            "courseCode": "CSE-203",
            "courseTitle": "Discrete Mathematics",
            "semester": 2,
            "batch": "26",
            "examType": "retake",
            "date": datetime.now() + timedelta(days=5),
            "startTime": "10:00",
            "endTime": "12:00",
            "room": "Room 102",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Only for students who failed in the regular exam."
        },
        {
            "courseCode": "CSE-601",
            "courseTitle": "Advanced Algorithms",
            "semester": 6,
            "batch": "23",
            "examType": "final",
            "date": datetime.now() + timedelta(days=9),
            "startTime": "09:00",
            "endTime": "12:00",
            "room": "Room 401",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Bring your algorithm design handbook."
        },
        {
            "courseCode": "CSE-405",
            "courseTitle": "Software Engineering",
            "semester": 4,
            "batch": "24",
            "examType": "final",
            "date": datetime.now() + timedelta(days=15),
            "startTime": "10:00",
            "endTime": "13:00",
            "room": "Room 301",
            "invigilators": [random.choice(invigilator_names), random.choice(invigilator_names)],
            "status": "scheduled",
            "notes": "Project documentation submission required before exam."
        }
    ]
    
    # Create exam objects
    exams = []
    for exam_data in exams_data:
        exam = Exam(
            courseCode=exam_data["courseCode"],
            courseTitle=exam_data["courseTitle"],
            semester=exam_data["semester"],
            batch=exam_data["batch"],
            examType=exam_data["examType"],
            date=exam_data["date"],
            startTime=exam_data["startTime"],
            endTime=exam_data["endTime"],
            room=exam_data["room"],
            invigilators=exam_data["invigilators"],
            status=exam_data["status"],
            notes=exam_data["notes"]
        )
        exams.append(exam)
    
    # Add to database
    db.add_all(exams)
    db.commit()
    
    print(f"Created {len(exams)} sample exams.")
    db.close()

if __name__ == "__main__":
    setup_exams()
