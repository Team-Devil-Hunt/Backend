from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_contact import Base, ContactMessage
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Database connection
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_contact_table():
    # Create the contact_messages table
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have sample data
        existing_messages = db.query(ContactMessage).count()
        
        if existing_messages == 0:
            print("Adding sample contact messages...")
            
            # Add sample contact messages
            sample_messages = [
                ContactMessage(
                    id=str(uuid.uuid4()),
                    name="John Doe",
                    email="john.doe@example.com",
                    subject="Admission Inquiry",
                    message="I would like to know more about the admission process for the undergraduate program.",
                    phone="+1234567890"
                ),
                ContactMessage(
                    id=str(uuid.uuid4()),
                    name="Jane Smith",
                    email="jane.smith@example.com",
                    subject="Research Collaboration",
                    message="I am interested in collaborating on a research project related to artificial intelligence.",
                    phone="+9876543210"
                ),
                ContactMessage(
                    id=str(uuid.uuid4()),
                    name="David Johnson",
                    email="david.johnson@example.com",
                    subject="Visiting Professor Inquiry",
                    message="I am a professor at XYZ University and would like to visit your department as a guest lecturer.",
                    phone=None
                )
            ]
            
            db.add_all(sample_messages)
            db.commit()
            
            print("Sample contact messages added successfully!")
        else:
            print("Contact messages table already has data. Skipping sample data creation.")
            
    except Exception as e:
        print(f"Error setting up contact messages table: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_contact_table()
