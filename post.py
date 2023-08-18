import requests
import json

url = 'http://127.0.0.1:8000/get_json_txt'
headers = {'Content-Type': 'application/json'}
data = {'key': 'value'}  # 你要发送的JSON数据

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
# print(response.json())