import psycopg2
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
    # Check enum types in the database
    cursor.execute("""
        SELECT t.typname, e.enumlabel
        FROM pg_type t 
        JOIN pg_enum e ON t.oid = e.enumtypid
        WHERE t.typname IN ('meetingtype', 'meetingstatus', 'rsvpstatus')
        ORDER BY t.typname, e.enumsortorder
    """)
    
    enums = cursor.fetchall()
    
    current_type = None
    for enum in enums:
        if current_type != enum[0]:
            current_type = enum[0]
            print(f"\n{current_type} values:")
        print(f"  - {enum[1]}")
    
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    cursor.close()
    conn.close()
    print("\nDatabase connection closed.")
