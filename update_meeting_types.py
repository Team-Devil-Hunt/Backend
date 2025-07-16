#!/usr/bin/env python3
"""
Script to update meeting types, meeting status, and RSVP status in the database from lowercase to uppercase.
"""
from sqlalchemy import create_engine, text
import os
from config import settings

def update_meeting_types():
    """Update meeting types, meeting status, and RSVP status from lowercase to uppercase in the database."""
    print("Connecting to database...")
    
    # Check if running in Docker (environment variable set in docker-compose.yml)
    IN_DOCKER = os.environ.get('IN_DOCKER', '').lower() in ('true', '1', 't')
    
    # Use the appropriate database URL based on environment
    if IN_DOCKER:
        # When running in Docker, use the service name
        sqlAlchemyDatabaseUrl = f"postgresql://{settings.database_username}:{settings.database_password}@db:{settings.database_port}/{settings.database_name}"
    else:
        # When running locally, use localhost
        sqlAlchemyDatabaseUrl = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
    
    print(f"Using database URL: {sqlAlchemyDatabaseUrl}")
    engine = create_engine(sqlAlchemyDatabaseUrl)
    
    # Define the mapping of lowercase to uppercase meeting types
    meeting_types = {
        'advising': 'ADVISING',
        'thesis': 'THESIS',
        'project': 'PROJECT',
        'general': 'GENERAL',
        'other': 'OTHER'
    }
    
    # Define the mapping of lowercase to uppercase meeting status
    meeting_status = {
        'scheduled': 'SCHEDULED',
        'confirmed': 'CONFIRMED',
        'cancelled': 'CANCELLED',
        'completed': 'COMPLETED'
    }
    
    # Define the mapping of lowercase to uppercase RSVP status
    rsvp_status = {
        'pending': 'PENDING',
        'confirmed': 'CONFIRMED',
        'tentative': 'TENTATIVE',
        'declined': 'DECLINED'
    }
    
    with engine.connect() as connection:
        # Start a transaction
        with connection.begin():
            print("Updating meeting types...")
            
            # Update each meeting type
            for old_type, new_type in meeting_types.items():
                query = text(f"UPDATE meetings SET meeting_type = '{new_type}' WHERE meeting_type = '{old_type}'")
                result = connection.execute(query)
                print(f"Updated {result.rowcount} records from '{old_type}' to '{new_type}'")
            
            print("Updating meeting status...")
            
            # Update each meeting status
            for old_status, new_status in meeting_status.items():
                query = text(f"UPDATE meetings SET status = '{new_status}' WHERE status = '{old_status}'")
                result = connection.execute(query)
                print(f"Updated {result.rowcount} records from '{old_status}' to '{new_status}'")
            
            print("Updating RSVP status...")
            
            # Update each RSVP status
            for old_status, new_status in rsvp_status.items():
                query = text(f"UPDATE meetings SET rsvp_status = '{new_status}' WHERE rsvp_status = '{old_status}'")
                result = connection.execute(query)
                print(f"Updated {result.rowcount} records from '{old_status}' to '{new_status}'")
            
            print("All updates completed successfully!")

if __name__ == "__main__":
    update_meeting_types()
