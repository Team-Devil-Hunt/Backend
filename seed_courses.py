from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from database import Base
from models import Program, Course
import datetime

# Database connection settings
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
database = 'csedu'

# Create database connection
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

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
        "description": "The Bachelor of Science in Computer Science and Engineering program at the University of Dhaka provides students with a strong foundation in computer science theory, programming, algorithms, and software engineering. The curriculum includes practical projects, internships, and research opportunities."
    },
    {
        "title": "Master of Science in Computer Science",
        "level": "Graduate",
        "duration": "2 years",
        "total_students": 45,
        "total_courses": 12,
        "total_credits": 36,
        "short_description": "An advanced program focusing on specialized areas of computer science research and development.",
        "description": "The Master of Science in Computer Science program offers advanced coursework and research opportunities in specialized areas such as artificial intelligence, machine learning, computer networks, and software engineering. Students complete a thesis or project demonstrating their expertise in their chosen specialization."
    },
    {
        "title": "Master of Science in Software Engineering",
        "level": "Graduate",
        "duration": "2 years",
        "total_students": 30,
        "total_courses": 12,
        "total_credits": 36,
        "short_description": "A specialized program focusing on advanced software development methodologies and practices.",
        "description": "The Master of Science in Software Engineering program prepares students for leadership roles in software development. The curriculum covers advanced topics in software architecture, project management, quality assurance, and emerging technologies."
    }
]

# First check if programs already exist
existing_programs = db.query(Program).all()
if not existing_programs:
    print("Adding programs...")
    for program_data in programs:
        program = Program(**program_data)
        db.add(program)
    db.commit()
else:
    print(f"Programs already exist ({len(existing_programs)} found). Skipping program creation.")

# Get program IDs for reference
undergraduate_program = db.query(Program).filter(Program.level == "Undergraduate").first()
graduate_program_cs = db.query(Program).filter(Program.level == "Graduate", Program.title.like("%Computer Science")).first()
graduate_program_se = db.query(Program).filter(Program.level == "Graduate", Program.title.like("%Software Engineering")).first()

if not undergraduate_program or not graduate_program_cs or not graduate_program_se:
    print("Error: Required programs not found. Please check the database.")
    exit(1)

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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": undergraduate_program.id
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
        "program_id": graduate_program_cs.id
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
        "program_id": graduate_program_cs.id
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
        "program_id": graduate_program_cs.id
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
        "program_id": graduate_program_se.id
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
        "program_id": graduate_program_se.id
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
        "program_id": graduate_program_se.id
    }
]

# Check if courses already exist
existing_courses = db.query(Course).all()
if existing_courses:
    print(f"Courses already exist ({len(existing_courses)} found). Deleting existing courses...")
    for course in existing_courses:
        db.delete(course)
    db.commit()

# Add courses
print("Adding courses...")
for course_data in courses:
    course = Course(**course_data)
    db.add(course)

db.commit()
print(f"Successfully added {len(courses)} courses to the database.")
