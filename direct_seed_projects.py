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

# First, get some faculty users to use as supervisors
cur.execute("SELECT id, name, email FROM users WHERE role = 'FACULTY' LIMIT 10")
faculty_users = cur.fetchall()

if not faculty_users:
    print("No faculty users found. Please seed users first.")
    conn.close()
    exit(1)

# Project categories and types
categories = [
    "machine_learning", "web_development", "mobile_app", "algorithms", 
    "iot", "security", "robotics", "graphics"
]

project_types = ["student", "faculty"]

# Sample project data
projects = [
    {
        "title": "Smart Campus Navigation System",
        "summary": "An AI-powered mobile app that helps students navigate the campus using AR and real-time location tracking.",
        "abstract": "The Smart Campus Navigation System is an innovative mobile application designed to enhance the campus experience for students and visitors. Using augmented reality (AR) technology and real-time GPS tracking, the app provides turn-by-turn navigation within the university premises.\n\nThe system incorporates machine learning algorithms to optimize routes based on real-time crowd density, weather conditions, and user preferences. It features indoor navigation for complex buildings, integration with class schedules, and accessibility options for students with disabilities.\n\nThe app also includes social features allowing students to share locations, find study groups, and discover campus events. The backend utilizes a microservices architecture deployed on AWS, ensuring scalability and reliability.",
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
        "abstract": "The Automated Code Review Assistant is a sophisticated machine learning system designed to enhance software development workflows by providing intelligent code analysis and review suggestions.\n\nThe system employs advanced natural language processing techniques and static code analysis to identify potential bugs, security vulnerabilities, code smells, and performance issues. It supports multiple programming languages including Python, Java, JavaScript, and C++.\n\nThe tool integrates seamlessly with popular version control systems like Git and provides detailed reports with actionable recommendations. It uses transformer-based models fine-tuned on large codebases to understand context and provide human-like review comments.",
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
        "abstract": "This comprehensive e-learning platform is designed to revolutionize programming education through interactive learning experiences and personalized instruction.\n\nThe platform features an integrated code editor with real-time syntax highlighting, automated testing, and instant feedback. Students can progress through carefully curated learning paths that adapt to their skill level and learning pace.\n\nThe system includes gamification elements, peer collaboration tools, and detailed analytics for both students and instructors. It supports multiple programming languages and integrates with popular development tools.",
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
        "abstract": "The IoT-Based Smart Agriculture System represents a cutting-edge approach to precision farming, combining Internet of Things sensors, machine learning, and automated control systems.\n\nThe system deploys a network of environmental sensors throughout agricultural fields to monitor soil moisture, temperature, humidity, light levels, and nutrient content. Computer vision algorithms analyze crop images to detect diseases, pests, and growth patterns.\n\nAutomated irrigation systems respond to real-time data, optimizing water usage and crop yield. The platform provides farmers with a comprehensive dashboard and mobile app for remote monitoring and control.",
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
        "abstract": "This project develops a secure, transparent, and tamper-proof digital voting system using blockchain technology to address concerns about election integrity and accessibility.\n\nThe system implements a permissioned blockchain network where each vote is recorded as an immutable transaction. Advanced cryptographic techniques ensure voter privacy while maintaining transparency and auditability.\n\nThe platform includes voter registration, identity verification, secure ballot casting, and real-time result tabulation. Smart contracts automate the voting process and ensure compliance with electoral rules.",
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
    },
    {
        "title": "Autonomous Drone Delivery System",
        "summary": "AI-powered drone fleet for package delivery with obstacle avoidance and route optimization.",
        "abstract": "The Autonomous Drone Delivery System is an innovative logistics solution that leverages artificial intelligence and robotics to create an efficient package delivery network.\n\nThe system features a fleet of autonomous drones equipped with computer vision, GPS navigation, and obstacle avoidance capabilities. Machine learning algorithms optimize delivery routes based on weather conditions, air traffic, and package priorities.\n\nThe platform includes a comprehensive management system for tracking deliveries, managing drone maintenance, and coordinating with ground operations. Safety protocols ensure compliance with aviation regulations.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2023,
        "category": "robotics",
        "type": "student",
        "tags": ["Robotics", "Computer Vision", "Path Planning", "Drones"],
        "team": [
            {"name": "Imran Hossain", "role": "Robotics Engineer"},
            {"name": "Nasir Ahmed", "role": "AI Developer"},
            {"name": "Salma Khatun", "role": "Systems Engineer"}
        ],
        "course": "CSE 4200 - Robotics and Automation",
        "team_size": 3,
        "completion_date": "2023-10-15",
        "technologies": ["ROS", "OpenCV", "Python", "TensorFlow", "GPS", "Lidar"],
        "key_features": [
            "Autonomous flight control",
            "Real-time obstacle detection",
            "Dynamic route optimization",
            "Package tracking system",
            "Weather adaptation",
            "Emergency landing protocols"
        ],
        "achievements": [
            "Best Project Award - Robotics Fair 2023",
            "Successful test flights completed"
        ],
        "demo_link": "https://dronedelivery.demo.bd",
        "github_link": "https://github.com/csedu/drone-delivery"
    },
    {
        "title": "Real-time 3D Graphics Engine",
        "summary": "High-performance graphics engine with advanced rendering techniques and physics simulation.",
        "abstract": "This project develops a sophisticated real-time 3D graphics engine capable of rendering complex scenes with advanced lighting, shadows, and physics simulation.\n\nThe engine implements modern rendering techniques including physically-based rendering (PBR), screen-space reflections, and volumetric lighting. It features an efficient scene graph system and supports multiple rendering APIs.\n\nThe engine includes a comprehensive physics system for realistic object interactions, particle effects, and fluid simulation. It provides tools for content creation and supports popular 3D model formats.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2024,
        "category": "graphics",
        "type": "faculty",
        "tags": ["Graphics", "OpenGL", "Physics", "Rendering"],
        "team": None,
        "course": None,
        "team_size": None,
        "completion_date": "2024-02-28",
        "technologies": ["C++", "OpenGL", "GLSL", "Bullet Physics", "Assimp", "ImGui"],
        "key_features": [
            "Physically-based rendering",
            "Real-time global illumination",
            "Advanced shadow mapping",
            "Physics simulation",
            "Particle systems",
            "Multi-threading support"
        ],
        "achievements": [
            "Presented at SIGGRAPH Asia 2024",
            "Used in 3 commercial games",
            "Open-source with active community"
        ],
        "demo_link": "https://graphics-engine.demo.bd",
        "github_link": "https://github.com/csedu/3d-graphics-engine",
        "paper_link": "https://dl.acm.org/doi/graphics-engine-2024",
        "contact_email": None  # Will be filled with faculty email
    },
    {
        "title": "Efficient Graph Algorithms Library",
        "summary": "Optimized implementations of graph algorithms with parallel processing and memory efficiency.",
        "abstract": "This research project focuses on developing highly optimized implementations of fundamental graph algorithms with emphasis on parallel processing and memory efficiency.\n\nThe library includes implementations of shortest path algorithms, minimum spanning tree algorithms, network flow algorithms, and graph traversal methods. Each algorithm is optimized for different graph types and sizes.\n\nThe project explores novel parallelization strategies and memory-efficient data structures to handle large-scale graphs. Comprehensive benchmarking demonstrates significant performance improvements over existing libraries.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2023,
        "category": "algorithms",
        "type": "student",
        "tags": ["Algorithms", "Graph Theory", "Parallel Computing", "Optimization"],
        "team": [
            {"name": "Rafiq Islam", "role": "Algorithm Developer"},
            {"name": "Shirin Akter", "role": "Performance Analyst"}
        ],
        "course": "CSE 3100 - Data Structures and Algorithms",
        "team_size": 2,
        "completion_date": "2023-09-20",
        "technologies": ["C++", "OpenMP", "CUDA", "Python", "Boost Graph Library"],
        "key_features": [
            "Parallel algorithm implementations",
            "Memory-efficient data structures",
            "Support for large-scale graphs",
            "Comprehensive benchmarking suite",
            "Python bindings",
            "Detailed documentation"
        ],
        "achievements": [
            "50% performance improvement over standard libraries",
            "Adopted by research community"
        ],
        "github_link": "https://github.com/csedu/graph-algorithms"
    },
    {
        "title": "Natural Language Processing for Bangla",
        "summary": "Comprehensive NLP toolkit for Bangla language with sentiment analysis, named entity recognition, and text classification.",
        "abstract": "This project addresses the challenges of natural language processing for the Bangla language, developing a comprehensive toolkit to enable advanced text analysis and understanding.\n\nThe system includes modules for tokenization, part-of-speech tagging, named entity recognition, sentiment analysis, and text classification specifically optimized for Bangla. It incorporates transformer-based models trained on a large corpus of Bangla text collected from diverse sources.\n\nThe toolkit provides APIs for developers to integrate Bangla NLP capabilities into their applications. Extensive evaluation demonstrates state-of-the-art performance on multiple Bangla language tasks.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2023,
        "category": "machine_learning",
        "type": "faculty",
        "tags": ["NLP", "Bangla", "Transformers", "Language Processing"],
        "team": None,
        "course": None,
        "team_size": None,
        "completion_date": "2023-08-15",
        "technologies": ["Python", "PyTorch", "HuggingFace", "FastAPI", "MongoDB"],
        "key_features": [
            "Bangla tokenization",
            "Named entity recognition",
            "Sentiment analysis",
            "Text classification",
            "Machine translation",
            "Question answering"
        ],
        "achievements": [
            "Published in ACL Conference 2023",
            "Open-source with 500+ GitHub stars",
            "Integrated into multiple government applications"
        ],
        "demo_link": "https://bangla-nlp.csedu.ac.bd",
        "github_link": "https://github.com/csedu/bangla-nlp",
        "paper_link": "https://aclanthology.org/2023.acl-long.123",
        "contact_email": None  # Will be filled with faculty email
    },
    {
        "title": "Augmented Reality Educational Platform",
        "summary": "AR application for interactive learning of complex scientific concepts through 3D visualization.",
        "abstract": "The Augmented Reality Educational Platform transforms traditional learning by enabling students to interact with complex scientific concepts through immersive 3D visualizations.\n\nThe application allows users to visualize abstract concepts in physics, chemistry, biology, and mathematics through augmented reality overlays. Students can manipulate 3D models, observe simulations of scientific phenomena, and conduct virtual experiments.\n\nThe platform includes a content management system for educators to create custom AR learning modules. Analytics track student engagement and comprehension, providing insights for personalized learning.",
        "supervisor_id": None,  # Will be filled with actual faculty ID
        "year": 2024,
        "category": "mobile_app",
        "type": "student",
        "tags": ["AR", "Education", "3D Visualization", "Mobile"],
        "team": [
            {"name": "Tasnim Khan", "role": "AR Developer"},
            {"name": "Mahbub Rahman", "role": "3D Artist"},
            {"name": "Anika Hossain", "role": "Educational Content Developer"},
            {"name": "Zubair Ahmed", "role": "Mobile Developer"}
        ],
        "course": "CSE 4000 - Final Year Project",
        "team_size": 4,
        "completion_date": "2024-04-10",
        "technologies": ["Unity", "ARKit", "ARCore", "C#", "Blender", "Firebase"],
        "key_features": [
            "Interactive 3D models",
            "Scientific simulations",
            "Virtual experiments",
            "Content management system",
            "Learning analytics",
            "Offline content access"
        ],
        "achievements": [
            "Winner - Educational Technology Award 2024",
            "Pilot implementation in 5 schools",
            "Featured in EdTech Magazine"
        ],
        "demo_link": "https://ar-edu.csedu.ac.bd",
        "github_link": "https://github.com/csedu/ar-education"
    }
]

