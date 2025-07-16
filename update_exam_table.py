"""
Script to update the exams table with new columns for student exams feature.
This script directly alters the database schema.
"""

from sqlalchemy import create_engine, text
from database import engine

def update_exam_table():
    # Use the imported engine
    
    # Connect and execute the SQL statements
    with engine.connect() as connection:
        # Add new columns to the exams table
        try:
            # Start a transaction
            connection.execute(text("BEGIN;"))
            
            # Add title column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title VARCHAR;"))
            
            # Add course_id column with foreign key
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS course_id INTEGER;"))
            
            # Check if constraint exists before adding it
            constraint_exists = connection.execute(text("""
                SELECT 1 FROM pg_constraint 
                WHERE conname = 'fk_course' AND conrelid = 'exams'::regclass;
            """)).fetchone()
            
            if not constraint_exists:
                connection.execute(text("ALTER TABLE exams ADD CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses(id);"))
            
            # Add location column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS location VARCHAR;"))
            
            # Add total_marks column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS total_marks INTEGER;"))
            
            # Add obtained_marks column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS obtained_marks INTEGER;"))
            
            # Add instructions column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS instructions TEXT;"))
            
            # Add materials_allowed column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS materials_allowed JSON;"))
            
            # Add syllabus_topics column
            connection.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS syllabus_topics JSON;"))
            
            # Modify date column type to Date if needed
            # This is a bit tricky as it requires data conversion
            # For now, we'll keep the DateTime type as it's compatible
            
            # Commit the transaction
            connection.execute(text("COMMIT;"))
            
            print("Successfully updated exams table schema.")
            
        except Exception as e:
            # Rollback in case of error
            connection.execute(text("ROLLBACK;"))
            print(f"Error updating exams table: {e}")

if __name__ == "__main__":
    update_exam_table()
