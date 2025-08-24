#!/usr/bin/env python3

import requests
import json

BASE_URL = 'http://localhost:5555'

def test_endpoints():
    print("Testing endpoints...")
    
    # Test health check
    try:
        response = requests.get(BASE_URL)
        print(f"✓ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # Test GET /workouts
    try:
        response = requests.get(f'{BASE_URL}/workouts')
        print(f"✓ GET /workouts: {response.status_code}")
    except Exception as e:
        print(f"✗ GET /workouts failed: {e}")
    
    # Test GET /exercises
    try:
        response = requests.get(f'{BASE_URL}/exercises')
        print(f"✓ GET /exercises: {response.status_code}")
    except Exception as e:
        print(f"✗ GET /exercises failed: {e}")
    
    print("Endpoint testing completed. Start the server with 'python server/app.py' to test fully.")

if __name__ == '__main__':
    test_endpoints()