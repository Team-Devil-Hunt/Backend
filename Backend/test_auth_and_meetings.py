#!/usr/bin/env python3
"""
Test script for authentication and meetings API integration.
This script tests the complete flow from login to accessing meetings data.
"""

import requests
import json
from datetime import datetime, timedelta
from pprint import pprint

# Configuration
BASE_URL = "http://127.0.0.1:8000"
CREDENTIALS = {
    "student": {
        "email": "student2@csedu.edu",
        "password": "password123",
        "id": 139  # From the database query
    },
    "faculty": {
        "email": "masroor@csedu.edu",
        "password": "password123",
        "id": 129  # From the database query
    }
}

def test_auth_and_meetings():
    """Test authentication and meetings API integration."""
    session = requests.Session()
    
    print("\n===== Testing Authentication and Meetings API Integration =====\n")
    
    # Step 1: Login as student
    print("Step 1: Login as student")
    login_response = session.post(
        f"{BASE_URL}/api/auth/login",
        json=CREDENTIALS["student"]
    )
    
    if login_response.status_code != 200:
        print(f"Login failed with status code {login_response.status_code}")
        print(login_response.text)
        return False
    
    login_data = login_response.json()
    print(f"Login successful: {login_data.get('message')}")
    print(f"User ID: {login_data.get('id')}")
    print(f"User Role: {login_data.get('role', {}).get('name')}")
    
    # The session cookie is automatically handled by the requests.Session object
    # No need to manually set Authorization header
    
    # Step 2: Get meeting types
    print("\nStep 2: Get meeting types")
    types_response = session.get(f"{BASE_URL}/api/meetings/types")
    
    if types_response.status_code != 200:
        print(f"Failed to get meeting types: {types_response.status_code}")
        print(types_response.text)
    else:
        meeting_types = types_response.json()
        print(f"Successfully retrieved {len(meeting_types)} meeting types:")
        pprint(meeting_types)
    
    # Step 3: Get all meetings
    print("\nStep 3: Get all meetings")
    meetings_response = session.get(f"{BASE_URL}/api/meetings/")
    
    if meetings_response.status_code != 200:
        print(f"Failed to get meetings: {meetings_response.status_code}")
        print(meetings_response.text)
        return False
    
    meetings = meetings_response.json()
    print(f"Successfully retrieved {len(meetings)} meetings")
    if meetings:
        print("First meeting:")
        pprint(meetings[0])
    
    # Step 4: Get upcoming meetings
    print("\nStep 4: Get upcoming meetings")
    upcoming_response = session.get(f"{BASE_URL}/api/meetings/?upcoming=true")
    
    if upcoming_response.status_code != 200:
        print(f"Failed to get upcoming meetings: {upcoming_response.status_code}")
        print(upcoming_response.text)
    else:
        upcoming = upcoming_response.json()
        print(f"Successfully retrieved {len(upcoming)} upcoming meetings")
        if upcoming:
            print("First upcoming meeting:")
            pprint(upcoming[0])
    
    # Step 5: Get meetings with filters
    print("\nStep 5: Get meetings with filters")
    today = datetime.now().strftime("%Y-%m-%d")
    next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    filters_response = session.get(
        f"{BASE_URL}/api/meetings/?start_date={today}&end_date={next_month}&status=confirmed"
    )
    
    if filters_response.status_code != 200:
        print(f"Failed to get filtered meetings: {filters_response.status_code}")
        print(filters_response.text)
    else:
        filtered = filters_response.json()
        print(f"Successfully retrieved {len(filtered)} filtered meetings")
        if filtered:
            print("First filtered meeting:")
            pprint(filtered[0])
    
    # Step 6: Update RSVP status for a meeting
    if meetings:
        meeting_id = meetings[0]["id"]
        print(f"\nStep 6: Update RSVP status for meeting {meeting_id}")
        
        rsvp_response = session.put(
            f"{BASE_URL}/api/meetings/{meeting_id}/rsvp",
            params={"status": "confirmed", "notes": "Looking forward to the meeting!"}
        )
        
        if rsvp_response.status_code != 200:
            print(f"Failed to update RSVP: {rsvp_response.status_code}")
            print(rsvp_response.text)
        else:
            rsvp_result = rsvp_response.json()
            print("RSVP update successful:")
            pprint(rsvp_result)
    
    # Step 7: Get faculty availability
    if meetings and meetings[0].get("faculty_id"):
        faculty_id = meetings[0]["faculty_id"]
        print(f"\nStep 7: Get faculty availability for faculty {faculty_id}")
        
        availability_response = session.get(
            f"{BASE_URL}/api/meetings/faculty/{faculty_id}/availability",
            params={"date": today}
        )
        
        if availability_response.status_code != 200:
            print(f"Failed to get faculty availability: {availability_response.status_code}")
            print(availability_response.text)
        else:
            availability = availability_response.json()
            print("Faculty availability:")
            pprint(availability)
    
    print("\n===== Test Completed Successfully =====")
    return True

if __name__ == "__main__":
    test_auth_and_meetings()
