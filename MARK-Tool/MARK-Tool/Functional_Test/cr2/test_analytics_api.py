"""
Example script to test Analytics API endpoints
"""
import requests
import json


# Configuration
BASE_URL = "http://127.0.0.1:5000"
OUTPUT_PATH = "C:/Users/turco/Desktop/IGES/MARK-IGES/MARK-Tool/MARK-Tool/Categorizer/results"


def test_analytics_health():
    """Test analytics health check"""
    print("\n=== Testing Analytics Health ===")
    response = requests.get(f"{BASE_URL}/api/analytics/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_summary():
    """Test get summary endpoint"""
    print("\n=== Testing Get Summary ===")
    params = {"output_path": OUTPUT_PATH}
    response = requests.get(f"{BASE_URL}/api/analytics/summary", params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_distribution():
    """Test get consumer/producer distribution"""
    print("\n=== Testing Get Distribution ===")
    params = {"output_path": OUTPUT_PATH}
    response = requests.get(
        f"{BASE_URL}/api/analytics/consumer-producer-distribution",
        params=params
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_keywords():
    """Test get top keywords"""
    print("\n=== Testing Get Keywords ===")
    params = {"output_path": OUTPUT_PATH, "limit": 10}
    response = requests.get(f"{BASE_URL}/api/analytics/keywords", params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_libraries():
    """Test get library distribution"""
    print("\n=== Testing Get Libraries ===")
    params = {"output_path": OUTPUT_PATH, "limit": 10}
    response = requests.get(f"{BASE_URL}/api/analytics/libraries", params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_filter_by_type():
    """Test filter results by type"""
    print("\n=== Testing Filter by Type (Consumer) ===")
    params = {
        "output_path": OUTPUT_PATH,
        "type": "consumer",
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/api/analytics/filter", params=params)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Count: {result.get('count')}")
    print(f"Filters Applied: {json.dumps(result.get('filters_applied'), indent=2)}")
    if result.get('results'):
        print(f"First Result: {json.dumps(result['results'][0], indent=2)}")


def test_filter_by_keyword():
    """Test filter results by keyword"""
    print("\n=== Testing Filter by Keyword ===")
    params = {
        "output_path": OUTPUT_PATH,
        "keyword": ".predict(",
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/api/analytics/filter", params=params)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Count: {result.get('count')}")
    print(f"Filters Applied: {json.dumps(result.get('filters_applied'), indent=2)}")


def test_filter_by_library():
    """Test filter results by library"""
    print("\n=== Testing Filter by Library ===")
    params = {
        "output_path": OUTPUT_PATH,
        "library": "tensorflow",
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/api/analytics/filter", params=params)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Count: {result.get('count')}")
    print(f"Filters Applied: {json.dumps(result.get('filters_applied'), indent=2)}")


def test_combined_filters():
    """Test combined filters"""
    print("\n=== Testing Combined Filters ===")
    params = {
        "output_path": OUTPUT_PATH,
        "type": "consumer",
        "library": "tensorflow",
        "keyword": ".predict(",
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/api/analytics/filter", params=params)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Count: {result.get('count')}")
    print(f"Filters Applied: {json.dumps(result.get('filters_applied'), indent=2)}")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("MARK Analytics API - Test Suite")
    print("=" * 60)
    
    try:
        test_analytics_health()
        test_get_summary()
        test_get_distribution()
        test_get_keywords()
        test_get_libraries()
        test_filter_by_type()
        test_filter_by_keyword()
        test_filter_by_library()
        test_combined_filters()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the API server.")
        print(f"Make sure the server is running at {BASE_URL}")
    except Exception as e:
        print(f"\nERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
