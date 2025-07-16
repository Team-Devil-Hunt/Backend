import requests
import json
import traceback
import sys
import time

# Enable more verbose output
requests.packages.urllib3.add_stderr_logger()

# Set to True to print detailed debugging information
DEBUG = True

def print_debug(message):
    """Print debug messages if DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def test_login_and_permissions():
    """Test login and check user permissions"""
    base_url = "http://127.0.0.1:8000"
    print(f"Testing connection to {base_url}...")
    
    # Test if server is reachable
    try:
        test_response = requests.get(f"{base_url}/ping")
        print(f"Server ping response: {test_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running.")
        return
    
    # Student login
    student_credentials = {
        "email": "fahim@student.csedu.edu",
        "password": "student123"
    }
    
    print("\n===== TESTING STUDENT LOGIN AND PERMISSIONS =====\n")
    session = requests.Session()
    
    try:
        # Step 1: Login
        print("Step 1: Logging in...")
        print_debug(f"Sending login request to {base_url}/api/auth/login")
        response = session.post(
            f"{base_url}/api/auth/login", 
            json=student_credentials,
            headers={"Content-Type": "application/json"},
            # Make sure cookies are stored in the session
            allow_redirects=True
        )
        
        print(f"Login status code: {response.status_code}")
        print_debug(f"Response headers: {dict(response.headers)}")
        print_debug(f"Cookies after login: {session.cookies.get_dict()}")
        
        if response.status_code == 200:
            print("\n✅ Login successful!")
            user_data = response.json()
            print(f"User: {user_data['name']} ({user_data['email']})")
            print(f"Role: {user_data['role']['name']}")
            print(f"Permissions: {user_data['role']['permissions']}")
            
            # Check if user has SUBMIT_ASSIGNMENT permission
            has_submit_permission = "SUBMIT_ASSIGNMENT" in user_data['role']['permissions']
            print(f"\nHas SUBMIT_ASSIGNMENT permission: {'✅ Yes' if has_submit_permission else '❌ No'}")
            
            # Step 2: Test fetching assignments
            print("\nStep 2: Fetching assignments...")
            assignments_response = session.get(
                f"{base_url}/api/assignments",
                headers={"Content-Type": "application/json"}
            )
            print(f"Assignments status code: {assignments_response.status_code}")
            
            if assignments_response.status_code == 200:
                print("✅ Successfully fetched assignments")
                assignments = assignments_response.json()
                print(f"Found {len(assignments)} assignments")
                
                # Use the first assignment ID for submission test
                assignment_id = assignments[0]['id'] if assignments else 1
                print_debug(f"Using assignment ID {assignment_id} for submission test")
            else:
                print(f"❌ Failed to fetch assignments: {assignments_response.text}")
                assignment_id = 1  # Fallback ID
            
            # Step 3: Test fetching user's submissions
            print("\nStep 3: Fetching user submissions...")
            print_debug(f"Cookies before submissions request: {session.cookies.get_dict()}")
            submissions_response = session.get(
                f"{base_url}/api/assignments/my-submissions",
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"SESSION={session.cookies.get('SESSION')}"
                }
            )
            print(f"Submissions status code: {submissions_response.status_code}")
            
            if submissions_response.status_code == 200:
                print("✅ Successfully fetched user submissions")
                submissions = submissions_response.json()
                print(f"Found {len(submissions)} submissions")
            else:
                print(f"❌ Failed to fetch submissions: {submissions_response.text}")
            
            # Step 4: Test submitting an assignment
            print("\nStep 4: Submitting an assignment...")
            submission_data = {
                "assignmentId": assignment_id,
                "submissionContent": f"Test submission content - {time.time()}",
                "submissionType": "text"
            }
            print_debug(f"Submission data: {submission_data}")
            print_debug(f"Cookies before submission: {session.cookies.get_dict()}")
            
            submit_response = session.post(
                f"{base_url}/api/assignments/submit", 
                json=submission_data,
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"SESSION={session.cookies.get('SESSION')}"
                }
            )
            print(f"Submission status code: {submit_response.status_code}")
            
            if submit_response.status_code == 200:
                print("✅ Successfully submitted assignment")
                print_debug(f"Submission response: {submit_response.json()}")
            else:
                print(f"❌ Failed to submit assignment: {submit_response.text}")
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_login_and_permissions()
