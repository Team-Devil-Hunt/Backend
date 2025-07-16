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
    CREATE TYPE class_type AS ENUM ('Lecture', 'Lab', 'Tutorial');
    CREATE TYPE class_status AS ENUM ('In Progress', 'Upcoming', 'Completed', 'Cancelled');
    
    CREATE TABLE class_schedules (
        id SERIAL PRIMARY KEY,
        course_code VARCHAR NOT NULL,
        course_name VARCHAR NOT NULL,
        type class_type NOT NULL,
        batch VARCHAR NOT NULL,
        semester VARCHAR NOT NULL,
        day VARCHAR NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        room VARCHAR NOT NULL,
        instructor_id INTEGER NOT NULL,
        instructor_name VARCHAR NOT NULL,
        instructor_designation VARCHAR NOT NULL,
        status class_status NOT NULL DEFAULT 'Upcoming',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
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
    print("No courses found. Please run seed_courses.py first.")
    conn.close()
    exit(1)

# Get faculty IDs and names
cursor.execute("""
SELECT u.id, u.name, f.designation
FROM users u
JOIN faculty f ON u.id = f.id
LIMIT 10
""")
faculty = cursor.fetchall()

if not faculty:
    print("No faculty found. Creating sample faculty...")
    # Create sample faculty users
    faculty_data = [
        (1, "Dr. Mohammad Shoyaib", "Professor"),
        (2, "Dr. Md. Mustafizur Rahman", "Associate Professor"),
        (3, "Dr. Anisur Rahman", "Assistant Professor"),
        (4, "Dr. Sadia Sharmin", "Assistant Professor"),
        (5, "Dr. Md. Shariful Islam", "Associate Professor")
    ]
    
    # Check if roles table exists
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'roles')")
    roles_table_exists = cursor.fetchone()[0]
    
    if not roles_table_exists:
        print("Creating roles table...")
        cursor.execute("""
        CREATE TABLE roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL
        )
        """)
        
        # Insert basic roles
        cursor.execute("""
        INSERT INTO roles (id, name) VALUES 
        (1, 'admin'),
        (2, 'faculty'),
        (3, 'student')
        """)
        conn.commit()
        print("Created roles table and inserted basic roles.")
    
    # Check if users table exists
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
    users_table_exists = cursor.fetchone()[0]
    
    if not users_table_exists:
        print("Creating users table...")
        cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            password VARCHAR NOT NULL,
            role_id INTEGER REFERENCES roles(id),
            username VARCHAR,
            contact VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Created users table.")
    
    # Check if faculty table exists
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'faculty')")
    faculty_table_exists = cursor.fetchone()[0]
    
    if not faculty_table_exists:
        print("Creating faculty table...")
        cursor.execute("""
        CREATE TYPE faculty_designation AS ENUM ('Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer');
        
        CREATE TABLE faculty (
            id INTEGER PRIMARY KEY REFERENCES users(id),
            designation faculty_designation NOT NULL,
            department VARCHAR NOT NULL,
            expertise JSONB NOT NULL,
            office VARCHAR,
            image VARCHAR,
            website VARCHAR,
            publications INTEGER DEFAULT 0,
            experience INTEGER DEFAULT 0,
            rating FLOAT DEFAULT 0.0,
            is_chairman BOOLEAN DEFAULT FALSE,
            bio TEXT,
            short_bio TEXT,
            education JSONB,
            courses JSONB,
            research_interests JSONB,
            recent_publications JSONB,
            awards JSONB,
            office_hours VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    
    # Insert sample faculty
    for faculty_id, name, designation in faculty_data:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (faculty_id,))
        user = cursor.fetchone()
        
        if not user:
            email = name.lower().replace(" ", ".") + "@cse.du.ac.bd"
            cursor.execute("""
            INSERT INTO users (id, name, email, password, role_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, (faculty_id, name, email, "password123", 2))  # role_id 2 for faculty
        
        # Check if faculty exists
        cursor.execute("SELECT id FROM faculty WHERE id = %s", (faculty_id,))
        faculty_exists = cursor.fetchone()
        
        if not faculty_exists:
            expertise = json.dumps(["Algorithms", "Machine Learning", "Computer Vision"])
            cursor.execute("""
            INSERT INTO faculty (id, designation, department, expertise)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, (faculty_id, designation, "Computer Science and Engineering", expertise))
    
    conn.commit()
    print("Sample faculty created.")
    
    # Get the created faculty
    cursor.execute("""
    SELECT u.id, u.name, f.designation
    FROM users u
    JOIN faculty f ON u.id = f.id
    LIMIT 10
    """)
    faculty = cursor.fetchall()

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

# Create class schedules
print("Adding class schedules...")
class_schedules = []

# Helper function to create datetime objects for time
def create_time(time_str):
    hour, minute = map(int, time_str.split(':'))
    return datetime.combine(datetime.today(), time(hour, minute))

# Create schedules for each course
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
    faculty_idx = i % len(faculty)
    faculty_id, faculty_name, faculty_designation = faculty[faculty_idx]
    
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
    
    # For some courses, add a lab class
    if i % 3 == 0:  # Every third course has a lab
        # Use a different day and time slot for the lab
        lab_day = days[(i + 2) % len(days)]
        lab_time_slot_idx = (i + 3) % len(time_slots)
        lab_start_time_str, lab_end_time_str = time_slots[lab_time_slot_idx]
        
        lab_start_time = create_time(lab_start_time_str)
        lab_end_time = create_time(lab_end_time_str)
        
        lab_room = f"Lab {(i % 4) + 1}"
        lab_faculty_idx = (i + 1) % len(faculty)
        lab_faculty_id, lab_faculty_name, lab_faculty_designation = faculty[lab_faculty_idx]
        
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

# Commit the changes
conn.commit()

# Get the count of inserted class schedules
cursor.execute("SELECT COUNT(*) FROM class_schedules")
inserted_count = cursor.fetchone()[0]
print(f"Successfully added {inserted_count} class schedules to the database.")

# Close the connection
cursor.close()
conn.close()
print("Database connection closed.")
