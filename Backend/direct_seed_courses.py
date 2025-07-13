import psycopg2
import json
from datetime import datetime

# Database connection settings
username = 'postgres'
password = 'password'
host = 'localhost'
port = '5432'
database = 'csedu'

# Connect to the database
conn = psycopg2.connect(
    dbname=database,
    user=username,
    password=password,
    host=host,
    port=port
)
conn.autocommit = False
cursor = conn.cursor()

# Check if programs already exist
cursor.execute("SELECT COUNT(*) FROM programs")
program_count = cursor.fetchone()[0]

# Sample programs
programs = [
    {
        "title": "Bachelor of Science in Computer Science and Engineering",
        "level": "Undergraduate",
        "duration": "4 years",
        "total_students": 120,
        "total_courses": 40,
        "total_credits": 160,
        "short_description": "A comprehensive undergraduate program covering computer science fundamentals, software development, and engineering principles.",
        "description": "The Bachelor of Science in Computer Science and Engineering program at the University of Dhaka provides students with a strong foundation in computer science theory, programming, algorithms, and software engineering. The curriculum includes practical projects, internships, and research opportunities.",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Master of Science in Computer Science",
        "level": "Graduate",
        "duration": "2 years",
        "total_students": 45,
        "total_courses": 12,
        "total_credits": 36,
        "short_description": "An advanced program focusing on specialized areas of computer science research and development.",
        "description": "The Master of Science in Computer Science program offers advanced coursework and research opportunities in specialized areas such as artificial intelligence, machine learning, computer networks, and software engineering. Students complete a thesis or project demonstrating their expertise in their chosen specialization.",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Master of Science in Software Engineering",
        "level": "Graduate",
        "duration": "2 years",
        "total_students": 30,
        "total_courses": 12,
        "total_credits": 36,
        "short_description": "A specialized program focusing on advanced software development methodologies and practices.",
        "description": "The Master of Science in Software Engineering program prepares students for leadership roles in software development. The curriculum covers advanced topics in software architecture, project management, quality assurance, and emerging technologies.",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

program_ids = []

if program_count == 0:
    print("Adding programs...")
    for program in programs:
        cursor.execute("""
            INSERT INTO programs (
                title, level, duration, total_students, total_courses, total_credits, 
                short_description, description, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (
            program["title"], program["level"], program["duration"], 
            program["total_students"], program["total_courses"], program["total_credits"],
            program["short_description"], program["description"], 
            program["created_at"], program["updated_at"]
        ))
        program_ids.append(cursor.fetchone()[0])
    conn.commit()
    print(f"Added {len(programs)} programs")
else:
    print(f"Programs already exist ({program_count} found). Getting program IDs...")
    cursor.execute("SELECT id, level, title FROM programs")
    existing_programs = cursor.fetchall()
    for program in existing_programs:
        program_ids.append(program[0])
        print(f"ID: {program[0]}, Level: {program[1]}, Title: {program[2]}")

# Get program IDs for reference
cursor.execute("SELECT id FROM programs WHERE level = 'Undergraduate' LIMIT 1")
undergraduate_result = cursor.fetchone()
if undergraduate_result:
    undergraduate_program_id = undergraduate_result[0]
else:
    # Create undergraduate program if it doesn't exist
    print("Creating undergraduate program...")
    cursor.execute("""
        INSERT INTO programs (
            title, level, duration, total_students, total_courses, total_credits, 
            short_description, description, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """, (
        "Bachelor of Science in Computer Science and Engineering", "Undergraduate", "4 years", 
        120, 40, 160,
        "A comprehensive undergraduate program covering computer science fundamentals, software development, and engineering principles.",
        "The Bachelor of Science in Computer Science and Engineering program at the University of Dhaka provides students with a strong foundation in computer science theory, programming, algorithms, and software engineering.",
        datetime.utcnow(), datetime.utcnow()
    ))
    undergraduate_program_id = cursor.fetchone()[0]
    conn.commit()

cursor.execute("SELECT id FROM programs WHERE level = 'Graduate' AND title LIKE '%Computer Science%' LIMIT 1")
graduate_cs_result = cursor.fetchone()
if graduate_cs_result:
    graduate_program_cs_id = graduate_cs_result[0]
else:
    # Create Computer Science graduate program if it doesn't exist
    print("Creating Computer Science graduate program...")
    cursor.execute("""
        INSERT INTO programs (
            title, level, duration, total_students, total_courses, total_credits, 
            short_description, description, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """, (
        "Master of Science in Computer Science", "Graduate", "2 years", 
        45, 12, 36,
        "An advanced program focusing on specialized areas of computer science research and development.",
        "The Master of Science in Computer Science program offers advanced coursework and research opportunities in specialized areas such as artificial intelligence, machine learning, computer networks, and software engineering.",
        datetime.utcnow(), datetime.utcnow()
    ))
    graduate_program_cs_id = cursor.fetchone()[0]
    conn.commit()

cursor.execute("SELECT id FROM programs WHERE level = 'Graduate' AND title LIKE '%Software Engineering%' LIMIT 1")
graduate_se_result = cursor.fetchone()
if graduate_se_result:
    graduate_program_se_id = graduate_se_result[0]
else:
    # Create Software Engineering graduate program if it doesn't exist
    print("Creating Software Engineering graduate program...")
    cursor.execute("""
        INSERT INTO programs (
            title, level, duration, total_students, total_courses, total_credits, 
            short_description, description, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """, (
        "Master of Science in Software Engineering", "Graduate", "2 years", 
        30, 12, 36,
        "A specialized program focusing on advanced software development methodologies and practices.",
        "The Master of Science in Software Engineering program prepares students for leadership roles in software development. The curriculum covers advanced topics in software architecture, project management, quality assurance, and emerging technologies.",
        datetime.utcnow(), datetime.utcnow()
    ))
    graduate_program_se_id = cursor.fetchone()[0]
    conn.commit()

print(f"Undergraduate Program ID: {undergraduate_program_id}")
print(f"Graduate CS Program ID: {graduate_program_cs_id}")
print(f"Graduate SE Program ID: {graduate_program_se_id}")

# Sample courses
courses = [
    # First Year, First Semester (Undergraduate)
    {
        "code": "CSE101",
        "title": "Introduction to Computer Science",
        "description": "An introductory course covering the basics of computer science, programming concepts, and problem-solving techniques.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Beginner",
        "prerequisites": json.dumps(["None"]),
        "specialization": "Core",
        "semester": 1,
        "year": 1,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE102",
        "title": "Programming Fundamentals",
        "description": "Introduction to programming using a high-level language, covering basic syntax, data types, control structures, and functions.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Beginner",
        "prerequisites": json.dumps(["None"]),
        "specialization": "Core",
        "semester": 1,
        "year": 1,
        "program_id": undergraduate_program_id
    },
    {
        "code": "MATH101",
        "title": "Calculus I",
        "description": "Introduction to differential and integral calculus, including limits, derivatives, and applications.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["None"]),
        "specialization": "Mathematics",
        "semester": 1,
        "year": 1,
        "program_id": undergraduate_program_id
    },
    
    # First Year, Second Semester (Undergraduate)
    {
        "code": "CSE103",
        "title": "Data Structures",
        "description": "Study of fundamental data structures including arrays, linked lists, stacks, queues, trees, and graphs, and their applications.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE102"]),
        "specialization": "Core",
        "semester": 2,
        "year": 1,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE104",
        "title": "Digital Logic Design",
        "description": "Introduction to digital systems, Boolean algebra, logic gates, combinational and sequential circuits, and memory elements.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE101"]),
        "specialization": "Hardware",
        "semester": 2,
        "year": 1,
        "program_id": undergraduate_program_id
    },
    {
        "code": "MATH102",
        "title": "Linear Algebra",
        "description": "Study of vector spaces, linear transformations, matrices, determinants, eigenvalues, and eigenvectors.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["MATH101"]),
        "specialization": "Mathematics",
        "semester": 2,
        "year": 1,
        "program_id": undergraduate_program_id
    },
    
    # Second Year, First Semester (Undergraduate)
    {
        "code": "CSE201",
        "title": "Algorithms",
        "description": "Analysis and design of algorithms, including searching, sorting, graph algorithms, and complexity analysis.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE103"]),
        "specialization": "Core",
        "semester": 1,
        "year": 2,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE202",
        "title": "Object-Oriented Programming",
        "description": "Principles of object-oriented programming, including classes, objects, inheritance, polymorphism, and encapsulation.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE102"]),
        "specialization": "Core",
        "semester": 1,
        "year": 2,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE203",
        "title": "Computer Architecture",
        "description": "Study of computer organization and architecture, including processor design, memory hierarchy, and I/O systems.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE104"]),
        "specialization": "Hardware",
        "semester": 1,
        "year": 2,
        "program_id": undergraduate_program_id
    },
    
    # Second Year, Second Semester (Undergraduate)
    {
        "code": "CSE204",
        "title": "Database Systems",
        "description": "Introduction to database concepts, relational model, SQL, database design, and transaction processing.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE103"]),
        "specialization": "Core",
        "semester": 2,
        "year": 2,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE205",
        "title": "Operating Systems",
        "description": "Principles of operating systems, including process management, memory management, file systems, and security.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["CSE203"]),
        "specialization": "Core",
        "semester": 2,
        "year": 2,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE206",
        "title": "Software Engineering",
        "description": "Software development methodologies, requirements analysis, design, testing, and project management.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE202"]),
        "specialization": "Software Engineering",
        "semester": 2,
        "year": 2,
        "program_id": undergraduate_program_id
    },
    
    # Third Year, First Semester (Undergraduate)
    {
        "code": "CSE301",
        "title": "Computer Networks",
        "description": "Principles of computer networks, protocols, network architecture, and network security.",
        "credits": 4,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["CSE205"]),
        "specialization": "Networking",
        "semester": 1,
        "year": 3,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE302",
        "title": "Artificial Intelligence",
        "description": "Introduction to artificial intelligence, including search algorithms, knowledge representation, and machine learning.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["CSE201"]),
        "specialization": "AI",
        "semester": 1,
        "year": 3,
        "program_id": undergraduate_program_id
    },
    {
        "code": "CSE303",
        "title": "Web Programming",
        "description": "Development of web applications using HTML, CSS, JavaScript, and server-side technologies.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Intermediate",
        "prerequisites": json.dumps(["CSE204"]),
        "specialization": "Web Development",
        "semester": 1,
        "year": 3,
        "program_id": undergraduate_program_id
    },
    
    # Graduate Courses (Computer Science)
    {
        "code": "CSE501",
        "title": "Advanced Algorithms",
        "description": "Advanced topics in algorithm design and analysis, including approximation algorithms, randomized algorithms, and computational complexity.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["Undergraduate Algorithms"]),
        "specialization": "Theoretical Computer Science",
        "semester": 1,
        "year": 1,
        "program_id": graduate_program_cs_id
    },
    {
        "code": "CSE502",
        "title": "Machine Learning",
        "description": "Theory and implementation of machine learning algorithms, including supervised and unsupervised learning, neural networks, and deep learning.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["Undergraduate AI"]),
        "specialization": "AI",
        "semester": 1,
        "year": 1,
        "program_id": graduate_program_cs_id
    },
    {
        "code": "CSE503",
        "title": "Distributed Systems",
        "description": "Principles and practice of distributed systems, including communication, synchronization, consistency, and fault tolerance.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["Operating Systems", "Computer Networks"]),
        "specialization": "Systems",
        "semester": 1,
        "year": 1,
        "program_id": graduate_program_cs_id
    },
    
    # Graduate Courses (Software Engineering)
    {
        "code": "SE501",
        "title": "Advanced Software Engineering",
        "description": "Advanced topics in software engineering, including software architecture, design patterns, and agile methodologies.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["Undergraduate Software Engineering"]),
        "specialization": "Software Engineering",
        "semester": 1,
        "year": 1,
        "program_id": graduate_program_se_id
    },
    {
        "code": "SE502",
        "title": "Software Quality Assurance",
        "description": "Principles and practices of software quality assurance, including testing, inspection, and formal verification.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["Advanced Software Engineering"]),
        "specialization": "Software Engineering",
        "semester": 1,
        "year": 1,
        "program_id": graduate_program_se_id
    },
    {
        "code": "SE503",
        "title": "Software Project Management",
        "description": "Principles and practices of software project management, including planning, estimation, risk management, and team management.",
        "credits": 3,
        "duration": "1 semester",
        "difficulty": "Advanced",
        "prerequisites": json.dumps(["Advanced Software Engineering"]),
        "specialization": "Software Engineering",
        "semester": 2,
        "year": 1,
        "program_id": graduate_program_se_id
    }
]

# Check if courses already exist
cursor.execute("SELECT COUNT(*) FROM courses")
course_count = cursor.fetchone()[0]

if course_count > 0:
    print(f"Courses already exist ({course_count} found). Deleting existing courses...")
    cursor.execute("DELETE FROM courses")
    conn.commit()

# Add courses
print("Adding courses...")
for course in courses:
    cursor.execute("""
        INSERT INTO courses (
            code, title, description, credits, duration, difficulty, 
            rating, enrolled_students, prerequisites, specialization, 
            semester, year, program_id, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        course["code"], course["title"], course["description"], 
        course["credits"], course["duration"], course["difficulty"],
        0.0, 0, course["prerequisites"], course["specialization"],
        course["semester"], course["year"], course["program_id"],
        datetime.utcnow(), datetime.utcnow()
    ))

conn.commit()
print(f"Successfully added {len(courses)} courses to the database.")

# Close the connection
cursor.close()
conn.close()
