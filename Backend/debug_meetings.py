import psycopg2
import traceback
from config import settings

# Connect to the database
conn = psycopg2.connect(
    host=settings.database_hostname,
    port=settings.database_port,
    user=settings.database_username,
    password=settings.database_password,
    database=settings.database_name
)
cursor = conn.cursor()

try:
    # Get faculty and student users directly from the database based on role IDs
    cursor.execute("""
        SELECT u.id, u.email 
        FROM users u 
        WHERE u.role_id = (SELECT id FROM roles WHERE name = 'FACULTY')
    """)
    faculty_users = cursor.fetchall()
    
    cursor.execute("""
        SELECT u.id, u.email 
        FROM users u 
        WHERE u.role_id = (SELECT id FROM roles WHERE name = 'STUDENT')
    """)
    student_users = cursor.fetchall()
    
    print(f"Found {len(faculty_users)} faculty users and {len(student_users)} student users for meetings")
    
    if not faculty_users or not student_users:
        print("Warning: No faculty or student users found. Skipping meetings seeding.")
    else:
        # Debug output
        print("Faculty users:")
        for faculty in faculty_users[:2]:
            print(f"  ID: {faculty[0]}, Email: {faculty[1]}")
            
        print("Student users:")
        for student in student_users[:2]:
            print(f"  ID: {student[0]}, Email: {student[1]}")
        
        # Create meetings
        meetings = []
        # Use the correct enum values from the models
        meeting_types = ['advising', 'thesis', 'project', 'general', 'other']
        statuses = ['scheduled', 'confirmed', 'cancelled', 'completed']
        rsvp_statuses = ['pending', 'confirmed', 'tentative', 'declined']
        
        print("Creating meetings...")
        
        # Check if meetings table exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'meetings')")
        table_exists = cursor.fetchone()[0]
        print(f"Meetings table exists: {table_exists}")
        
        # Check table structure
        if table_exists:
            cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'meetings'")
            columns = cursor.fetchall()
            print("Meetings table structure:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
        
        # Try to insert a single meeting
        faculty = faculty_users[0]
        student = student_users[0]
        
        meeting = {
            'title': f'Test Meeting: {faculty[1].split("@")[0]} with {student[1].split("@")[0]}',
            'description': 'This is a test meeting between student and faculty.',
            'faculty_id': faculty[0],
            'student_id': student[0],
            'date': '2025-07-15',
            'start_time': '10:00',
            'end_time': '11:00',
            'location': 'Room 101, CSE Building',
            'meeting_type': meeting_types[0],
            'status': statuses[0],
            'rsvp_status': rsvp_statuses[0],
            'rsvp_deadline': '2025-07-14',
            'rsvp_notes': 'Please bring your project materials for discussion.',
            'created_at': '2025-07-01 00:00:00',
            'updated_at': '2025-07-01 00:00:00'
        }
        
        print("Meeting data to insert:")
        for key, value in meeting.items():
            print(f"  {key}: {value}")
        
        try:
            cursor.execute("""
                INSERT INTO meetings (
                    title, description, faculty_id, student_id, date, start_time, end_time,
                    location, meeting_type, status, rsvp_status, rsvp_deadline, rsvp_notes,
                    created_at, updated_at
                ) VALUES (
                    %(title)s, %(description)s, %(faculty_id)s, %(student_id)s, %(date)s, 
                    %(start_time)s, %(end_time)s, %(location)s, %(meeting_type)s, %(status)s, 
                    %(rsvp_status)s, %(rsvp_deadline)s, %(rsvp_notes)s, %(created_at)s, %(updated_at)s
                ) RETURNING id;
            """, meeting)
            
            meeting_id = cursor.fetchone()[0]
            print(f"Successfully created meeting with ID {meeting_id}")
            conn.commit()
        except Exception as e:
            print(f"Error inserting meeting: {str(e)}")
            traceback.print_exc()
            conn.rollback()

except Exception as e:
    print(f"Error: {str(e)}")
    traceback.print_exc()
    conn.rollback()
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
