import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def debug_scoring():
    # Skip login and use bypass token
    print("Using bypass token...")
    token = "test-token-demo"
    headers = {"Authorization": f"Bearer {token}"}
    print("Token set.")

    try:
        # 2. Create/Update Profile
        print("Updating profile...")
        profile_data = {
            "bio": "I have strong communication and leadership skills. I led a team of 5 in a project.",
            "skills": "Python, React, SQL, Git",
            "experience_years": 1.0,
            "github_url": "https://github.com/test",
            "education_level": "Bachelor"
        }
        
        # Try to get profile first to see if it exists
        get_prof = requests.get(f"{BASE_URL}/student/profile", headers=headers)
        if get_prof.status_code == 200:
            # Update
            resp = requests.put(f"{BASE_URL}/student/profile", json=profile_data, headers=headers)
        else:
            # Create
            resp = requests.post(f"{BASE_URL}/student/profile", json=profile_data, headers=headers)
            
        print(f"Profile update status: {resp.status_code}")
        print(resp.text)

        # 3. Get Score
        print("Fetching score...")
        score_resp = requests.get(f"{BASE_URL}/career/score", headers=headers)
        print(f"Score status: {score_resp.status_code}")
        print(score_resp.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_scoring()
