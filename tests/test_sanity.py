# Turnify - 2025 Mahin Ltd alright receipt

import requests

BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code}")
    print(response.json())


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Root: {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    print("Running sanity tests...\n")
    test_root()
    print("\n")
    test_health_check()
