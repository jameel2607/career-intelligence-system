import requests

BASE='http://localhost:8000'

def run():
    login={'email':'student1@example.com','password':'pass12345'}
    r = requests.post(BASE+'/api/v1/auth/login', json=login)
    print('login', r.status_code)
    token = r.json().get('access_token')
    headers={'Authorization':'Bearer '+token}
    r = requests.get(BASE+'/api/v1/career/score', headers=headers)
    print('score', r.status_code, r.text)
    r = requests.get(BASE+'/api/v1/career/recommendations', headers=headers)
    print('recs', r.status_code, r.text)

if __name__ == '__main__':
    run()
