#!/usr/bin/env python3
"""Test API endpoint with ML models"""
import requests
import json

# Test API endpoint
url = "http://localhost:5000/api/plan"
payload = {
    "budget": 75,
    "people": 1,
    "dietType": "veg",
    "goal": "high_protein"
}

try:
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ API Test Successful!")
        print(f"   Items: {len(data['items'])}")
        print(f"   Total Spent: ${data['totals']['total_spent']:.2f}")
        print(f"   Protein: {data['totals']['protein']}g")
        print(f"   Calories: {data['totals']['calories']}")
        print(f"\n   Top 5 Items:")
        for i, item in enumerate(data['items'][:5], 1):
            print(f"   {i}. {item['product_name']} - ${item['estimated_cost']:.2f}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
except requests.exceptions.ConnectionError:
    print("❌ Backend not running. Start with: python3 app.py")
except Exception as e:
    print(f"❌ Error: {e}")
