import urllib.request
import json

test_users = [
    ('admin', 'admin123'),
    ('warden_boys', 'warden123'),
    ('accountant', 'acct123'),
    ('sahaana', 'sahaana123')
]

for u, p in test_users:
    data = json.dumps({'username': u, 'password': p}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(f"SUCCESS: {u} -> Role: {res.get('role')}")
    except Exception as e:
        print(f"FAILED: {u} -> {e}")
