#!/usr/bin/env python3
"""
Test script for the Meetings API endpoints with proper authentication
"""
import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test credentials
CREDENTIALS = {
    "email": "student1@csedu.edu",
    "password": "student123"
}

def login_and_get_session():
    """Login and get a session cookie"""
    print("\n=== Logging in to get session cookie ===")
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=CREDENTIALS
    )
    
    print(f"Login Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("Login successful!")
        # Get the session cookie
        session_cookie = response.cookies.get_dict()
        print(f"Session cookie: {session_cookie}")
        return session_cookie
    else:
        print(f"Login failed: {response.text}")
        return None

def test_get_meeting_types(session_cookie):
    """Test the endpoint to get all meeting types"""
    print("\n=== Testing GET /api/meetings/types ===")
    
    response = requests.get(
        f"{BASE_URL}/api/meetings/types", 
        cookies=session_cookie
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Meeting types:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def test_list_meetings(session_cookie):
    """Test the endpoint to list all meetings"""
    print("\n=== Testing GET /api/meetings/ ===")
    
    response = requests.get(
        f"{BASE_URL}/api/meetings/", 
        cookies=session_cookie
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meetings = response.json()
        print(f"Found {len(meetings)} meetings")
        if meetings:
            print("First meeting:")
            print(json.dumps(meetings[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def test_upcoming_meetings(session_cookie):
    """Test the endpoint to get upcoming meetings"""
    print("\n=== Testing GET /api/meetings/?upcoming=true ===")
    
    response = requests.get(
        f"{BASE_URL}/api/meetings/?upcoming=true", 
        cookies=session_cookie
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meetings = response.json()
        print(f"Found {len(meetings)} upcoming meetings")
        if meetings:
            print("First upcoming meeting:")
            print(json.dumps(meetings[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def test_filtered_meetings(session_cookie):
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
    
    response = requests.get(
        f"{BASE_URL}/api/meetings/", 
        cookies=session_cookie,
        params=params
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meetings = response.json()
        print(f"Found {len(meetings)} filtered meetings")
        if meetings:
            print("First filtered meeting:")
            print(json.dumps(meetings[0], indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def test_faculty_availability(session_cookie, faculty_id=129):
    """Test the endpoint to get faculty availability"""
    print(f"\n=== Testing GET /api/meetings/faculty/{faculty_id}/availability ===")
    
    # Date to check availability
    date = datetime.now().strftime("%Y-%m-%d")
    
    response = requests.get(
        f"{BASE_URL}/api/meetings/faculty/{faculty_id}/availability?date={date}", 
        cookies=session_cookie
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        availability = response.json()
        print("Faculty availability:")
        print(json.dumps(availability, indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def test_create_meeting(session_cookie, faculty_id=129, student_id=139):
    """Test the endpoint to create a new meeting"""
    print("\n=== Testing POST /api/meetings/ ===")
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Create meeting data
    meeting_data = {
        "title": "Test Meeting",
        "description": "This is a test meeting created by the API test script",
        "faculty_id": faculty_id,
        "student_id": student_id,
        "date": tomorrow,
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "location": "Room 101",
        "meeting_type": "advising"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/meetings/", 
        cookies=session_cookie,
        json=meeting_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        meeting = response.json()
        print("Created meeting:")
        print(json.dumps(meeting, indent=2))
        return meeting.get("id")
    else:
        print(f"Error: {response.text}")
        return None

def test_get_meeting(session_cookie, meeting_id):
    """Test the endpoint to get a specific meeting"""
    print(f"\n=== Testing GET /api/meetings/{meeting_id} ===")
    
    response = requests.get(
        f"{BASE_URL}/api/meetings/{meeting_id}", 
        cookies=session_cookie
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        meeting = response.json()
        print("Meeting details:")
        print(json.dumps(meeting, indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def test_update_rsvp(session_cookie, meeting_id):
    """Test the endpoint to update RSVP status"""
    print(f"\n=== Testing PUT /api/meetings/{meeting_id}/rsvp ===")
    
    rsvp_data = {
        "status": "confirmed",
        "notes": "Looking forward to the meeting!"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/meetings/{meeting_id}/rsvp", 
        cookies=session_cookie,
        json=rsvp_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("RSVP update result:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def main():
    """Run all tests"""
    print("Starting Meetings API Tests with Authentication...")
    print("================================================")
    
    # Login and get session cookie
    session_cookie = login_and_get_session()
    if not session_cookie:
        print("Failed to login. Exiting tests.")
        return
    
    # Test getting meeting types
    test_get_meeting_types(session_cookie)
    
    # Test listing all meetings
    meetings_response = test_list_meetings(session_cookie)
    
    # Test upcoming meetings
    test_upcoming_meetings(session_cookie)
    
    # Test filtered meetings
    test_filtered_meetings(session_cookie)
    
    # Test faculty availability
    test_faculty_availability(session_cookie)
    
    # Test creating a meeting
    meeting_id = test_create_meeting(session_cookie)
    
    # If meeting creation was successful, test other operations on that meeting
    if meeting_id:
        # Test getting the meeting
        test_get_meeting(session_cookie, meeting_id)
        
        # Test updating RSVP
        test_update_rsvp(session_cookie, meeting_id)
    else:
        # Try to get an existing meeting ID from the list meetings response
        if meetings_response.status_code == 200:
            meetings = meetings_response.json()
            if meetings:
                meeting_id = meetings[0].get("id")
                if meeting_id:
                    # Test getting the meeting
                    test_get_meeting(session_cookie, meeting_id)
                    
                    # Test updating RSVP
                    test_update_rsvp(session_cookie, meeting_id)
    
    print("\nAll tests completed!")
    print("================================================")

if __name__ == "__main__":
    main()
