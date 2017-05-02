import requests

kv = {'User-agent':'123'}
r = requests.get('http://python123.io/ws', headers=kv)

print(r.request.headers)