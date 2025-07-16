from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Award
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import settings

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_awards_table():
    # Create the awards table
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have awards data
        existing_awards = db.query(Award).count()
        
        if existing_awards == 0:
            print("Adding sample awards data...")
            
            # Sample awards data
            awards = [
                Award(
                    title="Outstanding Research Award in Artificial Intelligence",
                    description="Awarded for groundbreaking research in deep learning algorithms for medical image analysis, demonstrating significant improvements in early disease detection accuracy.",
                    details="This prestigious award recognizes exceptional contributions to the field of artificial intelligence research. The recipient demonstrated innovative approaches to medical image analysis using novel deep learning architectures that achieved a 27% improvement in early disease detection compared to previous methods.\n\nThe research has been implemented in several medical institutions and has already contributed to improved patient outcomes through earlier and more accurate diagnoses.",
                    recipient="Dr. Rashida Ahmed",
                    recipient_type="faculty",
                    year=2024,
                    type="award",
                    organization="Bangladesh Association for Computing Machinery",
                    department="Computer Science and Engineering",
                    categories=["AI", "Machine Learning", "Medical Imaging"]
                ),
                Award(
                    title="National Science Foundation Research Grant",
                    description="Received a substantial research grant for developing sustainable computing solutions that reduce energy consumption in data centers.",
                    details="This competitive grant funds a three-year research project focused on developing energy-efficient algorithms and hardware designs for modern data centers. The project aims to reduce carbon footprint while maintaining or improving computational performance.\n\nThe research includes novel approaches to dynamic resource allocation, thermal management, and workload scheduling that could reduce energy consumption by up to 40% in large-scale computing environments.",
                    recipient="Dr. Kamal Hossain",
                    recipient_type="faculty",
                    year=2023,
                    type="grant",
                    organization="National Science Foundation",
                    amount=1500000,
                    department="Computer Science and Engineering",
                    duration="3 years",
                    categories=["Green Computing", "Energy Efficiency", "Data Centers"]
                ),
                Award(
                    title="Microsoft Research Fellowship in Quantum Computing",
                    description="Prestigious fellowship awarded to support PhD research in quantum algorithms and their applications in cryptography.",
                    details="The Microsoft Research Fellowship provides full financial support for PhD studies and research, along with mentorship from Microsoft Research scientists. The fellowship recognizes exceptional promise in the field of quantum computing and encourages groundbreaking research that bridges theoretical computer science with practical applications.\n\nAs part of this fellowship, the recipient will have the opportunity to collaborate with Microsoft's Quantum Computing team and access to state-of-the-art quantum computing resources.",
                    recipient="Tanvir Ahmed",
                    recipient_type="student",
                    year=2023,
                    type="fellowship",
                    organization="Microsoft Research",
                    amount=120000,
                    duration="2 years",
                    department="Computer Science and Engineering",
                    categories=["Quantum Computing", "Cryptography", "Algorithms"]
                ),
                Award(
                    title="ACM SIGCHI Best Paper Award",
                    description="Recognized for outstanding contribution to human-computer interaction research with paper on accessible interface design for elderly users.",
                    details="This award recognizes the most influential paper presented at the ACM SIGCHI Conference on Human Factors in Computing Systems. The winning paper introduced novel methodologies for designing and evaluating user interfaces specifically tailored to elderly users with varying levels of technology familiarity and physical capabilities.\n\nThe research included extensive user studies with over 200 participants aged 65-90 and resulted in a set of design guidelines that have been adopted by several major technology companies for their accessibility initiatives.",
                    recipient="Dr. Ismat Rahman",
                    recipient_type="faculty",
                    year=2024,
                    type="publication",
                    organization="ACM Special Interest Group on Computer-Human Interaction",
                    department="Computer Science and Engineering",
                    categories=["HCI", "Accessibility", "User Interface Design"],
                    publications=["Rahman, I., et al. (2024). Designing for the Silver Generation: Adaptive Interfaces for Elderly Users. Proceedings of the ACM SIGCHI Conference on Human Factors in Computing Systems."],
                    link="https://doi.org/10.1145/3544548.3581496"
                ),
                Award(
                    title="Google PhD Fellowship in Machine Learning",
                    description="Awarded to support doctoral research in reinforcement learning for autonomous systems in complex environments.",
                    details="The Google PhD Fellowship recognizes outstanding graduate students doing exceptional work in computer science and related disciplines. This particular fellowship supports cutting-edge research in reinforcement learning algorithms that enable autonomous systems to navigate and make decisions in complex, unpredictable environments.\n\nThe fellowship provides full financial support for PhD studies, as well as mentorship from Google researchers and opportunities to collaborate with Google's AI teams.",
                    recipient="Nusrat Jahan",
                    recipient_type="student",
                    year=2022,
                    type="fellowship",
                    organization="Google Research",
                    amount=150000,
                    duration="3 years",
                    department="Computer Science and Engineering",
                    categories=["Machine Learning", "Reinforcement Learning", "Autonomous Systems"]
                ),
                Award(
                    title="IEEE Cybersecurity Innovation Award",
                    description="Honored for developing a novel intrusion detection system that combines behavioral analytics with machine learning to identify zero-day attacks.",
                    details="This award recognizes innovative contributions to the field of cybersecurity that demonstrate significant potential for real-world impact. The winning project developed a hybrid intrusion detection system that achieved a 94% detection rate for previously unknown (zero-day) attacks while maintaining a false positive rate below 0.1%.\n\nThe system has been implemented as an open-source solution and has been adopted by several organizations for enhancing their security infrastructure.",
                    recipient="Dr. Farhan Ahmed",
                    recipient_type="faculty",
                    year=2023,
                    type="award",
                    organization="IEEE Computer Society",
                    department="Computer Science and Engineering",
                    categories=["Cybersecurity", "Intrusion Detection", "Machine Learning"],
                    link="https://github.com/farhan-ahmed/ml-ids"
                ),
                Award(
                    title="Prime Minister's Gold Medal for Academic Excellence",
                    description="Awarded for maintaining the highest CGPA in the Department of Computer Science and Engineering for four consecutive years.",
                    details="The Prime Minister's Gold Medal is one of the highest academic honors awarded to undergraduate students in Bangladesh. Recipients must demonstrate exceptional academic performance throughout their entire degree program, maintaining a perfect or near-perfect CGPA.\n\nIn addition to academic excellence, recipients must demonstrate leadership qualities, participation in extracurricular activities, and contributions to the university community.",
                    recipient="Anika Rahman",
                    recipient_type="student",
                    year=2024,
                    type="award",
                    organization="Government of Bangladesh",
                    department="Computer Science and Engineering",
                    categories=["Academic Excellence", "Undergraduate Achievement"]
                ),
                Award(
                    title="Bangladesh Academy of Sciences Research Grant",
                    description="Awarded for innovative research proposal on using AI for climate change adaptation strategies in Bangladesh.",
                    details="This competitive research grant supports projects that address critical challenges facing Bangladesh through scientific and technological innovation. The funded project aims to develop AI-powered predictive models for climate change impacts specific to Bangladesh's geographical and socioeconomic context.\n\nThe research will focus on developing adaptation strategies for agriculture, water resource management, and disaster preparedness based on machine learning analysis of climate data, satellite imagery, and socioeconomic indicators.",
                    recipient="Dr. Palash Roy",
                    recipient_type="faculty",
                    year=2022,
                    type="grant",
                    organization="Bangladesh Academy of Sciences",
                    amount=500000,
                    duration="2 years",
                    department="Computer Science and Engineering",
                    categories=["AI", "Climate Change", "Sustainable Development"]
                ),
                Award(
                    title="International Collegiate Programming Contest (ICPC) World Finals - Bronze Medal",
                    description="Team achievement for securing 3rd place in the prestigious global programming competition.",
                    details="The ICPC World Finals is the most prestigious algorithmic programming contest for university students worldwide. The team from the Department of Computer Science and Engineering, University of Dhaka demonstrated exceptional problem-solving skills, teamwork, and programming expertise to secure a bronze medal.\n\nThe team successfully solved 8 out of 12 complex algorithmic problems within the 5-hour contest period, competing against top teams from renowned universities around the world.",
                    recipient="DU_CodeBreakers Team (Rafiq Islam, Sabina Yasmin, Omar Farooq)",
                    recipient_type="student",
                    year=2023,
                    type="award",
                    organization="ICPC Foundation",
                    department="Computer Science and Engineering",
                    categories=["Competitive Programming", "Algorithms", "Team Achievement"],
                    link="https://icpc.global/worldfinals/results"
                ),
                Award(
                    title="Best Undergraduate Thesis Award",
                    description="Recognized for exceptional undergraduate thesis on developing accessible mobile applications for visually impaired users.",
                    recipient="Saima Akter",
                    recipient_type="student",
                    year=2024,
                    type="award",
                    organization="Department of Computer Science and Engineering, University of Dhaka",
                    department="Computer Science and Engineering",
                    categories=["Accessibility", "Mobile Applications", "Human-Computer Interaction"],
                    details="This award recognizes the most outstanding undergraduate thesis project in the department. The winning thesis developed and evaluated a suite of mobile applications specifically designed for visually impaired users, incorporating novel audio-tactile interfaces and gesture-based navigation.\n\nThe project included extensive user testing with visually impaired participants and resulted in practical applications that have been made freely available on app stores. The research demonstrated significant improvements in usability metrics compared to existing solutions."
                )
            ]
            
            db.add_all(awards)
            db.commit()
            
            print("Sample awards data added successfully!")
        else:
            print("Awards table already has data. Skipping sample data creation.")
            
    except Exception as e:
        print(f"Error setting up awards table: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_awards_table()
