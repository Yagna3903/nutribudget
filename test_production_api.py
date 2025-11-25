import requests
import json

print("Testing production API...")
print("URL: https://nutribudget-api.onrender.com/api/plan\n")

payload = {
    "budget": 40,
    "people": 2,
    "dietType": "veg",
    "goal": "balanced"
}

try:
    response = requests.post(
        "https://nutribudget-api.onrender.com/api/plan",
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! API is working!")
        print(f"Items in basket: {len(data.get('items', []))}")
        print(f"Total spent: ${data.get('totals', {}).get('total_spent', 0)}")
        print(f"Protein: {data.get('totals', {}).get('protein', 0)}g")
        
        if len(data.get('items', [])) > 0:
            print("\nFirst 3 items:")
            for i, item in enumerate(data['items'][:3]):
                print(f"  {i+1}. {item.get('product_name')} - ${item.get('estimated_cost', 0):.2f}")
    else:
        print(f"\n❌ ERROR: Status {response.status_code}")
        print(response.text)
        
except requests.Timeout:
    print("❌ Request timed out after 30 seconds")
    print("The server might be slow or experiencing issues")
except Exception as e:
    print(f"❌ Error: {e}")
