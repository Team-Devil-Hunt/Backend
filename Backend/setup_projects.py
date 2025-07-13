from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Project, ProjectCategory, ProjectType, User, Role
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid
import random
from config import settings

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_projects_table():
    # Create the projects table
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have projects data
        existing_projects = db.query(Project).count()
        
        # Check if faculty role exists for supervisor reference
        faculty_role = db.query(Role).filter(Role.name == "FACULTY").first()
        if not faculty_role:
            faculty_role = Role(name="FACULTY")
            db.add(faculty_role)
            db.commit()
            db.refresh(faculty_role)
        
        # Create a single faculty user if none exists
        faculty_user = db.query(User).filter(User.role_id == faculty_role.id).first()
        
        if not faculty_user:
            # Create a faculty user
            faculty_user = User(
                name="Dr. Palash Roy",
                email="palash.roy@cse.du.ac.bd",
                password="hashed_password",  # In a real scenario, this would be properly hashed
                role_id=faculty_role.id
            )
            db.add(faculty_user)
            db.commit()
            db.refresh(faculty_user)
        
        if existing_projects == 0 and faculty_user:
            print("Adding sample projects...")
            
            # Current date for reference
            now = datetime.utcnow()
            
            # Sample projects
            projects = [
                {
                    "title": "Smart Campus Navigation System",
                    "summary": "An AI-powered mobile app that helps students navigate the campus using AR and real-time location tracking.",
                    "abstract": "The Smart Campus Navigation System is an innovative mobile application designed to enhance the campus experience for students and visitors. Using augmented reality (AR) technology and real-time GPS tracking, the app provides turn-by-turn navigation within the university premises.\n\nThe system incorporates machine learning algorithms to optimize routes based on real-time crowd density, weather conditions, and user preferences. It features indoor navigation for complex buildings, integration with class schedules, and accessibility options for students with disabilities.\n\nThe app also includes social features allowing students to share locations, find study groups, and discover campus events. The backend utilizes a microservices architecture deployed on AWS, ensuring scalability and reliability.",
                    "supervisor_id": faculty_user.id,
                    "year": 2024,
                    "category": ProjectCategory.MOBILE_APP,
                    "type": ProjectType.STUDENT,
                    "tags": ["mobile app", "augmented reality", "navigation", "AI", "GPS"],
                    "team": [
                        {"name": "Anik Rahman", "role": "Team Lead & AR Developer"},
                        {"name": "Fahmida Akter", "role": "Backend Developer"},
                        {"name": "Tanvir Ahmed", "role": "UI/UX Designer"},
                        {"name": "Nusrat Jahan", "role": "ML Engineer"}
                    ],
                    "course": "CSE 4000: Final Year Project",
                    "team_size": 4,
                    "completion_date": now - timedelta(days=30),
                    "technologies": ["Flutter", "ARCore", "Firebase", "TensorFlow", "Node.js"],
                    "key_features": [
                        "AR-based navigation",
                        "Indoor positioning",
                        "Crowd density prediction",
                        "Accessibility routes",
                        "Social features"
                    ],
                    "achievements": [
                        "1st Prize at DU Tech Fest 2024",
                        "Selected for Google Solution Challenge"
                    ],
                    "demo_link": "https://campus-nav.demo.bd",
                    "github_link": "https://github.com/csedu/campus-navigation",
                    "contact_email": "anik.rahman@example.com"
                },
                {
                    "title": "Code Quality Analysis Tool",
                    "summary": "A static code analysis tool that automatically detects code smells, potential bugs, and security vulnerabilities in Java applications.",
                    "abstract": "This project presents a comprehensive static code analysis tool designed to improve code quality in Java applications. The tool automatically identifies code smells, potential bugs, security vulnerabilities, and performance issues by analyzing source code without execution.\n\nThe system employs abstract syntax tree (AST) parsing and pattern matching to detect problematic code patterns. It implements over 200 rules covering various aspects of code quality including maintainability, reliability, security, and performance.\n\nThe tool integrates with popular IDEs and CI/CD pipelines, providing real-time feedback to developers. It also generates detailed reports with suggestions for improvement and code examples.",
                    "supervisor_id": faculty_user.id,
                    "year": 2023,
                    "category": ProjectCategory.ALGORITHMS,
                    "type": ProjectType.FACULTY,
                    "tags": ["static analysis", "code quality", "Java", "security", "performance"],
                    "team": [
                        {"name": "Dr. Ismat Rahman", "role": "Principal Investigator"},
                        {"name": "Md. Karim", "role": "Research Assistant"},
                        {"name": "Sadia Islam", "role": "Research Assistant"}
                    ],
                    "team_size": 3,
                    "completion_date": now - timedelta(days=180),
                    "technologies": ["Java", "ANTLR", "JavaParser", "Spring Boot", "React"],
                    "key_features": [
                        "200+ code quality rules",
                        "IDE integration",
                        "CI/CD pipeline support",
                        "Performance optimization suggestions",
                        "Git integration",
                        "Automated report generation",
                        "Custom rule configuration"
                    ],
                    "achievements": [
                        "Published in IEEE Software Journal",
                        "Adopted by 3 local software companies",
                        "Open-sourced with 500+ GitHub stars"
                    ],
                    "github_link": "https://github.com/ismat-rahman/code-analyzer",
                    "paper_link": "https://doi.org/10.1109/software.2023.1234567",
                    "contact_email": "ismat.rahman@cse.du.ac.bd"
                },
                {
                    "title": "Blockchain-based E-voting System",
                    "summary": "A secure and transparent electronic voting system built on blockchain technology to ensure election integrity.",
                    "abstract": "This project develops a secure, transparent, and tamper-proof digital voting system using blockchain technology to address concerns about election integrity and accessibility.\n\nThe system implements a permissioned blockchain network where each vote is recorded as an immutable transaction. Advanced cryptographic techniques ensure voter privacy while maintaining transparency and auditability.\n\nThe platform includes voter registration, identity verification, secure ballot casting, and real-time result tabulation. Smart contracts automate the voting process and ensure compliance with electoral rules.",
                    "supervisor_id": faculty_user.id,
                    "year": 2024,
                    "category": ProjectCategory.SECURITY,
                    "type": ProjectType.FACULTY,
                    "tags": ["blockchain", "e-voting", "security", "cryptography", "smart contracts"],
                    "team": [
                        {"name": "Prof. Shahida Sultana", "role": "Principal Investigator"},
                        {"name": "Dr. Kamal Hossain", "role": "Co-Investigator"},
                        {"name": "Arif Khan", "role": "PhD Researcher"},
                        {"name": "Maliha Rahman", "role": "Masters Researcher"}
                    ],
                    "team_size": 4,
                    "completion_date": now - timedelta(days=90),
                    "technologies": ["Hyperledger Fabric", "Solidity", "React", "Node.js", "Zero-knowledge proofs"],
                    "key_features": [
                        "Immutable vote recording",
                        "Voter anonymity",
                        "Real-time result verification",
                        "Distributed consensus",
                        "Audit trail",
                        "Resistance to DDoS attacks"
                    ],
                    "achievements": [
                        "Pilot implementation in University Student Council elections",
                        "Research grant from ICT Division, Bangladesh",
                        "Best Paper Award at International Conference on Blockchain Technology 2024"
                    ],
                    "demo_link": "https://evoting-blockchain.demo.bd",
                    "github_link": "https://github.com/shahida-sultana/blockchain-voting",
                    "paper_link": "https://doi.org/10.1145/blockchain.2024.7654321",
                    "contact_email": "shahida.sultana@cse.du.ac.bd"
                },
                {
                    "title": "Real-time Bangla Sign Language Recognition",
                    "summary": "An AI system that recognizes Bangla sign language gestures in real-time using computer vision and deep learning.",
                    "abstract": "This project develops a real-time Bangla sign language recognition system to bridge the communication gap between the hearing-impaired community and the general public in Bangladesh.\n\nThe system uses computer vision techniques and deep learning models to recognize and interpret Bangla sign language gestures captured through a webcam or smartphone camera. It can recognize over 200 common Bangla signs with high accuracy.\n\nThe application provides real-time translation of sign language to text and speech in Bangla. It also includes a learning module to help users learn Bangla sign language through interactive tutorials.",
                    "supervisor_id": faculty_user.id,
                    "year": 2023,
                    "category": ProjectCategory.MACHINE_LEARNING,
                    "type": ProjectType.STUDENT,
                    "tags": ["sign language", "computer vision", "deep learning", "accessibility", "Bangla"],
                    "team": [
                        {"name": "Tasnim Akter", "role": "Team Lead & ML Engineer"},
                        {"name": "Rafiq Islam", "role": "Computer Vision Specialist"},
                        {"name": "Sabina Yasmin", "role": "Mobile Developer"}
                    ],
                    "course": "CSE 4000: Final Year Project",
                    "team_size": 3,
                    "completion_date": now - timedelta(days=365),
                    "technologies": ["TensorFlow", "OpenCV", "MediaPipe", "Flutter", "Python"],
                    "key_features": [
                        "Real-time recognition",
                        "200+ Bangla signs",
                        "Text and speech output",
                        "Interactive learning module",
                        "Works in various lighting conditions"
                    ],
                    "achievements": [
                        "National ICT Award 2023",
                        "Implemented in 5 schools for hearing-impaired students",
                        "Featured in The Daily Star"
                    ],
                    "demo_link": "https://bsl-recognition.demo.bd",
                    "github_link": "https://github.com/tasnim/bangla-sign-language",
                    "contact_email": "tasnim.akter@example.com"
                },
                {
                    "title": "Advanced Graphics Rendering Engine",
                    "summary": "A high-performance 3D graphics rendering engine with support for ray tracing, global illumination, and physically-based materials.",
                    "abstract": "This project presents an advanced 3D graphics rendering engine designed for both real-time applications and offline rendering. The engine implements state-of-the-art rendering techniques including ray tracing, path tracing, and photon mapping to achieve photorealistic image quality.\n\nThe system features a physically-based material system, advanced lighting models, and support for complex scenes with millions of polygons. It utilizes GPU acceleration through Vulkan and CUDA to achieve high performance.\n\nThe engine includes a node-based material editor, scene organization tools, and a comprehensive API for integration with games and visualization applications.",
                    "supervisor_id": faculty_user.id,
                    "year": 2024,
                    "category": ProjectCategory.GRAPHICS,
                    "type": ProjectType.FACULTY,
                    "tags": ["graphics", "rendering", "ray tracing", "GPU", "game engine"],
                    "team": [
                        {"name": "Dr. Farhan Ahmed", "role": "Principal Investigator"},
                        {"name": "Imran Khan", "role": "Graphics Programmer"},
                        {"name": "Nadia Islam", "role": "GPGPU Specialist"},
                        {"name": "Omar Farooq", "role": "Research Assistant"}
                    ],
                    "team_size": 4,
                    "completion_date": now - timedelta(days=120),
                    "technologies": ["C++", "Vulkan", "CUDA", "OpenGL", "DirectX"],
                    "key_features": [
                        "Path tracing",
                        "Real-time global illumination",
                        "Physically-based materials",
                        "Volumetric lighting",
                        "Particle systems",
                        "Post-processing effects",
                        "Animation system"
                    ],
                    "achievements": [
                        "Presented at SIGGRAPH Asia 2024",
                        "Used in 3 commercial games",
                        "Open-source with active community"
                    ],
                    "demo_link": "https://graphics-engine.demo.bd",
                    "github_link": "https://github.com/farhan-ahmed/advanced-graphics-engine",
                    "paper_link": "https://doi.org/10.1145/siggraph.2024.9876543",
                    "contact_email": "farhan.ahmed@cse.du.ac.bd"
                }
            ]
            
            # Add projects to database
            for project_data in projects:
                project = Project(**project_data)
                db.add(project)
            
            db.commit()
            
            print("Sample projects added successfully!")
        else:
            print("Projects table already has data or no faculty users available. Skipping sample data creation.")
            
    except Exception as e:
        print(f"Error setting up projects table: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_projects_table()
