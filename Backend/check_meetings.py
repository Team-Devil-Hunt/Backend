from sqlalchemy import create_engine, text
from config import settings

# Create SQLAlchemy engine
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)

# Check database tables and data
with engine.connect() as conn:
    # Check roles table
    print("\n=== ROLES TABLE ===")
    result = conn.execute(text("SELECT id, name FROM roles"))
    roles = result.fetchall()
    print(f"Number of roles: {len(roles)}")
    for role in roles:
        print(f"Role ID: {role[0]}, Name: {role[1]}")
    
    # Check users table
    print("\n=== USERS TABLE ===")
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    user_count = result.scalar()
    print(f"Number of users: {user_count}")
    
    # Check faculty users
    print("\n=== FACULTY USERS ===")
    result = conn.execute(text("""
        SELECT u.id, u.email, u.role_id 
        FROM users u 
        WHERE u.role_id = (SELECT id FROM roles WHERE name = 'FACULTY')
        LIMIT 5
    """))
    faculty_users = result.fetchall()
    print(f"Number of faculty users found: {len(faculty_users)}")
    for user in faculty_users:
        print(f"ID: {user[0]}, Email: {user[1]}, Role ID: {user[2]}")
    
    # Check student users
    print("\n=== STUDENT USERS ===")
    result = conn.execute(text("""
        SELECT u.id, u.email, u.role_id 
        FROM users u 
        WHERE u.role_id = (SELECT id FROM roles WHERE name = 'STUDENT')
        LIMIT 5
    """))
    student_users = result.fetchall()
    print(f"Number of student users found: {len(student_users)}")
    for user in student_users:
        print(f"ID: {user[0]}, Email: {user[1]}, Role ID: {user[2]}")
    
    # Check if meetings table exists and has data
    print("\n=== MEETINGS TABLE ===")
    result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'meetings')"))
    table_exists = result.scalar()
    
    if table_exists:
        print("Meetings table exists in the database.")
        
        # Count meetings
        result = conn.execute(text("SELECT COUNT(*) FROM meetings"))
        count = result.scalar()
        print(f"Number of meetings in database: {count}")
        
        if count > 0:
            # Sample data
            result = conn.execute(text("SELECT id, title, faculty_id, student_id, date, meeting_type, status, rsvp_status FROM meetings LIMIT 5"))
            rows = result.fetchall()
            print("\nSample meetings:")
            for row in rows:
                print(row)
    else:
        print("Meetings table does not exist in the database.")
