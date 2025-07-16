import psycopg2
from datetime import datetime, time, timedelta
import os
from dotenv import load_dotenv
import json

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

# Check if class_schedules table exists
cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'class_schedules')")
table_exists = cursor.fetchone()[0]

if not table_exists:
    print("Table 'class_schedules' does not exist. Creating it...")
    
    cursor.execute("""
    CREATE TABLE class_schedules (
        id SERIAL PRIMARY KEY,
        course_code VARCHAR NOT NULL,
        course_name VARCHAR NOT NULL,
        type VARCHAR NOT NULL,
        batch VARCHAR NOT NULL,
        semester VARCHAR NOT NULL,
        day VARCHAR NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        room VARCHAR NOT NULL,
        instructor_id INTEGER NOT NULL,
        instructor_name VARCHAR NOT NULL,
        instructor_designation VARCHAR NOT NULL,
        status VARCHAR NOT NULL DEFAULT 'Upcoming',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("Table 'class_schedules' created successfully.")

# Check if there are existing class schedules
cursor.execute("SELECT COUNT(*) FROM class_schedules")
schedule_count = cursor.fetchone()[0]

if schedule_count > 0:
    print(f"Class schedules already exist ({schedule_count} found). Deleting existing schedules...")
    cursor.execute("DELETE FROM class_schedules")
    conn.commit()
    print("Existing class schedules deleted.")

# Get course codes and titles
cursor.execute("SELECT code, title FROM courses")
courses = cursor.fetchall()

if not courses:
    print("No courses found. Please run direct_seed_courses.py first.")
    conn.close()
    exit(1)

print(f"Found {len(courses)} courses. Creating class schedules...")

# Sample faculty data
faculty_data = [
    (1, "Dr. Mohammad Shoyaib", "Professor"),
    (2, "Dr. Md. Mustafizur Rahman", "Associate Professor"),
    (3, "Dr. Anisur Rahman", "Assistant Professor"),
    (4, "Dr. Sadia Sharmin", "Assistant Professor"),
    (5, "Dr. Md. Shariful Islam", "Associate Professor")
]

# Days of the week
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

# Rooms
rooms = ["301", "302", "303", "304", "501", "601", "Lab 1", "Lab 2", "Lab 3", "Lab 4", "Hardware Lab"]

# Batches
batches = ["25", "24", "23", "22", "MSc", "PhD"]

# Time slots
time_slots = [
    ("08:00", "09:30"),
    ("09:30", "11:00"),
    ("11:00", "12:30"),
    ("12:30", "14:00"),
    ("14:00", "15:30"),
    ("15:30", "17:00")
]

# Helper function to create datetime objects for time
def create_time(time_str):
    hour, minute = map(int, time_str.split(':'))
    return datetime.combine(datetime.today(), time(hour, minute))

# Create schedules for each course
class_count = 0
for i, (code, title) in enumerate(courses):
    # Determine batch and semester based on course code
    if "CSE" in code and any(char.isdigit() for char in code):
        course_num = int(''.join(filter(str.isdigit, code)))
        year = (course_num // 100) % 10
        
        if year <= 4:
            # Undergraduate
            batch = batches[year % len(batches)]
            semester = str((year - 1) * 2 + (i % 2) + 1)
        else:
            # Graduate
            batch = "MSc" if i % 2 == 0 else "PhD"
            semester = str(i % 4 + 1)
    else:
        # Default values
        batch = batches[i % len(batches)]
        semester = str(i % 8 + 1)
    
    # Create lecture class
    day = days[i % len(days)]
    time_slot_idx = i % len(time_slots)
    start_time_str, end_time_str = time_slots[time_slot_idx]
    
    start_time = create_time(start_time_str)
    end_time = create_time(end_time_str)
    
    room = rooms[i % len(rooms)]
    faculty_idx = i % len(faculty_data)
    faculty_id, faculty_name, faculty_designation = faculty_data[faculty_idx]
    
    # Insert lecture class
    cursor.execute("""
    INSERT INTO class_schedules (
        course_code, course_name, type, batch, semester, day, 
        start_time, end_time, room, instructor_id, instructor_name, 
        instructor_designation, status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        code, title, "Lecture", batch, semester, day,
        start_time, end_time, room, faculty_id, faculty_name,
        faculty_designation, "Upcoming"
    ))
    class_count += 1
    
    # For some courses, add a lab class
    if i % 3 == 0:  # Every third course has a lab
        # Use a different day and time slot for the lab
        lab_day = days[(i + 2) % len(days)]
        lab_time_slot_idx = (i + 3) % len(time_slots)
        lab_start_time_str, lab_end_time_str = time_slots[lab_time_slot_idx]
        
        lab_start_time = create_time(lab_start_time_str)
        lab_end_time = create_time(lab_end_time_str)
        
        lab_room = f"Lab {(i % 4) + 1}"
        lab_faculty_idx = (i + 1) % len(faculty_data)
        lab_faculty_id, lab_faculty_name, lab_faculty_designation = faculty_data[lab_faculty_idx]
        
        # Insert lab class
        cursor.execute("""
        INSERT INTO class_schedules (
            course_code, course_name, type, batch, semester, day, 
            start_time, end_time, room, instructor_id, instructor_name, 
            instructor_designation, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            code, title, "Lab", batch, semester, lab_day,
            lab_start_time, lab_end_time, lab_room, lab_faculty_id, lab_faculty_name,
            lab_faculty_designation, "Upcoming"
        ))
        class_count += 1

# Commit the changes
conn.commit()

# Get the count of inserted class schedules
cursor.execute("SELECT COUNT(*) FROM class_schedules")
inserted_count = cursor.fetchone()[0]
print(f"Successfully added {class_count} class schedules to the database.")

# Close the connection
cursor.close()
conn.close()
print("Database connection closed.")
