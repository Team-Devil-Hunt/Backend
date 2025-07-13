from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Program, Course
from config import settings

# Create database connection
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_programs():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if program table has data
        existing_programs = db.query(Program).count()
        
        if existing_programs == 0:
            print("Adding sample program data...")
            
            # Sample program data
            programs_data = [
                {
                    "title": "Bachelor of Science in Computer Science and Engineering",
                    "level": "Undergraduate",
                    "duration": "4 years",
                    "short_description": "A comprehensive undergraduate program covering the fundamentals of computer science and engineering.",
                    "description": "The Bachelor of Science in Computer Science and Engineering program at the University of Dhaka provides students with a strong foundation in computer science theory and practical engineering skills. The curriculum covers programming, algorithms, data structures, computer architecture, operating systems, software engineering, and more.",
                    "specializations": ["Software Engineering", "Artificial Intelligence", "Data Science", "Computer Networks"],
                    "learning_objectives": [
                        "Develop proficiency in programming languages and software development",
                        "Understand fundamental algorithms and data structures",
                        "Design and analyze complex software systems",
                        "Apply computer science principles to solve real-world problems"
                    ],
                    "career_prospects": [
                        {
                            "title": "Software Engineer",
                            "description": "Design, develop, and maintain software applications",
                            "salary_range": "$70,000 - $120,000",
                            "companies": ["Google", "Microsoft", "Amazon", "Facebook"]
                        },
                        {
                            "title": "Data Scientist",
                            "description": "Analyze and interpret complex data to inform business decisions",
                            "salary_range": "$80,000 - $130,000",
                            "companies": ["IBM", "Netflix", "Uber", "Airbnb"]
                        }
                    ]
                },
                {
                    "title": "Master of Science in Computer Science",
                    "level": "Graduate",
                    "duration": "2 years",
                    "short_description": "An advanced program focusing on specialized areas of computer science.",
                    "description": "The Master of Science in Computer Science program at the University of Dhaka is designed for students who want to deepen their knowledge in specific areas of computer science. The program offers specializations in artificial intelligence, data science, cybersecurity, and more.",
                    "specializations": ["Artificial Intelligence", "Machine Learning", "Cybersecurity", "Big Data Analytics"],
                    "learning_objectives": [
                        "Develop advanced knowledge in specialized areas of computer science",
                        "Conduct original research in computer science",
                        "Apply advanced algorithms and techniques to solve complex problems",
                        "Develop critical thinking and problem-solving skills"
                    ],
                    "career_prospects": [
                        {
                            "title": "Machine Learning Engineer",
                            "description": "Design and implement machine learning models and systems",
                            "salary_range": "$90,000 - $150,000",
                            "companies": ["Google AI", "OpenAI", "DeepMind", "NVIDIA"]
                        },
                        {
                            "title": "Research Scientist",
                            "description": "Conduct research to advance the field of computer science",
                            "salary_range": "$100,000 - $160,000",
                            "companies": ["Microsoft Research", "IBM Research", "Facebook AI Research"]
                        }
                    ]
                },
                {
                    "title": "Doctor of Philosophy in Computer Science",
                    "level": "Postgraduate",
                    "duration": "3-5 years",
                    "short_description": "A research-focused program for those seeking to contribute to the advancement of computer science.",
                    "description": "The Doctor of Philosophy in Computer Science program at the University of Dhaka is designed for students who want to pursue advanced research in computer science. The program focuses on original research contributions to the field.",
                    "specializations": ["Theoretical Computer Science", "Advanced AI", "Quantum Computing", "Computational Biology"],
                    "learning_objectives": [
                        "Conduct original research that advances the field of computer science",
                        "Develop expertise in a specialized area of computer science",
                        "Contribute to the academic community through publications and presentations",
                        "Develop skills in teaching and mentoring"
                    ],
                    "career_prospects": [
                        {
                            "title": "Professor",
                            "description": "Teach and conduct research at universities",
                            "salary_range": "$80,000 - $150,000",
                            "companies": ["Top Universities Worldwide"]
                        },
                        {
                            "title": "Research Scientist",
                            "description": "Lead research teams in industry or academia",
                            "salary_range": "$120,000 - $200,000",
                            "companies": ["Google Brain", "DeepMind", "Microsoft Research"]
                        }
                    ]
                }
            ]
            
            # Add programs to database
            for program_data in programs_data:
                program = Program(
                    title=program_data["title"],
                    level=program_data["level"],
                    duration=program_data["duration"],
                    short_description=program_data["short_description"],
                    description=program_data["description"],
                    specializations=program_data["specializations"],
                    learning_objectives=program_data["learning_objectives"],
                    career_prospects=program_data["career_prospects"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(program)
                db.commit()
                db.refresh(program)
                print(f"Added program: {program.title}")
            
            print(f"Added {len(programs_data)} programs")
            
            # Now add courses for the BSc program
            bsc_program = db.query(Program).filter(Program.level == "Undergraduate").first()
            
            if bsc_program:
                # Sample course data for BSc program
                courses_data = [
                    {
                        "code": "CSE 1101",
                        "title": "Introduction to Programming",
                        "description": "An introduction to programming concepts and techniques using a high-level language. Topics include variables, data types, control structures, functions, and basic algorithms.",
                        "credits": 3,
                        "duration": "1 semester",
                        "difficulty": "Beginner",
                        "prerequisites": [],
                        "specialization": "Core",
                        "semester": 1,
                        "year": 1
                    },
                    {
                        "code": "CSE 1102",
                        "title": "Introduction to Computer Systems",
                        "description": "An overview of computer systems, including hardware components, operating systems, and basic networking concepts.",
                        "credits": 3,
                        "duration": "1 semester",
                        "difficulty": "Beginner",
                        "prerequisites": [],
                        "specialization": "Core",
                        "semester": 1,
                        "year": 1
                    },
                    {
                        "code": "CSE 2201",
                        "title": "Data Structures",
                        "description": "Study of fundamental data structures and their applications. Topics include arrays, linked lists, stacks, queues, trees, and graphs.",
                        "credits": 4,
                        "duration": "1 semester",
                        "difficulty": "Intermediate",
                        "prerequisites": ["CSE 1101"],
                        "specialization": "Core",
                        "semester": 1,
                        "year": 2
                    },
                    {
                        "code": "CSE 2202",
                        "title": "Algorithms",
                        "description": "Design and analysis of algorithms. Topics include sorting, searching, graph algorithms, and algorithm complexity.",
                        "credits": 4,
                        "duration": "1 semester",
                        "difficulty": "Intermediate",
                        "prerequisites": ["CSE 2201"],
                        "specialization": "Core",
                        "semester": 2,
                        "year": 2
                    },
                    {
                        "code": "CSE 3301",
                        "title": "Database Systems",
                        "description": "Introduction to database concepts, design, and implementation. Topics include relational model, SQL, normalization, and transaction processing.",
                        "credits": 3,
                        "duration": "1 semester",
                        "difficulty": "Intermediate",
                        "prerequisites": ["CSE 2201"],
                        "specialization": "Software Engineering",
                        "semester": 1,
                        "year": 3
                    },
                    {
                        "code": "CSE 3302",
                        "title": "Artificial Intelligence",
                        "description": "Introduction to artificial intelligence concepts and techniques. Topics include search algorithms, knowledge representation, and machine learning.",
                        "credits": 3,
                        "duration": "1 semester",
                        "difficulty": "Advanced",
                        "prerequisites": ["CSE 2202"],
                        "specialization": "Artificial Intelligence",
                        "semester": 2,
                        "year": 3
                    },
                    {
                        "code": "CSE 4401",
                        "title": "Machine Learning",
                        "description": "Study of algorithms and statistical models that enable computer systems to learn from data. Topics include supervised and unsupervised learning, neural networks, and deep learning.",
                        "credits": 4,
                        "duration": "1 semester",
                        "difficulty": "Advanced",
                        "prerequisites": ["CSE 3302"],
                        "specialization": "Artificial Intelligence",
                        "semester": 1,
                        "year": 4
                    },
                    {
                        "code": "CSE 4402",
                        "title": "Software Engineering",
                        "description": "Principles and practices of software engineering. Topics include requirements analysis, design, testing, and project management.",
                        "credits": 3,
                        "duration": "1 semester",
                        "difficulty": "Advanced",
                        "prerequisites": ["CSE 3301"],
                        "specialization": "Software Engineering",
                        "semester": 2,
                        "year": 4
                    }
                ]
                
                # Add courses to database
                for course_data in courses_data:
                    course = Course(
                        code=course_data["code"],
                        title=course_data["title"],
                        description=course_data["description"],
                        credits=course_data["credits"],
                        duration=course_data["duration"],
                        difficulty=course_data["difficulty"],
                        prerequisites=course_data["prerequisites"],
                        specialization=course_data["specialization"],
                        semester=course_data["semester"],
                        year=course_data["year"],
                        program_id=bsc_program.id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(course)
                    db.commit()
                    db.refresh(course)
                    print(f"Added course: {course.code} - {course.title}")
                
                print(f"Added {len(courses_data)} courses for {bsc_program.title}")
            else:
                print("BSc program not found, skipping course creation")
                
        else:
            print(f"Found {existing_programs} existing programs, skipping sample data creation")
            
    except Exception as e:
        print(f"Error setting up program data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_programs()
