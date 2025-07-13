import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine
from models import Assignment, AssignmentSubmission

def create_tables():
    print("Creating Assignment and AssignmentSubmission tables...")
    Base.metadata.create_all(bind=engine, tables=[Assignment.__table__, AssignmentSubmission.__table__])
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
