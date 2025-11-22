import requests
import json

BASE = 'http://localhost:8000'

def run():
    try:
        r = requests.get(BASE + '/health', timeout=5)
        print('health', r.status_code, r.text)
    except Exception as e:
        print('health failed', e)
        return

    reg = {'email':'student1@example.com','password':'pass12345','name':'Student One'}
    r = requests.post(BASE + '/api/v1/auth/register', json=reg)
    print('register', r.status_code, r.text)

    login = {'email':reg['email'],'password':reg['password']}
    r = requests.post(BASE + '/api/v1/auth/login', json=login)
    print('login', r.status_code, r.text)
    token = r.json().get('access_token')
    if not token:
        print('no token')
        return

    headers={'Authorization':'Bearer '+token}
    r = requests.get(BASE + '/api/v1/students/me', headers=headers)
    print('get profile', r.status_code, r.text)

    payload={'education_level':'Bachelor','skills':'Python,React','interests':'AI,Data','bio':'Test bio'}
    r = requests.post(BASE + '/api/v1/students/me', json=payload, headers=headers)
    print('create profile', r.status_code, r.text)

    payload={'bio':'Updated bio'}
    r = requests.put(BASE + '/api/v1/students/me', json=payload, headers=headers)
    print('update profile', r.status_code, r.text)

if __name__ == '__main__':
    run()
