"""
Seed script to populate the database with exam data for testing purposes.
This script directly inserts exam data into the database.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Exam, Course
import json
from datetime import datetime, date, timedelta
import random

def seed_exams():
    db = SessionLocal()
    try:
        # First, get all courses to link exams to them
        courses = db.query(Course).all()
        if not courses:
            print("No courses found in database. Please seed courses first.")
            return
        
        # Clear existing exams
        db.query(Exam).delete()
        db.commit()
        
        # Sample exam types
        exam_types = ["midterm", "final", "quiz", "retake", "improvement"]
        
        # Sample locations
        locations = [
            "Main Building",
            "Science Complex",
            "Engineering Building",
            "Arts Building",
            "Library Annex"
        ]
        
        # Sample rooms
        rooms = [
            "Room 101",
            "Room 102",
            "Room 201",
            "Room 202",
            "Room 301",
            "Room 302",
            "Lab 101",
            "Lab 102",
            "Lecture Hall 1",
            "Lecture Hall 2"
        ]
        
        # Sample invigilators
        invigilators = [
            "Dr. Ahmed Khan",
            "Prof. Sarah Johnson",
            "Dr. Michael Smith",
            "Prof. Emily Brown",
            "Dr. David Wilson",
            "Prof. Jessica Lee",
            "Dr. Robert Taylor",
            "Prof. Lisa Anderson",
            "Dr. James Martin",
            "Prof. Maria Garcia"
        ]
        
        # Sample materials allowed
        materials_allowed_options = [
            ["Calculator", "Textbook", "Notes"],
            ["Calculator", "Formula Sheet"],
            ["Calculator"],
            ["None"],
            ["Open Book"],
            ["One A4 Sheet of Notes"]
        ]
        
        # Sample instructions
        instructions_options = [
            "Answer all questions. Show your work for partial credit.",
            "Choose any 5 out of the 7 questions to answer.",
            "Section A is compulsory. Choose 2 questions from Section B.",
            "No electronic devices allowed except for calculators.",
            "Time limit strictly enforced. No extra time will be given.",
            "Write your answers in the provided answer booklet."
        ]
        
        # Generate exams for each course
        exams = []
        today = date.today()
        
        for course in courses:
            # Create 2-4 exams per course
            num_exams = random.randint(2, 4)
            
            for i in range(num_exams):
                # Determine exam type
                exam_type = random.choice(exam_types)
                
                # Generate a title based on course and exam type
                title = f"{course.code} {exam_type.capitalize()}"
                if i > 0:
                    title += f" {i}"
                
                # Determine date - mix of past, current, and future exams
                days_offset = random.randint(-30, 30)  # -30 to +30 days from today
                exam_date = today + timedelta(days=days_offset)
                
                # Determine time
                start_hour = random.randint(8, 16)  # 8 AM to 4 PM
                start_minute = random.choice([0, 30])
                duration_hours = random.randint(1, 3)
                
                start_time = f"{start_hour:02d}:{start_minute:02d}"
                end_hour = start_hour + duration_hours
                if end_hour > 18:
                    end_hour = 18  # Cap at 6 PM
                end_time = f"{end_hour:02d}:{start_minute:02d}"
                
                # Determine status based on date
                if exam_date < today:
                    status = "completed"
                elif exam_date > today:
                    status = "scheduled"
                else:
                    current_hour = datetime.now().hour
                    if current_hour < start_hour:
                        status = "scheduled"
                    elif current_hour > end_hour:
                        status = "completed"
                    else:
                        status = "ongoing"
                
                # Generate random invigilators
                num_invigilators = random.randint(1, 3)
                exam_invigilators = random.sample(invigilators, num_invigilators)
                
                # Generate syllabus topics based on course
                syllabus_topics = []
                if course.description:
                    # Extract potential topics from description
                    words = course.description.split()
                    if len(words) > 10:
                        for _ in range(random.randint(3, 6)):
                            start_idx = random.randint(0, len(words) - 3)
                            topic_length = random.randint(2, 3)
                            topic = " ".join(words[start_idx:start_idx + topic_length])
                            syllabus_topics.append(topic)
                
                # Generate marks
                total_marks = random.choice([50, 100, 150, 200])
                obtained_marks = None
                if status == "completed":
                    obtained_marks = random.randint(int(total_marks * 0.5), total_marks)
                
                # Create the exam
                exam = Exam(
                    title=title,
                    course_id=course.id,
                    courseCode=course.code,
                    courseTitle=course.title,
                    semester=course.semester,
                    batch=f"20{random.randint(18, 22)}",  # Random batch between 2018-2022
                    examType=exam_type,
                    date=exam_date,
                    startTime=start_time,
                    endTime=end_time,
                    room=random.choice(rooms),
                    location=random.choice(locations),
                    invigilators=json.dumps(exam_invigilators),
                    status=status,
                    total_marks=total_marks,
                    obtained_marks=obtained_marks,
                    instructions=random.choice(instructions_options),
                    materials_allowed=json.dumps(random.choice(materials_allowed_options)),
                    syllabus_topics=json.dumps(syllabus_topics) if syllabus_topics else None,
                    notes=f"This is a {exam_type} exam for {course.code}. Please arrive 15 minutes early."
                )
                
                exams.append(exam)
        
        # Add all exams to the database
        db.add_all(exams)
        db.commit()
        
        print(f"Successfully seeded {len(exams)} exams for {len(courses)} courses.")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding exams: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_exams()
