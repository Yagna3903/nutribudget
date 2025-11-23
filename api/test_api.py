"""
NutriBudget API Testing Script

This script tests all API endpoints with various scenarios including:
- Health check
- Foods filtering
- Plan generation with different parameters
- Statistics retrieval
- Edge cases and error handling

Run this script with the API server running on http://localhost:5000
"""

import requests
import json
from typing import Dict, Any
import time

BASE_URL = "http://localhost:5000"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name: str):
    """Print test name"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Testing: {name}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")

def test_health_endpoint():
    """Test the health check endpoint"""
    print_test("Health Check Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print_success("Health endpoint returned 200 OK")
                print_info(f"Response: {json.dumps(data, indent=2)}")
            else:
                print_error(f"Unexpected response: {data}")
        else:
            print_error(f"Expected 200, got {response.status_code}")
    except Exception as e:
        print_error(f"Failed to connect: {e}")

def test_foods_endpoint():
    """Test the foods endpoint with various filters"""
    print_test("Foods Endpoint - Various Filters")
    
    test_cases = [
        {
            "name": "Get all foods (limit 10)",
            "params": {"limit": 10}
        },
        {
            "name": "Filter by vegetarian",
            "params": {"veg_nonveg": "veg", "limit": 10}
        },
        {
            "name": "Filter by non-vegetarian",
            "params": {"veg_nonveg": "non-veg", "limit": 10}
        },
        {
            "name": "Filter by max price",
            "params": {"max_price_per_100g": 1.0, "limit": 10}
        },
        {
            "name": "Filter by cluster 0",
            "params": {"cluster": 0, "limit": 10}
        },
        {
            "name": "Filter by store",
            "params": {"store": "costco", "limit": 10}
        },
        {
            "name": "Combined filters",
            "params": {"veg_nonveg": "veg", "max_price_per_100g": 0.8, "limit": 5}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        try:
            response = requests.get(f"{BASE_URL}/api/foods", params=test_case['params'])
            
            if response.status_code == 200:
                data = response.json()
                count = data.get("count", 0)
                print_success(f"Returned {count} items")
                
                if count > 0 and "items" in data:
                    first_item = data["items"][0]
                    print_info(f"Sample item: {first_item.get('product_name', 'N/A')}")
            else:
                print_error(f"Status code: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {e}")

def test_stats_endpoint():
    """Test the statistics endpoint"""
    print_test("Statistics Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Stats endpoint returned successfully")
            
            # Check for expected fields
            if "total_products" in data:
                print_info(f"Total products: {data['total_products']}")
            if "avg_price_per_100g" in data:
                print_info(f"Average price per 100g: ${data['avg_price_per_100g']}")
            if "cluster_distribution" in data:
                print_info(f"Number of clusters: {len(data['cluster_distribution'])}")
            if "category_distribution" in data:
                print_info(f"Number of categories: {len(data['category_distribution'])}")
                
            print(f"\nFull response:\n{json.dumps(data, indent=2)[:500]}...")
        else:
            print_error(f"Status code: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_plan_endpoint():
    """Test the plan generation endpoint with various scenarios"""
    print_test("Plan Generation Endpoint - Various Scenarios")
    
    test_cases = [
        {
            "name": "Budget-conscious student (veg, $30)",
            "data": {"budget": 30, "people": 1, "dietType": "veg", "goal": "balanced"}
        },
        {
            "name": "Family of 3 (mixed, $50)",
            "data": {"budget": 50, "people": 3, "dietType": "mixed", "goal": "balanced"}
        },
        {
            "name": "High protein athlete (non-veg, $40)",
            "data": {"budget": 40, "people": 1, "dietType": "nonveg", "goal": "high_protein"}
        },
        {
            "name": "Low sugar diet (veg, $35)",
            "data": {"budget": 35, "people": 2, "dietType": "veg", "goal": "low_sugar"}
        },
        {
            "name": "Large family (mixed, $100)",
            "data": {"budget": 100, "people": 5, "dietType": "mixed", "goal": "balanced"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/plan",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Plan generated in {elapsed_time:.2f}s")
                
                if "basket" in data:
                    print_info(f"Basket items: {len(data['basket'])}")
                
                if "totals" in data:
                    totals = data["totals"]
                    print_info(f"Budget: ${totals.get('budget', 0)}, Spent: ${totals.get('cost', 0):.2f}")
                    print_info(f"Calories: {totals.get('calories', 0):.0f}, Protein: {totals.get('protein', 0):.1f}g")
                
                if "clusterBreakdown" in data:
                    print_info(f"Cluster breakdown: {len(data['clusterBreakdown'])} clusters")
            else:
                print_error(f"Status code: {response.status_code}")
                print_error(f"Response: {response.text}")
        except Exception as e:
            print_error(f"Error: {e}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print_test("Edge Cases and Error Handling")
    
    test_cases = [
        {
            "name": "Very low budget ($5)",
            "data": {"budget": 5, "people": 1, "dietType": "veg", "goal": "balanced"},
            "expected_status": 400
        },
        {
            "name": "Zero budget",
            "data": {"budget": 0, "people": 1, "dietType": "veg", "goal": "balanced"},
            "expected_status": 400
        },
        {
            "name": "Negative budget",
            "data": {"budget": -10, "people": 1, "dietType": "veg", "goal": "balanced"},
            "expected_status": 400
        },
        {
            "name": "Zero people",
            "data": {"budget": 50, "people": 0, "dietType": "veg", "goal": "balanced"},
            "expected_status": 400
        },
        {
            "name": "Invalid diet type",
            "data": {"budget": 50, "people": 2, "dietType": "invalid", "goal": "balanced"},
            "expected_status": [200, 400]  # May accept or reject
        },
        {
            "name": "Missing required fields",
            "data": {"budget": 50},
            "expected_status": 400
        },
        {
            "name": "Very high budget ($500)",
            "data": {"budget": 500, "people": 1, "dietType": "veg", "goal": "balanced"},
            "expected_status": 200
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        try:
            response = requests.post(
                f"{BASE_URL}/api/plan",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            expected = test_case['expected_status']
            if isinstance(expected, list):
                if response.status_code in expected:
                    print_success(f"Status code {response.status_code} (expected one of {expected})")
                else:
                    print_error(f"Status code {response.status_code} (expected one of {expected})")
            else:
                if response.status_code == expected:
                    print_success(f"Status code {response.status_code} (expected)")
                else:
                    print_error(f"Status code {response.status_code} (expected {expected})")
            
            if response.status_code >= 400:
                error_data = response.json()
                print_info(f"Error message: {error_data.get('error', 'No error message')}")
        except Exception as e:
            print_error(f"Error: {e}")

def test_performance():
    """Test API performance with multiple requests"""
    print_test("Performance Testing")
    
    print("\nTesting /api/plan endpoint performance (10 requests):")
    times = []
    
    for i in range(10):
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/plan",
                json={"budget": 50, "people": 2, "dietType": "veg", "goal": "balanced"},
                headers={"Content-Type": "application/json"}
            )
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)
            
            if response.status_code == 200:
                print(f"  Request {i+1}: {elapsed_time:.3f}s")
            else:
                print_error(f"  Request {i+1} failed with status {response.status_code}")
        except Exception as e:
            print_error(f"  Request {i+1} error: {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n{Colors.GREEN}Performance Summary:{Colors.RESET}")
        print_info(f"Average response time: {avg_time:.3f}s")
        print_info(f"Min response time: {min_time:.3f}s")
        print_info(f"Max response time: {max_time:.3f}s")

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}NutriBudget API Test Suite{Colors.RESET}")
    print(f"{Colors.BLUE}Testing API at: {BASE_URL}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.RequestException:
        print_error(f"\nCannot connect to API at {BASE_URL}")
        print_error("Please make sure the Flask server is running:")
        print_error("  cd api")
        print_error("  python app.py")
        return
    
    # Run all tests
    test_health_endpoint()
    test_foods_endpoint()
    test_stats_endpoint()
    test_plan_endpoint()
    test_edge_cases()
    test_performance()
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}All tests completed!{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
