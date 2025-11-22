import requests

BASE_URL = "http://127.0.0.1:8001/api/v1"
TOKEN = "test-token-demo"

def main():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        resp = requests.get(f"{BASE_URL}/career/score", headers=headers)
        print("Status code:", resp.status_code)
        print("Response JSON:")
        print(resp.json())
    except Exception as e:
        print("Error during request:", e)

if __name__ == "__main__":
    main()
