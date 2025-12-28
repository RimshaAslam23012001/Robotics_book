import requests
import json

def test_auth():
    base_url = "http://localhost:8000"

    print("Testing authentication endpoints...")

    # Test signup
    print("\n1. Testing Signup:")
    signup_data = {
        "email": "test@example.com",
        "password": "TestPass123",  # Less than 72 characters
        "name": "Test User",
        "profileData": {
            "softwareBackground": "beginner",
            "programmingLanguages": ["Python", "JavaScript"],
            "aiMlExperience": "learning",
            "hardwareBackground": "none",
            "primaryLearningGoal": "Learn AI concepts"
        }
    }

    try:
        response = requests.post(f"{base_url}/api/auth/signup", json=signup_data)
        print(f"Signup response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Signup successful!")
            print(f"User ID: {result['user']['id']}")
            token = result.get('session', {}).get('token')
            print(f"Token received: {bool(token)}")
        else:
            print(f"Signup failed: {response.text}")
    except Exception as e:
        print(f"Signup error: {e}")

    # Test signin
    print("\n2. Testing Signin:")
    signin_data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }

    try:
        response = requests.post(f"{base_url}/api/auth/signin", json=signin_data)
        print(f"Signin response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Signin successful!")
            print(f"User ID: {result['user']['id']}")
            token = result.get('session', {}).get('token')
            print(f"Token received: {bool(token)}")
        else:
            print(f"Signin failed: {response.text}")
    except Exception as e:
        print(f"Signin error: {e}")

    print("\n3. Testing endpoints availability:")
    endpoints = [
        "/api/auth/signup",
        "/api/auth/signin",
        "/api/auth/signout",
        "/api/auth/me"
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

    print("\nAuthentication test completed!")

if __name__ == "__main__":
    test_auth()