# Insert projects into the database
inserted_count = 0
for project in projects:
    # Assign a random faculty supervisor
    faculty = random.choice(faculty_users)
    project["supervisor_id"] = faculty[0]
    
    # For faculty projects, use the faculty's email as contact
    if project["type"] == "faculty":
        project["contact_email"] = faculty[2]
    
    # Convert datetime strings to datetime objects
    if isinstance(project["completion_date"], str):
        project["completion_date"] = datetime.strptime(project["completion_date"], "%Y-%m-%d")
    
    # Convert JSON fields to JSON strings
    for field in ["tags", "team", "technologies", "key_features", "achievements"]:
        if project[field] is not None:
            project[field] = json.dumps(project[field])
    
    # Insert the project
    cur.execute("""
        INSERT INTO projects (
            title, summary, abstract, supervisor_id, year, category, type, 
            tags, team, course, team_size, completion_date, technologies, 
            key_features, achievements, demo_link, github_link, paper_link, 
            contact_email, created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        project["title"], project["summary"], project["abstract"], project["supervisor_id"],
        project["year"], project["category"], project["type"], project["tags"], project["team"],
        project["course"], project["team_size"], project["completion_date"], project["technologies"],
        project["key_features"], project["achievements"], project["demo_link"], project["github_link"],
        project["paper_link"], project["contact_email"], datetime.now(), datetime.now()
    ))
    inserted_count += 1

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print(f"Successfully inserted {inserted_count} projects into the database.")
