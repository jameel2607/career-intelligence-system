import requests

BASE='http://localhost:8000'

def run():
    login={'email':'student1@example.com','password':'pass12345'}
    r = requests.post(BASE+'/api/v1/auth/login', json=login)
    print('login', r.status_code)
    token = r.json().get('access_token')
    headers={'Authorization':'Bearer '+token}
    r = requests.post(BASE+'/api/v1/reports/generate', headers=headers)
    print('generate', r.status_code)
    r = requests.get(BASE+'/api/v1/reports/', headers=headers)
    print('list', r.status_code, len(r.json()))
    first = r.json()[0]
    r = requests.get(BASE+f"/api/v1/reports/{first['id']}/download", headers=headers)
    print('download', r.status_code, r.headers.get('content-type'))

if __name__ == '__main__':
    run()
