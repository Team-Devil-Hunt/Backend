import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
import random

# Load environment variables
load_dotenv()

# Database connection parameters
db_params = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'csedu'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# Connect to the database
print("Connecting to PostgreSQL database...")
conn = psycopg2.connect(**db_params)
conn.autocommit = False
cursor = conn.cursor()

# Check if there are existing exams
cursor.execute("SELECT COUNT(*) FROM exams")
exam_count = cursor.fetchone()[0]

if exam_count > 0:
    print(f"Exams already exist ({exam_count} found). Deleting existing exams...")
    cursor.execute("DELETE FROM exams")
    conn.commit()
    print("Existing exams deleted.")

# Get course codes and titles
cursor.execute("SELECT code, title FROM courses")
courses = cursor.fetchall()

if not courses:
    print("No courses found. Please run direct_seed_courses.py first.")
    conn.close()
    exit(1)

print(f"Found {len(courses)} courses. Creating exams...")

# Get faculty names
cursor.execute("""
SELECT u.id, u.name, f.designation
FROM users u
JOIN faculty f ON u.id = f.id
LIMIT 10
""")
faculty = cursor.fetchall()

if not faculty:
    print("No faculty found. Using default faculty names...")
    faculty = [
        (1, "Dr. Mohammad Shoyaib", "Professor"),
        (2, "Dr. Md. Mustafizur Rahman", "Associate Professor"),
        (3, "Dr. Anisur Rahman", "Assistant Professor"),
        (4, "Dr. Sadia Sharmin", "Assistant Professor"),
        (5, "Dr. Md. Shariful Islam", "Associate Professor")
    ]

# Exam types
exam_types = ["midterm", "final", "retake", "improvement"]

# Rooms
rooms = ["301", "302", "303", "304", "501", "601", "Lab 1", "Lab 2", "Lab 3", "Lab 4", "Hardware Lab"]

# Batches
batches = ["25", "24", "23", "22", "MSc", "PhD"]

# Status options
status_options = ["scheduled", "ongoing", "completed", "cancelled"]

# Create exams for each course
exam_count = 0
today = datetime.now().date()

for i, (code, title) in enumerate(courses):
    # Determine batch and semester based on course code
    if "CSE" in code and any(char.isdigit() for char in code):
        course_num = int(''.join(filter(str.isdigit, code)))
        year = (course_num // 100) % 10
        
        if year <= 4:
            # Undergraduate
            batch = batches[year % len(batches)]
            semester = (year - 1) * 2 + (i % 2) + 1
        else:
            # Graduate
            batch = "MSc" if i % 2 == 0 else "PhD"
            semester = i % 4 + 1
    else:
        # Default values
        batch = batches[i % len(batches)]
        semester = i % 8 + 1
    
    # Create exams (midterm and final) for each course
    for exam_type_idx, exam_type in enumerate(exam_types[:2]):  # Only midterm and final by default
        # Set exam date (midterms earlier, finals later)
        exam_date = today + timedelta(days=(10 + i*2) if exam_type == "midterm" else (30 + i*2))
        
        # Set exam time
        start_hour = 9 + (i % 6)  # Between 9 AM and 2 PM
        start_time = f"{start_hour:02d}:00"
        end_time = f"{start_hour + 2:02d}:00"  # 2-hour exams
        
        # Set room
        room = f"Room {rooms[i % len(rooms)]}"
        
        # Set invigilators (2 random faculty members)
        invigilator_indices = random.sample(range(len(faculty)), min(2, len(faculty)))
        invigilators = [faculty[idx][1] for idx in invigilator_indices]
        
        # Set status (mostly scheduled, some ongoing or completed)
        status_weight = [0.8, 0.1, 0.1, 0.0]  # 80% scheduled, 10% ongoing, 10% completed
        status = random.choices(status_options, weights=status_weight)[0]
        
        # Set notes
        notes = ""
        if exam_type == "midterm":
            notes = "Bring your student ID and calculator."
        elif exam_type == "final":
            notes = "Comprehensive exam covering all course material."
        
        # Insert exam
        cursor.execute("""
        INSERT INTO exams (
            "courseCode", "courseTitle", semester, batch, "examType", 
            date, "startTime", "endTime", room, invigilators, 
            status, notes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            code, title, semester, batch, exam_type,
            exam_date, start_time, end_time, room, json.dumps(invigilators),
            status, notes
        ))
        exam_count += 1
    
    # Add some retake and improvement exams (for about 20% of courses)
    if i % 5 == 0:
        exam_type = random.choice(exam_types[2:])  # retake or improvement
        exam_date = today + timedelta(days=45 + i)
        start_hour = 14 + (i % 4)  # Between 2 PM and 5 PM
        start_time = f"{start_hour:02d}:00"
        end_time = f"{start_hour + 2:02d}:00"
        room = f"Room {rooms[(i + 3) % len(rooms)]}"
        invigilator_indices = random.sample(range(len(faculty)), min(2, len(faculty)))
        invigilators = [faculty[idx][1] for idx in invigilator_indices]
        status = "scheduled"
        notes = f"Only for students who registered for {exam_type}."
        
        cursor.execute("""
        INSERT INTO exams (
            "courseCode", "courseTitle", semester, batch, "examType", 
            date, "startTime", "endTime", room, invigilators, 
            status, notes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            code, title, semester, batch, exam_type,
            exam_date, start_time, end_time, room, json.dumps(invigilators),
            status, notes
        ))
        exam_count += 1

# Commit the changes
conn.commit()

# Get the count of inserted exams
cursor.execute("SELECT COUNT(*) FROM exams")
inserted_count = cursor.fetchone()[0]
print(f"Successfully added {exam_count} exams to the database.")

# Close the connection
cursor.close()
conn.close()
print("Database connection closed.")
