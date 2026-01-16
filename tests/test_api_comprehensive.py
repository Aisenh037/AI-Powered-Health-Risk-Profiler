"""
Comprehensive Automated Test Suite for Health Risk Profiler API
Tests all endpoints with various scenarios and validates responses
"""

import requests
import json
import time
from typing import Dict, Any, List
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name: str, passed: bool, message: str = ""):
        self.tests.append({"name": name, "passed": passed, "message": message})
        if passed:
            self.passed += 1
            print(f"{Colors.GREEN}✓{Colors.RESET} {name}")
        else:
            self.failed += 1
            print(f"{Colors.RED}✗{Colors.RESET} {name} - {message}")
    
    def print_summary(self):
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print("\n" + "="*60)
        print(f"{Colors.BLUE}TEST SUMMARY{Colors.RESET}")
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print(f"Success Rate: {success_rate:.1f}%")
        print("="*60 + "\n")

results = TestResults()

def test_health_check():
    """Test 1: Health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "healthy" and data.get("ml_available"):
            results.add_result("Health Check", True)
            return True
        else:
            results.add_result("Health Check", False, f"Unexpected response: {data}")
            return False
    except Exception as e:
        results.add_result("Health Check", False, str(e))
        return False

def test_model_info():
    """Test 2: Model info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/model-info", timeout=5)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("Model Info", False, f"Status code: {response.status_code}")
            return False
        
        # Verify all models loaded
        expected_models = ["random_forest", "xgboost", "neural_network"]
        if set(data["models_loaded"]) != set(expected_models):
            results.add_result("Model Info", False, "Not all models loaded")
            return False
        
        # Verify performance metrics
        for model in expected_models:
            if model not in data["performance"]:
                results.add_result("Model Info", False, f"Missing performance for {model}")
                return False
            
            perf = data["performance"][model]
            if perf["accuracy"] < 0.8 or perf["f1_score"] < 0.8:
                results.add_result("Model Info", False, f"Low performance for {model}")
                return False
        
        results.add_result("Model Info", True)
        return True
    except Exception as e:
        results.add_result("Model Info", False, str(e))
        return False

def test_analyze_high_risk():
    """Test 3: Rule-based high risk prediction"""
    try:
        payload = {
            "age": 55,
            "smoker": True,
            "exercise": "never",
            "diet": "high fat"
        }
        
        response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=5)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("Analyze High Risk", False, f"Status: {response.status_code}")
            return False
        
        if data["risk_level"] != "high":
            results.add_result("Analyze High Risk", False, f"Expected high, got {data['risk_level']}")
            return False
        
        if len(data["factors"]) < 2:
            results.add_result("Analyze High Risk", False, "Too few factors identified")
            return False
        
        results.add_result("Analyze High Risk", True)
        return True
    except Exception as e:
        results.add_result("Analyze High Risk", False, str(e))
        return False

def test_analyze_low_risk():
    """Test 4: Rule-based low risk prediction"""
    try:
        payload = {
            "age": 25,
            "smoker": False,
            "exercise": "daily",
            "diet": "balanced"
        }
        
        response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=5)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("Analyze Low Risk", False, f"Status: {response.status_code}")
            return False
        
        if data["risk_level"] != "low":
            results.add_result("Analyze Low Risk", False, f"Expected low, got {data['risk_level']}")
            return False
        
        results.add_result("Analyze Low Risk", True)
        return True
    except Exception as e:
        results.add_result("Analyze Low Risk", False, str(e))
        return False

