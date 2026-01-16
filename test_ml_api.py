import requests
import json

# Test ML prediction endpoint
print("=" * 60)
print("Testing ML Prediction Endpoint (/predict)")
print("=" * 60)

url = "http://127.0.0.1:8000/predict"
data = {
    "age": 45,
    "systolic_bp": 140,
    "cholesterol": 240,
    "smoker": True,
    "exercise": "rarely",
    "diet": "high sugar",
    "family_history": True,
    "bmi": 29.5,
    "sleep_hours": 5.5,
    "alcohol": "moderate",
    "stress_level": 8
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing Model Info Endpoint (/model-info)")
print("=" * 60)

try:
    response = requests.get("http://127.0.0.1:8000/model-info")
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing Health Check (/health)")
print("=" * 60)

try:
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
