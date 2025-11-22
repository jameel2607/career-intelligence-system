import requests
from PIL import Image, ImageDraw
import io

BASE = 'http://localhost:8000'

def make_image():
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 40), 'Hello', fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def run():
    r = requests.post(BASE + '/api/v1/auth/login', json={'email':'student1@example.com','password':'pass12345'})
    token = r.json()['access_token']
    headers={'Authorization':'Bearer '+token}
    img = make_image()
    files={'file': ('hello.png', img, 'image/png')}
    r = requests.post(BASE + '/api/v1/documents/upload', files=files, headers=headers)
    print('upload', r.status_code)
    doc = r.json()
    r = requests.get(BASE + '/api/v1/documents/', headers=headers)
    print('list', r.status_code, len(r.json()))
    r = requests.post(BASE + f"/api/v1/documents/{doc['id']}/ocr", headers=headers)
    print('ocr', r.status_code, bool(r.json().get('ocr_text')), r.json().get('ocr_confidence'))

if __name__ == '__main__':
    run()
