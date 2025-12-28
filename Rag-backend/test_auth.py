import asyncio
import httpx
import json

async def test_auth_endpoints():
    base_url = "http://localhost:8000"

    print("Testing Better Auth Integration...")

    # Test signup endpoint
    print("\n1. Testing Signup endpoint...")
    signup_data = {
        "email": "test@example.com",
        "password": "TestPass123!",
        "name": "Test User",
        "profile_data": {
            "softwareBackground": "beginner",
            "programmingLanguages": ["Python", "JavaScript"],
            "aiMlExperience": "learning",
            "hardwareBackground": "none",
            "primaryLearningGoal": "Learn AI concepts"
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/auth/signup",
                json=signup_data,
                timeout=30.0
            )
            print(f"Signup response: {response.status_code}")
            if response.status_code == 200:
                signup_result = response.json()
                print("Signup successful!")
                token = signup_result.get("session", {}).get("token")
                print(f"Token received: {bool(token)}")
            else:
                print(f"Signup failed: {response.text}")
    except Exception as e:
        print(f"Signup error: {e}")

    # Test signin endpoint
    print("\n2. Testing Signin endpoint...")
    signin_data = {
        "email": "test@example.com",
        "password": "TestPass123!"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/auth/signin",
                json=signin_data,
                timeout=30.0
            )
            print(f"Signin response: {response.status_code}")
            if response.status_code == 200:
                signin_result = response.json()
                print("Signin successful!")
                token = signin_result.get("session", {}).get("token")
                print(f"Token received: {bool(token)}")
            else:
                print(f"Signin failed: {response.text}")
    except Exception as e:
        print(f"Signin error: {e}")

    print("\n3. Testing Auth endpoints availability...")

    # Check if auth endpoints are available
    endpoints = [
        "/api/auth/signup",
        "/api/auth/signin",
        "/api/auth/signout",
        "/api/auth/me"
    ]

    for endpoint in endpoints:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}{endpoint}")
                print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

    print("\nAuthentication integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_auth_endpoints())