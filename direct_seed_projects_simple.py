import psycopg2
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

# Database connection parameters
DB_USERNAME = os.environ.get("DATABASE_USERNAME")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DB_HOSTNAME = os.environ.get("DATABASE_HOSTNAME")
DB_PORT = os.environ.get("DATABASE_PORT")
DB_NAME = os.environ.get("DATABASE_NAME")

print(f"Connecting to database {DB_NAME} at {DB_HOSTNAME}:{DB_PORT} as {DB_USERNAME}")

# Connect to the database
conn = psycopg2.connect(
    host=DB_HOSTNAME,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD
)

# Create a cursor
cur = conn.cursor()

# Check if users table exists and get its structure
try:
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")
    user_columns = [row[0] for row in cur.fetchall()]
    print(f"User table columns: {user_columns}")
    
    # Check if we have user_type or role column
    role_column = 'user_type' if 'user_type' in user_columns else 'role' if 'role' in user_columns else None
    
    if role_column:
        # Get faculty users
        cur.execute(f"SELECT id, name, email FROM users WHERE {role_column} = 'FACULTY' LIMIT 10")
        faculty_users = cur.fetchall()
    else:
        # Just get some users if we can't filter by role
        cur.execute("SELECT id, name, email FROM users LIMIT 10")
        faculty_users = cur.fetchall()
    
    print(f"Found {len(faculty_users)} users to use as supervisors")
    
    if not faculty_users:
        print("No users found. Creating sample faculty users...")
        # Create some sample faculty users if none exist
        faculty_names = [
            ("Dr. Mahmuda Naznin", "mahmuda@cse.du.ac.bd"),
            ("Dr. Syed Monowar Hossain", "monowar@cse.du.ac.bd"),
            ("Dr. Md. Abdur Rahman", "arahman@cse.du.ac.bd"),
            ("Dr. Md. Shariful Islam", "shariful@cse.du.ac.bd"),
            ("Prof. Aminul Haque", "aminul@cse.du.ac.bd")
        ]
        
        faculty_users = []
        # Construct the INSERT statement based on available columns
        if 'user_type' in user_columns:
            role_insert = ", user_type"
            role_value = ", 'FACULTY'"
        elif 'role' in user_columns:
            role_insert = ", role"
            role_value = ", 'FACULTY'"
        else:
            role_insert = ""
            role_value = ""
            
        for name, email in faculty_names:
            cur.execute(f"""
                INSERT INTO users (name, email{role_insert}, created_at, updated_at)
                VALUES (%s, %s{role_value}, %s, %s)
                RETURNING id, name, email
            """, (name, email, datetime.now(), datetime.now()))
            faculty_users.append(cur.fetchone())
        
        conn.commit()
        print(f"Created {len(faculty_users)} faculty users")

