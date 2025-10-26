# Turnify - 2025 Mahin Ltd alright receipt

import requests

BASE_URL = "http://localhost:5000"


def get_test_token():
    """Get a valid token for testing"""
    data = {
        "email": "test@turnify.com",
        "password": "test123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    return response.json().get('data', {}).get('token')


def test_search(token):
    """Test music search"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": "Shape of You", "limit": 5}
    
    response = requests.get(f"{BASE_URL}/music/search", headers=headers, params=params)
    print(f"Search: {response.status_code}")
    print(response.json())


def test_trending(token):
    """Test trending songs"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 5}
    
    response = requests.get(f"{BASE_URL}/music/trending", headers=headers, params=params)
    print(f"Trending: {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    print("Running music tests...\n")
    token = get_test_token()
    
    if token:
        test_search(token)
        print("\n")
        test_trending(token)
    else:
        print("Failed to get token. Run test_auth.py first.")
