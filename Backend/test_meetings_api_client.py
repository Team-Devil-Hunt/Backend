#!/usr/bin/env python3
"""
Test script for the Meetings API endpoints using FastAPI TestClient
"""
import json
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app
from database import get_db, engine
from sqlalchemy.orm import Session
from models import Base, User, Role, Faculty, Student, Meeting, MeetingType

# Create a test client
client = TestClient(app)

# Mock session data for authentication bypass
mock_user_data = {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "role": {"id": 1, "name": "admin", "permissions": ["all"]}
}

# Override the dependency to bypass authentication
def override_get_user_from_session():
    return mock_user_data

app.dependency_overrides[get_db] = lambda: Session(bind=engine)

# Test functions
def test_get_meeting_types():
    """Test the endpoint to get all meeting types"""
    print("\n=== Testing GET /api/meetings/types ===")
    
    response = client.get("/api/meetings/types")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Meeting types:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_list_meetings():
    """Test the endpoint to list all meetings"""
    print("\n=== Testing GET /api/meetings/ ===")
    
    response = client.get("/api/meetings/")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meetings = response.json()
        print(f"Success! Found {len(meetings)} meetings")
        if meetings:
            print("First meeting:")
            print(json.dumps(meetings[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_upcoming_meetings():
    """Test the endpoint to get upcoming meetings"""
    print("\n=== Testing GET /api/meetings/upcoming ===")
    
    response = client.get("/api/meetings/upcoming")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meetings = response.json()
        print(f"Success! Found {len(meetings)} upcoming meetings")
        if meetings:
            print("First upcoming meeting:")
            print(json.dumps(meetings[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_filtered_meetings():
    """Test the endpoint to list meetings with filters"""
    print("\n=== Testing GET /api/meetings/ with filters ===")
    
    # Get meetings for the next 30 days
    today = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    response = client.get(
        "/api/meetings/",
        params={
            "start_date": today,
            "end_date": end_date,
            "status": "pending"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meetings = response.json()
        print(f"Success! Found {len(meetings)} filtered meetings")
        if meetings:
            print("First filtered meeting:")
            print(json.dumps(meetings[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_faculty_endpoint():
    """Test the endpoint to get faculty members"""
    print("\n=== Testing GET /api/meetings/faculty ===")
    
    response = client.get("/api/meetings/faculty")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        faculty = response.json()
        print(f"Success! Found {len(faculty)} faculty members")
        if faculty:
            print("First faculty member:")
            print(json.dumps(faculty[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_faculty_availability():
    """Test the endpoint to get faculty availability"""
    print("\n=== Testing GET /api/meetings/{faculty_id}/availability ===")
    
    # You'll need to replace this with a valid faculty ID
    faculty_id = 1
    
    # Check availability for tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    response = client.get(
        f"/api/meetings/{faculty_id}/availability",
        params={"date": tomorrow}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Faculty availability:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print("Starting Meetings API Tests")
    
    # Test getting meeting types
    test_get_meeting_types()
    
    # Test listing meetings
    test_list_meetings()
    
    # Test upcoming meetings
    test_upcoming_meetings()
    
    # Test filtered meetings
    test_filtered_meetings()
    
    # Test faculty endpoint
    test_faculty_endpoint()
    
    # Test faculty availability
    test_faculty_availability()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    # Override the dependency
    from dependencies import get_user_from_session
    app.dependency_overrides[get_user_from_session] = override_get_user_from_session
    
    main()
