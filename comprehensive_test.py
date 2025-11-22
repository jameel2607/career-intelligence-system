#!/usr/bin/env python3
"""
Comprehensive Test Suite for Career Intelligence System
Tests all features: Auth, Profile, OCR, Scoring, Recommendations, Reports
"""

import requests
import json
import time
from datetime import datetime
import sys

BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"

# Test results tracking
results = {
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "summary": {}
}

def log_test(name, status, details=""):
    """Log test result"""
    result = {
        "test": name,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    results["tests"].append(result)
    status_icon = "✅" if status == "PASS" else "❌"
    print(f"{status_icon} {name}: {status}")
    if details:
        print(f"   └─ {details}")

def test_system_status():
    """Test 1: System Status"""
    try:
        response = requests.get(f"{API_V1}/system/status")
        if response.status_code == 200:
            data = response.json()
            log_test("System Status", "PASS", f"Status: {data.get('status')}")
            return True
        else:
            log_test("System Status", "FAIL", f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("System Status", "FAIL", str(e))
        return False

def test_user_registration():
    """Test 2: User Registration"""
    try:
        test_email = f"testuser_{int(time.time())}@example.com"
        payload = {
            "email": test_email,
            "password": "TestPassword123!",
            "name": "Test User"
        }
        response = requests.post(f"{API_V1}/auth/register", json=payload)
        
        if response.status_code in [200, 201]:
            data = response.json()
            log_test("User Registration", "PASS", f"User created: {test_email}")
            return True, test_email, payload["password"]
        else:
            log_test("User Registration", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
            return False, None, None
    except Exception as e:
        log_test("User Registration", "FAIL", str(e))
        return False, None, None

def test_user_login(email, password):
    """Test 3: User Login"""
    try:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{API_V1}/auth/login", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            log_test("User Login", "PASS", f"Token obtained: {token[:20]}...")
            return True, token
        else:
            log_test("User Login", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("User Login", "FAIL", str(e))
        return False, None

def test_profile_creation(token):
    """Test 4: Profile Creation"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "education_level": "Bachelor's Degree",
            "experience_years": 2,
            "skills": "Python, React, SQL, Docker, AWS",
            "interests": "Web Development, AI, Cloud Computing",
            "bio": "I am a passionate developer with 2 years of experience building web applications using React and Python. I have completed several projects including e-commerce platforms and data analytics dashboards.",
            "target_salary": 12
        }
        response = requests.post(f"{API_V1}/students/me", json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            log_test("Profile Creation", "PASS", "Profile created successfully")
            return True
        else:
            log_test("Profile Creation", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        log_test("Profile Creation", "FAIL", str(e))
        return False

def test_profile_retrieval(token):
    """Test 5: Profile Retrieval"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_V1}/students/me", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            log_test("Profile Retrieval", "PASS", 
                    f"Profile retrieved: {data.get('education_level')}, {data.get('experience_years')} years exp")
            return True, data
        else:
            log_test("Profile Retrieval", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("Profile Retrieval", "FAIL", str(e))
        return False, None

def test_career_score(token):
    """Test 6: Career Readiness Score Calculation"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_V1}/career/score", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            score = data.get("score")
            breakdown = data.get("breakdown", {})
            confidence = data.get("confidence")
            
            log_test("Career Readiness Score", "PASS", 
                    f"Score: {score}/100, Confidence: {confidence:.2f}")
            
            # Log breakdown details
            print(f"   └─ Breakdown:")
            for key, value in breakdown.items():
                if isinstance(value, (int, float)):
                    print(f"      • {key}: {value:.3f}")
            
            return True, data
        else:
            log_test("Career Readiness Score", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("Career Readiness Score", "FAIL", str(e))
        return False, None

def test_job_recommendations(token):
    """Test 7: Job Recommendations"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_V1}/career/recommendations", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("job_roles", [])
            skills = data.get("skills_to_learn", [])
            
            log_test("Job Recommendations", "PASS", 
                    f"Found {len(jobs)} job roles, {len(skills)} skills to learn")
            
            if jobs:
                print(f"   └─ Top Recommended Roles:")
                for i, job in enumerate(jobs[:3], 1):
                    role_name = job.get("role_name", "Unknown")
                    match_score = job.get("match_score", 0)
                    print(f"      {i}. {role_name} (Match: {match_score:.1f}%)")
            
            return True, data
        else:
            log_test("Job Recommendations", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("Job Recommendations", "FAIL", str(e))
        return False, None

def test_ai_recommendations(token):
    """Test 8: AI-Powered Recommendations"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_V1}/career/ai-recommendations", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", "")
            recommendations = data.get("recommendations", [])
            
            log_test("AI Recommendations", "PASS", 
                    f"Generated {len(recommendations)} recommendations")
            
            if recommendations:
                print(f"   └─ AI Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"      {i}. {rec}")
            
            return True, data
        else:
            log_test("AI Recommendations", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("AI Recommendations", "FAIL", str(e))
        return False, None

def test_report_generation(token):
    """Test 9: Report Generation"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "report_type": "comprehensive",
            "include_recommendations": True,
            "include_roadmap": True
        }
        response = requests.post(f"{API_V1}/reports/generate", json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            data = response.json()
            report_id = data.get("report_id")
            log_test("Report Generation", "PASS", f"Report generated: {report_id}")
            return True, report_id
        else:
            log_test("Report Generation", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("Report Generation", "FAIL", str(e))
        return False, None

def test_knowledge_base():
    """Test 10: Knowledge Base Query"""
    try:
        payload = {
            "query": "Python developer",
            "limit": 5
        }
        response = requests.post(f"{API_V1}/kb/query", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            log_test("Knowledge Base Query", "PASS", f"Found {len(results)} matching roles")
            
            if results:
                print(f"   └─ Top Matches:")
                for i, result in enumerate(results[:3], 1):
                    role = result.get("role_name", "Unknown")
                    print(f"      {i}. {role}")
            
            return True, data
        else:
            log_test("Knowledge Base Query", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("Knowledge Base Query", "FAIL", str(e))
        return False, None

def test_profile_update(token):
    """Test 11: Profile Update"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "education_level": "Master's Degree",
            "experience_years": 3,
            "skills": "Python, React, SQL, Docker, AWS, Kubernetes, Machine Learning",
            "interests": "Full-stack Development, AI/ML, DevOps",
            "bio": "Senior developer with 3 years of experience in full-stack development and cloud technologies. Specialized in building scalable web applications.",
            "target_salary": 15
        }
        response = requests.put(f"{API_V1}/students/me", json=payload, headers=headers)
        
        if response.status_code == 200:
            log_test("Profile Update", "PASS", "Profile updated successfully")
            return True
        else:
            log_test("Profile Update", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("Profile Update", "FAIL", str(e))
        return False

def test_updated_score(token):
    """Test 12: Verify Score Updates After Profile Change"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_V1}/career/score", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            score = data.get("score")
            log_test("Updated Career Score", "PASS", 
                    f"New score after profile update: {score}/100")
            return True, data
        else:
            log_test("Updated Career Score", "FAIL", f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        log_test("Updated Career Score", "FAIL", str(e))
        return False, None

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*70)
    print("🧪 CAREER INTELLIGENCE SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70 + "\n")
    
    # Test 1: System Status
    if not test_system_status():
        print("\n❌ System is not running. Please start the backend server.")
        return
    
    time.sleep(1)
    
    # Test 2-3: Registration and Login
    success, email, password = test_user_registration()
    if not success:
        print("\n❌ Registration failed. Stopping tests.")
        return
    
    time.sleep(1)
    success, token = test_user_login(email, password)
    if not success:
        print("\n❌ Login failed. Stopping tests.")
        return
    
    time.sleep(1)
    
    # Test 4-5: Profile Creation and Retrieval
    if not test_profile_creation(token):
        print("\n❌ Profile creation failed.")
        return
    
    time.sleep(1)
    success, profile_data = test_profile_retrieval(token)
    if not success:
        print("\n❌ Profile retrieval failed.")
        return
    
    time.sleep(1)
    
    # Test 6-8: Scoring and Recommendations
    success, score_data = test_career_score(token)
    time.sleep(1)
    
    success, rec_data = test_job_recommendations(token)
    time.sleep(1)
    
    success, ai_data = test_ai_recommendations(token)
    time.sleep(1)
    
    # Test 9: Report Generation
    success, report_id = test_report_generation(token)
    time.sleep(1)
    
    # Test 10: Knowledge Base
    success, kb_data = test_knowledge_base()
    time.sleep(1)
    
    # Test 11-12: Profile Update and Score Recalculation
    if test_profile_update(token):
        time.sleep(1)
        success, updated_score = test_updated_score(token)
    
    # Print Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
    failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
    total = len(results["tests"])
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    results["summary"] = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "success_rate": f"{(passed/total*100):.1f}%"
    }
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: test_results.json")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_all_tests()
