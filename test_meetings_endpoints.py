#!/usr/bin/env python3
"""
Simple script to test the meetings API endpoints
"""
import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, params=None, data=None, expected_status=200):
    """Test an API endpoint and print the results"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n=== Testing {method.upper()} {endpoint} ===")
    
    try:
        if method.lower() == 'get':
            response = requests.get(url, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, json=data)
        elif method.lower() == 'put':
            response = requests.put(url, json=data)
        elif method.lower() == 'delete':
            response = requests.delete(url)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        print(f"Status Code: {response.status_code} (Expected: {expected_status})")
        
        if response.status_code == expected_status:
            if response.status_code != 204:  # No content
                try:
                    print(json.dumps(response.json(), indent=2))
                except:
                    print(response.text)
            print("✅ Test passed")
            return True
        else:
            print(f"❌ Test failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=== MEETINGS API ENDPOINT TESTS ===")
    
    # Test meeting types endpoint
    test_endpoint('get', '/api/meetings/types')
    
    # Test upcoming meetings endpoint
    test_endpoint('get', '/api/meetings/upcoming')
    
    # Test list meetings with filters
    today = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    test_endpoint('get', '/api/meetings/', params={
        'start_date': today,
        'end_date': end_date
    })
    
    # Test faculty endpoint
    test_endpoint('get', '/api/meetings/faculty')
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
