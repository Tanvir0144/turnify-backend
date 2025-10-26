# Turnify - 2025 Mahin Ltd alright receipt

import requests
import random

BASE_URL = "http://localhost:5000"


def test_register():
    """Test user registration"""
    random_num = random.randint(1000, 9999)
    
    data = {
        "username": f"testuser{random_num}",
        "email": f"test{random_num}@turnify.com",
        "password": "test123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Register: {response.status_code}")
    print(response.json())
    
    return response.json().get('data', {}).get('token')


def test_login():
    """Test user login"""
    data = {
        "email": "test@turnify.com",
        "password": "test123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Login: {response.status_code}")
    print(response.json())
    
    return response.json().get('data', {}).get('token')


def test_verify(token):
    """Test token verification"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/verify", headers=headers)
    print(f"Verify: {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    print("Running auth tests...\n")
    token = test_register()
    print("\n")
    if token:
        test_verify(token)