except Exception as e:
    print(f"Error getting users: {e}")
    # Create a temporary users table if needed
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            user_type VARCHAR DEFAULT 'FACULTY',
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
        """)
        conn.commit()
        print("Created users table")
        
        # Add some faculty users
        faculty_names = [
            ("Dr. Mahmuda Naznin", "mahmuda@cse.du.ac.bd"),
            ("Dr. Syed Monowar Hossain", "monowar@cse.du.ac.bd"),
            ("Dr. Md. Abdur Rahman", "arahman@cse.du.ac.bd"),
            ("Dr. Md. Shariful Islam", "shariful@cse.du.ac.bd"),
            ("Prof. Aminul Haque", "aminul@cse.du.ac.bd")
        ]
        
        faculty_users = []
        for name, email in faculty_names:
            cur.execute("""
                INSERT INTO users (name, email, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, email
            """, (name, email, datetime.now(), datetime.now()))
            faculty_users.append(cur.fetchone())
        
        conn.commit()
        print(f"Created {len(faculty_users)} faculty users")
    except Exception as e:
        print(f"Error creating users table: {e}")
        # If we can't create users, create some dummy faculty data
        faculty_users = [(1, "Dr. Mahmuda Naznin", "mahmuda@cse.du.ac.bd")]

# Sample project data
projects = [
    {
        "title": "Smart Campus Navigation System",
        "summary": "An AI-powered mobile app that helps students navigate the campus using AR and real-time location tracking.",
        "abstract": "The Smart Campus Navigation System is an innovative mobile application designed to enhance the campus experience for students and visitors. Using augmented reality (AR) technology and real-time GPS tracking, the app provides turn-by-turn navigation within the university premises.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2024,
        "category": "mobile_app",
        "type": "student",
        "tags": ["React Native", "AR", "Machine Learning", "AWS", "GPS"],
        "team": [
            {"name": "Fahim Rahman", "role": "Team Lead"},
            {"name": "Sadia Islam", "role": "Frontend Developer"},
            {"name": "Arif Hassan", "role": "Backend Developer"},
            {"name": "Nusrat Jahan", "role": "UI/UX Designer"}
        ],
        "course": "CSE 4000 - Final Year Project",
        "team_size": 4,
        "completion_date": "2024-05-15",
        "technologies": ["React Native", "Node.js", "MongoDB", "AWS Lambda", "ARCore", "ARKit"],
        "key_features": [
            "Augmented Reality navigation overlay",
            "Real-time crowd density analysis",
            "Indoor positioning system",
            "Class schedule integration",
            "Accessibility features for disabled users",
            "Social location sharing"
        ],
        "achievements": [
            "Winner - Best Innovation Award 2024",
            "Featured in University Tech Showcase",
            "Deployed for campus-wide use"
        ],
        "demo_link": "https://demo.smartcampus.edu",
        "github_link": "https://github.com/csedu/smart-campus"
    },
    {
        "title": "Automated Code Review Assistant",
        "summary": "ML-powered tool that analyzes code quality, detects bugs, and suggests improvements using natural language processing.",
        "abstract": "The Automated Code Review Assistant is a sophisticated machine learning system designed to enhance software development workflows by providing intelligent code analysis and review suggestions.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2024,
        "category": "machine_learning",
        "type": "faculty",
        "tags": ["NLP", "Static Analysis", "Transformers", "DevOps"],
        "team": None,
        "course": None,
        "team_size": None,
        "completion_date": "2024-03-20",
        "technologies": ["Python", "PyTorch", "BERT", "FastAPI", "Docker", "PostgreSQL"],
        "key_features": [
            "Multi-language code analysis",
            "Security vulnerability detection",
            "Performance optimization suggestions",
            "Git integration",
            "Automated report generation",
            "Custom rule configuration"
        ],
        "achievements": [
            "Published in IEEE Software Engineering Conference",
            "Adopted by 5+ tech companies",
            "Open-sourced with 2000+ GitHub stars"
        ],
        "demo_link": "https://codereview.ai/demo",
        "github_link": "https://github.com/csedu/code-review-ai",
        "paper_link": "https://ieeexplore.ieee.org/document/code-review-2024",
        "contact_email": None  # Will be filled with faculty email
    },
    {
        "title": "E-Learning Platform for Programming",
        "summary": "Interactive web platform with coding challenges, automated grading, and personalized learning paths.",
        "abstract": "This comprehensive e-learning platform is designed to revolutionize programming education through interactive learning experiences and personalized instruction.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2023,
        "category": "web_development",
        "type": "student",
        "tags": ["React", "Node.js", "Education", "Gamification"],
        "team": [
            {"name": "Rakib Ahmed", "role": "Full Stack Developer"},
            {"name": "Tahmina Akter", "role": "Frontend Developer"},
            {"name": "Sabbir Rahman", "role": "Backend Developer"}
        ],
        "course": "CSE 3200 - Software Engineering",
        "team_size": 3,
        "completion_date": "2023-12-10",
        "technologies": ["React", "Node.js", "Express", "MongoDB", "Socket.io", "Docker"],
        "key_features": [
            "Interactive code editor",
            "Automated code testing",
            "Personalized learning paths",
            "Real-time collaboration",
            "Progress tracking",
            "Gamification system"
        ],
        "achievements": None,
        "demo_link": "https://codelearn.edu.bd",
        "github_link": "https://github.com/csedu/elearning-platform"
    },
    {
        "title": "IoT-Based Smart Agriculture System",
        "summary": "Sensor network for monitoring crop conditions with automated irrigation and pest detection using computer vision.",
        "abstract": "The IoT-Based Smart Agriculture System represents a cutting-edge approach to precision farming, combining Internet of Things sensors, machine learning, and automated control systems.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2023,
        "category": "iot",
        "type": "student",
        "tags": ["IoT", "Computer Vision", "Agriculture", "Sensors"],
        "team": [
            {"name": "Hasibul Islam", "role": "IoT Developer"},
            {"name": "Ruma Begum", "role": "ML Engineer"},
            {"name": "Kamal Uddin", "role": "Hardware Engineer"}
        ],
        "course": "CSE 4100 - Embedded Systems",
        "team_size": 3,
        "completion_date": "2023-11-25",
        "technologies": ["Arduino", "Raspberry Pi", "Python", "OpenCV", "MQTT", "InfluxDB"],
        "key_features": [
            "Multi-sensor environmental monitoring",
            "Computer vision crop analysis",
            "Automated irrigation control",
            "Weather prediction integration",
            "Mobile app for farmers",
            "Data analytics dashboard"
        ],
        "achievements": [
            "Winner - National IoT Competition 2023",
            "Pilot deployment in 3 farms"
        ],
        "demo_link": "https://smartfarm.iot.bd",
        "github_link": "https://github.com/csedu/smart-agriculture"
    },
    {
        "title": "Blockchain-Based Voting System",
        "summary": "Secure and transparent digital voting platform using blockchain technology with voter verification.",
        "abstract": "This project develops a secure, transparent, and tamper-proof digital voting system using blockchain technology to address concerns about election integrity and accessibility.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2024,
        "category": "security",
        "type": "faculty",
        "tags": ["Blockchain", "Cryptography", "Security", "Smart Contracts"],
        "team": None,
        "course": None,
        "team_size": None,
        "completion_date": "2024-01-30",
        "technologies": ["Ethereum", "Solidity", "Web3.js", "React", "IPFS", "MetaMask"],
        "key_features": [
            "Immutable vote recording",
            "Zero-knowledge voter verification",
            "Real-time result transparency",
            "Multi-device accessibility",
            "Audit trail generation",
            "Smart contract automation"
        ],
        "achievements": [
            "Published in ACM Digital Government Conference",
            "Pilot tested in student elections",
            "Patent application filed"
        ],
        "demo_link": "https://blockvote.demo.bd",
        "github_link": "https://github.com/csedu/blockchain-voting",
        "paper_link": "https://dl.acm.org/doi/blockchain-voting-2024",
        "contact_email": None  # Will be filled with faculty email
    }
]

# Check if projects table exists
try:
    cur.execute("SELECT COUNT(*) FROM projects")
    projects_count = cur.fetchone()[0]
    print(f"Found {projects_count} existing projects in the database")
except psycopg2.errors.UndefinedTable:
    print("Projects table does not exist. Creating it...")
    # Create the projects table if it doesn't exist
    cur.execute("""
    CREATE TABLE projects (
        id SERIAL PRIMARY KEY,
        title VARCHAR NOT NULL,
        summary VARCHAR NOT NULL,
        abstract TEXT NOT NULL,
        supervisor_id INTEGER REFERENCES users(id),
        year INTEGER NOT NULL,
        category VARCHAR NOT NULL,
        type VARCHAR NOT NULL,
        tags JSONB,
        team JSONB,
        course VARCHAR,
        team_size INTEGER,
        completion_date TIMESTAMP NOT NULL,
        technologies JSONB,
        key_features JSONB,
        achievements JSONB,
        demo_link VARCHAR,
        github_link VARCHAR,
        paper_link VARCHAR,
        contact_email VARCHAR,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL
    )
    """)
    conn.commit()
    print("Projects table created successfully")

# Insert projects into the database
inserted_count = 0
for project in projects:
    # Assign a random faculty supervisor
    faculty = random.choice(faculty_users)
    project["supervisor_id"] = faculty[0]
    
    # For faculty projects, use the faculty's email as contact
    if project["type"] == "faculty" and len(faculty) > 2:
        project["contact_email"] = faculty[2]
    else:
        project["contact_email"] = None
    
    # Convert datetime strings to datetime objects
    if isinstance(project["completion_date"], str):
        project["completion_date"] = datetime.strptime(project["completion_date"], "%Y-%m-%d")
    
    # Convert JSON fields to JSON strings
    for field in ["tags", "team", "technologies", "key_features", "achievements"]:
        if project[field] is not None:
            project[field] = json.dumps(project[field])
    
    # Add paper_link if it doesn't exist
    if "paper_link" not in project:
        project["paper_link"] = None
    
    # Insert the project
    try:
        # Check if the projects table has all the fields we need
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'projects'")
        project_columns = [row[0] for row in cur.fetchall()]
        
        # Build dynamic SQL based on available columns
        columns = []
        values = []
        params = []
        
        # Map our data to available columns
        field_mapping = {
            "title": project["title"],
            "summary": project["summary"],
            "abstract": project["abstract"],
            "supervisor_id": project["supervisor_id"],
            "year": project["year"],
            "category": project["category"],
            "type": project["type"],
            "tags": project["tags"],
            "team": project["team"],
            "course": project["course"],
            "team_size": project["team_size"],
            "completion_date": project["completion_date"],
            "technologies": project["technologies"],
            "key_features": project["key_features"],
            "achievements": project["achievements"],
            "demo_link": project["demo_link"],
            "github_link": project["github_link"],
            "paper_link": project["paper_link"],
            "contact_email": project["contact_email"],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Only include columns that exist in the database
        for col, val in field_mapping.items():
            if col in project_columns:
                columns.append(col)
                values.append(f"%s")
                params.append(val)
        
        # Build and execute the SQL
        sql = f"INSERT INTO projects ({', '.join(columns)}) VALUES ({', '.join(values)})"
        cur.execute(sql, params)
        inserted_count += 1
        print(f"Inserted project: {project['title']}")
    except Exception as e:
        print(f"Error inserting project {project['title']}: {e}")
        conn.rollback()
        continue

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print(f"Successfully inserted {inserted_count} projects into the database.")
