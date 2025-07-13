from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AdmissionStats, AdmissionDeadline, AdmissionFAQ
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Database connection
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_admissions_tables():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have stats data
        existing_stats = db.query(AdmissionStats).first()
        
        if not existing_stats:
            print("Adding admission stats...")
            
            # Add admission stats
            stats = AdmissionStats(
                next_deadline="July 30, 2025",
                programs_offered=8,
                application_time="4-6 weeks",
                acceptance_rate="12%"
            )
            
            db.add(stats)
            db.commit()
            
            print("Admission stats added successfully!")
        else:
            print("Admission stats already exist. Skipping...")
            
        # Check if we already have deadline data
        existing_deadlines = db.query(AdmissionDeadline).count()
        
        if existing_deadlines == 0:
            print("Adding admission deadlines...")
            
            # Calculate dates relative to current date for better demo
            today = datetime.now()
            next_month = today + timedelta(days=30)
            two_months = today + timedelta(days=60)
            three_months = today + timedelta(days=90)
            
            # Add admission deadlines
            deadlines = [
                AdmissionDeadline(
                    program="Bachelor of Science in Computer Science and Engineering",
                    level="Undergraduate",
                    date=next_month,
                    requirements="High school diploma with strong mathematics background. Minimum GPA of 3.5.",
                    notes="Early applications are encouraged."
                ),
                AdmissionDeadline(
                    program="Master of Science in Computer Science",
                    level="Graduate",
                    date=two_months,
                    requirements="Bachelor's degree in Computer Science or related field. Minimum GPA of 3.0.",
                    notes="GRE scores are required for international applicants."
                ),
                AdmissionDeadline(
                    program="Doctor of Philosophy in Computer Science",
                    level="Postgraduate",
                    date=three_months,
                    requirements="Master's degree in Computer Science or related field. Research proposal required.",
                    notes="Applicants are encouraged to contact potential supervisors before applying."
                ),
                AdmissionDeadline(
                    program="Bachelor of Science in Software Engineering",
                    level="Undergraduate",
                    date=next_month,
                    requirements="High school diploma with strong mathematics background. Minimum GPA of 3.5.",
                    notes=None
                ),
                AdmissionDeadline(
                    program="Master of Science in Data Science",
                    level="Graduate",
                    date=two_months,
                    requirements="Bachelor's degree in Computer Science, Statistics, or related field. Minimum GPA of 3.0.",
                    notes="Programming experience in Python or R is required."
                )
            ]
            
            db.add_all(deadlines)
            db.commit()
            
            print("Admission deadlines added successfully!")
        else:
            print("Admission deadlines already exist. Skipping...")
            
        # Check if we already have FAQ data
        existing_faqs = db.query(AdmissionFAQ).count()
        
        if existing_faqs == 0:
            print("Adding admission FAQs...")
            
            # Add admission FAQs
            faqs = [
                AdmissionFAQ(
                    question="What are the admission requirements for undergraduate programs?",
                    answer="Applicants must have a high school diploma or equivalent with strong performance in mathematics and science subjects. A minimum GPA of 3.5 is required. Applicants must also pass the university entrance examination.",
                    category="Requirements"
                ),
                AdmissionFAQ(
                    question="How do I apply for graduate programs?",
                    answer="Applications for graduate programs are submitted online through the university portal. Required documents include transcripts, letters of recommendation, statement of purpose, and GRE scores for international applicants.",
                    category="Application Process"
                ),
                AdmissionFAQ(
                    question="Are there any scholarships available for international students?",
                    answer="Yes, the university offers merit-based scholarships for international students with outstanding academic records. Additionally, research assistantships and teaching assistantships are available for graduate students.",
                    category="Financial Aid"
                ),
                AdmissionFAQ(
                    question="What is the application fee?",
                    answer="The application fee is 2,000 BDT for domestic students and $50 USD for international students. The fee can be paid online during the application process.",
                    category="Fees"
                ),
                AdmissionFAQ(
                    question="Can I transfer credits from another university?",
                    answer="Yes, credits can be transferred from accredited institutions. The maximum number of transferable credits is 60 for undergraduate programs and 9 for graduate programs. Each transfer request is evaluated individually.",
                    category="Transfer Students"
                ),
                AdmissionFAQ(
                    question="What documents are required for the application?",
                    answer="Required documents include academic transcripts, certificates, passport-sized photographs, national ID or birth certificate, and application fee payment receipt. International students must also provide proof of English proficiency.",
                    category="Application Process"
                ),
                AdmissionFAQ(
                    question="How competitive is the admission process?",
                    answer="Admission to our programs is highly competitive, with an acceptance rate of approximately 12%. We evaluate applicants based on academic performance, entrance exam scores, and other relevant achievements.",
                    category="General"
                ),
                AdmissionFAQ(
                    question="What are the tuition fees for the programs?",
                    answer="Tuition fees vary by program. Undergraduate programs cost approximately 8,000 BDT per credit hour, while graduate programs cost approximately 10,000 BDT per credit hour. International students pay approximately 1.5 times the regular tuition fees.",
                    category="Fees"
                )
            ]
            
            db.add_all(faqs)
            db.commit()
            
            print("Admission FAQs added successfully!")
        else:
            print("Admission FAQs already exist. Skipping...")
            
    except Exception as e:
        print(f"Error setting up admissions tables: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_admissions_tables()
