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

# Sample faculty data
faculty_data = [
    (1, "Dr. Mohammad Shoyaib", "Professor", "shoyaib@cse.du.ac.bd"),
    (2, "Dr. Md. Mustafizur Rahman", "Associate Professor", "mustafiz@cse.du.ac.bd"),
    (3, "Dr. Anisur Rahman", "Assistant Professor", "anis@cse.du.ac.bd"),
    (4, "Dr. Sadia Sharmin", "Assistant Professor", "sadia@cse.du.ac.bd"),
    (5, "Dr. Md. Shariful Islam", "Associate Professor", "shariful@cse.du.ac.bd")
]

# Check if faculty users exist
print("Checking for existing faculty users...")
faculty_ids = []
for faculty_id, _, _, _ in faculty_data:
    cursor.execute("SELECT id FROM users WHERE id = %s", (faculty_id,))
    result = cursor.fetchone()
    if result:
        faculty_ids.append(result[0])
        print(f"Faculty user with ID {faculty_id} already exists.")

# If no faculty users exist, create them
if not faculty_ids:
    print("No faculty users found. Creating faculty users...")
    
    # Get role_id for faculty
    cursor.execute("SELECT id FROM roles WHERE name = 'faculty'")
    role_result = cursor.fetchone()
    if not role_result:
        print("Creating 'faculty' role...")
        cursor.execute("INSERT INTO roles (name) VALUES ('faculty') RETURNING id")
        faculty_role_id = cursor.fetchone()[0]
    else:
        faculty_role_id = role_result[0]
    
    print(f"Using faculty role ID: {faculty_role_id}")
    
    # Create faculty users
    for faculty_id, name, designation, email in faculty_data:
        # Insert into users table
        cursor.execute("""
        INSERT INTO users (id, name, email, password, role_id, username, contact, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (id) DO NOTHING
        RETURNING id
        """, (
            faculty_id, 
            name, 
            email, 
            "password123", 
            faculty_role_id, 
            email.split('@')[0], 
            "+880-1XXX-XXXXXX"
        ))
        
        result = cursor.fetchone()
        if result:
            print(f"Created user: {name} with ID {result[0]}")
            faculty_ids.append(result[0])
            
            # Get designation enum value
            cursor.execute("SELECT unnest(enum_range(NULL::facultydesignation))")
            designations = [d[0] for d in cursor.fetchall()]
            
            # Convert designation to match enum
            enum_designation = designation.upper().replace(' ', '_')
            if enum_designation not in designations:
                enum_designation = designations[0]  # Use first available designation if not found
            
            # Create expertise JSON
            expertise = json.dumps(["Algorithms", "Machine Learning", "Computer Vision"])
            
            # Insert into faculty table
            cursor.execute("""
            INSERT INTO faculty (
                id, designation, department, expertise, office, image, 
                website, publications, experience, rating, is_chairman, 
                bio, short_bio, education, courses, research_interests, 
                recent_publications, awards, office_hours, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            ON CONFLICT (id) DO NOTHING
            """, (
                result[0],
                enum_designation,
                "Computer Science and Engineering",
                expertise,
                f"Room {300 + faculty_id}",
                None,
                None,
                faculty_id * 5,  # Random number of publications
                faculty_id + 5,  # Random years of experience
                4.5,  # Default rating
                False,  # Not chairman by default
                f"Detailed biography for {name}",
                f"Short bio for {name}",
                json.dumps([{"degree": "PhD", "institution": "University of Dhaka", "year": "2010"}]),
                json.dumps(["CSE101", "CSE201"]),
                json.dumps(["Machine Learning", "Computer Vision"]),
                json.dumps([{"title": "Recent Paper", "journal": "IEEE", "year": "2023"}]),
                json.dumps([{"name": "Best Teacher Award", "year": "2022"}]),
                "Sunday, Tuesday: 2:00 PM - 4:00 PM",
            ))
            print(f"Created faculty profile for {name}")
        else:
            print(f"User {name} already exists")

    conn.commit()
    print("Faculty users created successfully.")
else:
    print(f"Using existing faculty users: {faculty_ids}")

# Get course codes and titles
cursor.execute("SELECT code, title FROM courses")
courses = cursor.fetchall()

if not courses:
    print("No courses found. Please run direct_seed_courses.py first.")
    conn.close()
    exit(1)

print(f"Found {len(courses)} courses. Creating class schedules...")

# Check if there are existing class schedules
cursor.execute("SELECT COUNT(*) FROM class_schedules")
schedule_count = cursor.fetchone()[0]

if schedule_count > 0:
    print(f"Class schedules already exist ({schedule_count} found). Deleting existing schedules...")
    cursor.execute("DELETE FROM class_schedules")
    conn.commit()
    print("Existing class schedules deleted.")

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
    faculty_id, faculty_name, faculty_designation, _ = faculty_data[faculty_idx]
    
    # Insert lecture class - using uppercase enum values
    cursor.execute("""
    INSERT INTO class_schedules (
        course_code, course_name, type, batch, semester, day, 
        start_time, end_time, room, instructor_id, instructor_name, 
        instructor_designation, status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        code, title, "LECTURE", batch, semester, day,
        start_time, end_time, room, faculty_id, faculty_name,
        faculty_designation, "UPCOMING"
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
        lab_faculty_id, lab_faculty_name, lab_faculty_designation, _ = faculty_data[lab_faculty_idx]
        
        # Insert lab class - using uppercase enum values
        cursor.execute("""
        INSERT INTO class_schedules (
            course_code, course_name, type, batch, semester, day, 
            start_time, end_time, room, instructor_id, instructor_name, 
            instructor_designation, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            code, title, "LAB", batch, semester, lab_day,
            lab_start_time, lab_end_time, lab_room, lab_faculty_id, lab_faculty_name,
            lab_faculty_designation, "UPCOMING"
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