def test_ml_predict_high_risk():
    """Test 5: ML-based high risk prediction"""
    try:
        payload = {
            "age": 58,
            "bmi": 32.5,
            "systolic_bp": 160,
            "cholesterol": 280,
            "smoker": True,
            "exercise": "never",
            "diet": "high fat",
            "family_history": True,
            "sleep_hours": 5.0,
            "alcohol": "heavy",
            "stress_level": 9
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("ML Predict High Risk", False, f"Status: {response.status_code}")
            return False
        
        # Verify structure
        required_fields = ["risk_level", "risk_score", "confidence", "probabilities", 
                          "model_predictions", "top_contributing_factors"]
        for field in required_fields:
            if field not in data:
                results.add_result("ML Predict High Risk", False, f"Missing field: {field}")
                return False
        
        # Verify risk level
        if data["risk_level"] not in ["medium", "high"]:
            results.add_result("ML Predict High Risk", False, f"Unexpected risk: {data['risk_level']}")
            return False
        
        # Verify confidence
        if data["confidence"] < 0.5 or data["confidence"] > 1.0:
            results.add_result("ML Predict High Risk", False, f"Invalid confidence: {data['confidence']}")
            return False
        
        # Verify top factors
        if len(data["top_contributing_factors"]) != 5:
            results.add_result("ML Predict High Risk", False, "Should have 5 top factors")
            return False
        
        results.add_result("ML Predict High Risk", True)
        return True
    except Exception as e:
        results.add_result("ML Predict High Risk", False, str(e))
        return False

def test_ml_predict_low_risk():
    """Test 6: ML-based low risk prediction"""
    try:
        payload = {
            "age": 28,
            "bmi": 22.0,
            "systolic_bp": 110,
            "cholesterol": 170,
            "smoker": False,
            "exercise": "daily",
            "diet": "balanced",
            "family_history": False,
            "sleep_hours": 8.0,
            "alcohol": "none",
            "stress_level": 2
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("ML Predict Low Risk", False, f"Status: {response.status_code}")
            return False
        
        if data["risk_level"] != "low":
            results.add_result("ML Predict Low Risk", False, f"Expected low, got {data['risk_level']}")
            return False
        
        # Low risk should have high probability for "low"
        if data["probabilities"]["low"] < 0.6:
            results.add_result("ML Predict Low Risk", False, "Low probability too low")
            return False
        
        results.add_result("ML Predict Low Risk", True)
        return True
    except Exception as e:
        results.add_result("ML Predict Low Risk", False, str(e))
        return False

def test_ml_borderline_case():
    """Test 7: ML borderline case (medium risk)"""
    try:
        payload = {
            "age": 40,
            "bmi": 26.0,
            "systolic_bp": 130,
            "cholesterol": 210,
            "smoker": False,
            "exercise": "occasionally",
            "diet": "balanced",
            "family_history": False,
            "sleep_hours": 7.0,
            "alcohol": "light",
            "stress_level": 5
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("ML Borderline Case", False, f"Status: {response.status_code}")
            return False
        
        # Should be low or medium
        if data["risk_level"] not in ["low", "medium"]:
            results.add_result("ML Borderline Case", False, f"Unexpected risk: {data['risk_level']}")
            return False
        
        results.add_result("ML Borderline Case", True)
        return True
    except Exception as e:
        results.add_result("ML Borderline Case", False, str(e))
        return False

def test_ml_minimal_input():
    """Test 8: ML with minimal input (defaults)"""
    try:
        payload = {
            "age": 50
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            results.add_result("ML Minimal Input", False, f"Status: {response.status_code}")
            return False
        
        # Should work with defaults
        if "risk_level" not in data:
            results.add_result("ML Minimal Input", False, "No risk_level in response")
            return False
        
        results.add_result("ML Minimal Input", True)
        return True
    except Exception as e:
        results.add_result("ML Minimal Input", False, str(e))
        return False

def test_performance():
    """Test 9: Response time performance"""
    try:
        payload = {
            "age": 45,
            "bmi": 25.0,
            "systolic_bp": 120,
            "cholesterol": 200,
            "smoker": False,
            "exercise": "occasionally",
            "diet": "balanced",
            "family_history": False,
            "sleep_hours": 7.0,
            "alcohol": "none",
            "stress_level": 5
        }
        
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=10)
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code != 200:
            results.add_result("Performance Test", False, "Request failed")
            return False
        
        # Should respond within 1 second
        if elapsed_time > 1000:
            results.add_result("Performance Test", False, f"Too slow: {elapsed_time:.0f}ms")
            return False
        
        results.add_result("Performance Test", True, f"({elapsed_time:.0f}ms)")
        return True
    except Exception as e:
        results.add_result("Performance Test", False, str(e))
        return False

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print(f"{Colors.BLUE}AI-Powered Health Risk Profiler - Automated Test Suite{Colors.RESET}")
    print("="*60 + "\n")
    print(f"Starting tests at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}\n")
    
    # Run all tests
    test_health_check()
    test_model_info()
    test_analyze_high_risk()
    test_analyze_low_risk()
    test_ml_predict_high_risk()
    test_ml_predict_low_risk()
    test_ml_borderline_case()
    test_ml_minimal_input()
    test_performance()
    
    # Print summary
    results.print_summary()
    
    # Save test report
    save_test_report()

def save_test_report():
    """Save test results to file"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": results.passed + results.failed,
        "passed": results.passed,
        "failed": results.failed,
        "success_rate": (results.passed / (results.passed + results.failed) * 100) if (results.passed + results.failed) > 0 else 0,
        "tests": results.tests
    }
    
    with open("test_results.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Test report saved to: test_results.json\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
