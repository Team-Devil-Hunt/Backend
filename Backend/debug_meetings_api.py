#!/usr/bin/env python3
"""
Debug script for the Meetings API endpoints
This script bypasses authentication to test the API endpoints directly
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import json
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

# Import the FastAPI app
from main import app
from database import SessionLocal
from models import MeetingStatus, RSVPStatus, MeetingType
from dependencies import get_user_from_session
from database import get_db, engine
from models import Base, User, Role, Faculty, Meeting

# Create a test client
client = TestClient(app)

# Mock session data for authentication bypass
mock_user_data = {
    "id": 1,
    "name": "Test Admin",
    "email": "admin@example.com",
    "role": {"id": 1, "name": "admin", "permissions": ["all"]}
}

# Override the dependency to bypass authentication
def override_get_user_from_session():
    return mock_user_data

# Apply the override
app.dependency_overrides[get_user_from_session] = override_get_user_from_session

def print_response(response, title: str):
    """Print the response in a formatted way"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    
    try:
        if response.status_code != 204:  # No content
            data = response.json()
            if isinstance(data, list):
                print(f"Found {len(data)} items")
                if data:
                    print("First item:")
                    print(json.dumps(data[0], indent=2))
            else:
                print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        print(response.text)

def test_meeting_types():
    # Test getting meeting types
    print("\n=== GET /api/meetings/types ===")
    response = client.get("/api/meetings/types")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        types = response.json()
        print(f"Found {len(types)} meeting types")
        print("Types:", types)
    else:
        print(response.json())

def test_list_meetings():
    """Test the endpoint to list all meetings"""
    response = client.get("/api/meetings/")
    print_response(response, "GET /api/meetings/")
    return response

def test_filtered_meetings():
    """Test the endpoint to list meetings with filters"""
    # Get meetings for the next 30 days
    today = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    params = {
        "start_date": today,
        "end_date": end_date,
        "status": "SCHEDULED"  # Using uppercase to match enum values
    }
    
    response = client.get("/api/meetings/", params=params)
    print_response(response, "GET /api/meetings/ with filters")
    return response

def test_upcoming_meetings():
    """Test the endpoint to get upcoming meetings"""
    # The upcoming endpoint is a query parameter, not a path
    response = client.get("/api/meetings/", params={"upcoming": "true"})
    print_response(response, "GET /api/meetings/?upcoming=true")
    return response

# The faculty endpoint is likely in a different router, so we'll skip this test
# def test_faculty_endpoint():
#     """Test the endpoint to get faculty members"""
#     response = client.get("/api/faculty/")
#     print_response(response, "GET /api/faculty/")
#     return response

def test_faculty_availability():
    """Test the endpoint to get faculty availability"""
    faculty_id = 129  # Using Dr. Muhammad Masroor Ali's ID from the debug output
    date = "2025-07-16"  # Replace with a valid date
    response = client.get(f"/api/meetings/faculty/{faculty_id}/availability?date={date}")
    print_response(response, f"GET /api/meetings/faculty/{faculty_id}/availability")
    return response

def test_create_meeting():
    """Test the endpoint to create a new meeting"""
    # Create a meeting for tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Using valid IDs from the database based on debug output
    faculty_id = 129  # Dr. Muhammad Masroor Ali
    student_id = 139  # Student Two
    
    meeting_data = {
        "title": "Test Meeting",
        "description": "This is a test meeting created by the API test script",
        "faculty_id": faculty_id,
        "student_id": student_id,
        "date": tomorrow,
        "start_time": "10:00",
        "end_time": "10:30",
        "location": "Office 101",
        "meeting_type": MeetingType.ADVISING.value,  # Using enum value
        "status": MeetingStatus.SCHEDULED.value,  # Using enum value
        "rsvp_status": RSVPStatus.PENDING.value,  # Using enum value
        "rsvp_notes": "Test notes"
    }
    
    response = client.post("/api/meetings/", json=meeting_data)
    print_response(response, "POST /api/meetings/")
    
    if response.status_code in [200, 201]:
        return response.json()["id"]
    return None

def test_get_meeting(meeting_id):
    """Test the endpoint to get a specific meeting"""
    response = client.get(f"/api/meetings/{meeting_id}")
    print_response(response, f"GET /api/meetings/{meeting_id}")
    return response

def test_update_meeting(meeting_id):
    """Test the endpoint to update a meeting"""
    update_data = {
        "title": "Updated Test Meeting",
        "description": "This meeting was updated by the API test script",
        "rsvp_notes": "Updated test notes"
    }
    
    response = client.put(f"/api/meetings/{meeting_id}", json=update_data)
    print_response(response, f"PUT /api/meetings/{meeting_id}")
    return response

def test_update_rsvp(meeting_id):
    """Test the endpoint to update RSVP status"""
    response = client.post(
        f"/api/meetings/{meeting_id}/rsvp",
        params={"rsvp_status": "CONFIRMED", "rsvp_notes": "RSVP confirmed by test script"}
    )
    print_response(response, f"POST /api/meetings/{meeting_id}/rsvp")
    return response

def test_delete_meeting(meeting_id):
    """Test the endpoint to delete a meeting"""
    response = client.delete(f"/api/meetings/{meeting_id}")
    print_response(response, f"DELETE /api/meetings/{meeting_id}")
    return response

def main():
    """Run all tests"""
    print("Starting Meetings API Tests")
    
    # Test getting meeting types
    test_meeting_types()
    
    # Test listing meetings
    test_list_meetings()
    
    # Test upcoming meetings
    test_upcoming_meetings()
    
    # Test filtered meetings
    test_filtered_meetings()
    
    # Test faculty availability
    test_faculty_availability()
    
    # Test creating a meeting
    meeting_id = test_create_meeting()
    
    if meeting_id:
        # Test getting a specific meeting
        test_get_meeting(meeting_id)
        
        # Test updating a meeting
        test_update_meeting(meeting_id)
        
        # Test updating RSVP status
        test_update_rsvp(meeting_id)
        
        # Test deleting a meeting
        test_delete_meeting(meeting_id)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
