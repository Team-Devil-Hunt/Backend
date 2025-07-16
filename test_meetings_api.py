#!/usr/bin/env python3
"""
Test script for the Meetings API endpoints using FastAPI test client
"""
import sys
import os
from fastapi.testclient import TestClient
import json
from datetime import datetime, timedelta
from pprint import pprint

# Add the parent directory to the path so we can import the main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main app
from main import app

# Create a test client
client = TestClient(app)

# Test data
STUDENT_ID = 139  # Student Two
FACULTY_ID = 129  # Dr. Muhammad Masroor Ali

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
    print("\n=== Testing GET /api/meetings/?upcoming=true ===")
    
    response = client.get("/api/meetings/?upcoming=true")
    
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
    
    # Get today's date and one month from now
    today = datetime.now().strftime("%Y-%m-%d")
    next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Build query parameters
    params = {
        "start_date": today,
        "end_date": next_month,
        "status": "scheduled",
        "type": "advising"
    }
    
    response = client.get("/api/meetings/", params=params)
    
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

def test_create_meeting():
    """Test the endpoint to create a new meeting"""
    print("\n=== Testing POST /api/meetings/ ===")
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Create meeting data
    meeting_data = {
        "title": "Test Meeting",
        "description": "This is a test meeting created by the API test script",
        "faculty_id": FACULTY_ID,  # Using our defined constant
        "student_id": STUDENT_ID,  # Using our defined constant
        "date": tomorrow,
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "location": "Room 101",
        "meeting_type": "advising"
    }
    
    response = client.post(
        "/api/meetings/",
        json=meeting_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        print("Success! Created meeting:")
        meeting = response.json()
        print(json.dumps(meeting, indent=2))
        return meeting["id"]  # Return the ID for further testing
    else:
        print(f"Error: {response.text}")
        return None

def test_get_meeting(meeting_id):
    """Test the endpoint to get a specific meeting"""
    print(f"\n=== Testing GET /api/meetings/{meeting_id} ===")
    
    response = client.get(f"/api/meetings/{meeting_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Meeting details:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_update_meeting(meeting_id):
    """Test the endpoint to update a meeting"""
    print(f"\n=== Testing PUT /api/meetings/{meeting_id} ===")
    
    # Update data
    update_data = {
        "title": "Updated Test Meeting",
        "description": "This meeting was updated by the API test script",
        "location": "Room 202"
    }
    
    response = client.put(
        f"/api/meetings/{meeting_id}",
        json=update_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Updated meeting:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_faculty_availability():
    """Test the endpoint to get faculty availability"""
    print("\n=== Testing GET /api/meetings/faculty/{faculty_id}/availability ===")
    
    # Date to check availability
    date = datetime.now().strftime("%Y-%m-%d")
    
    response = client.get(
        f"/api/meetings/faculty/{FACULTY_ID}/availability?date={date}"
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Faculty availability:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_delete_meeting(meeting_id):
    """Test the endpoint to delete a meeting"""
    print(f"\n=== Testing DELETE /api/meetings/{meeting_id} ===")
    
    response = client.delete(f"/api/meetings/{meeting_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Success! Meeting deleted")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 204

def main():
    """Run all tests"""
    print("Starting Meetings API Tests...")
    print("==================================")
    
    # Test getting meeting types
    test_get_meeting_types()
    
    # Test listing all meetings
    test_list_meetings()
    
    # Test upcoming meetings
    test_upcoming_meetings()
    
    # Test filtered meetings
    test_filtered_meetings()
    
    # Test faculty availability
    test_faculty_availability()
    
    # Test creating a meeting
    create_response = test_create_meeting()
    
    # If meeting creation was successful, test other operations on that meeting
    if create_response.status_code == 201:
        meeting_id = create_response.json().get("id")
        
        # Test getting the meeting
        test_get_meeting(meeting_id)
        
        # Test updating the meeting
        test_update_meeting(meeting_id)
        
        # Test deleting the meeting
        test_delete_meeting(meeting_id)
    else:
        # Try to get an existing meeting ID
        meetings_response = client.get("/api/meetings/")
        if meetings_response.status_code == 200 and meetings_response.json():
            meeting_id = meetings_response.json()[0].get("id")
            if meeting_id:
                # Test getting the meeting
                test_get_meeting(meeting_id)
                
                # Test updating the meeting
                test_update_meeting(meeting_id)
    
    print("\nAll tests completed!")
    print("==================================")

if __name__ == "__main__":
    main()
