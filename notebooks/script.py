import requests
import json

print("hello")

with open("minfil.txt") as f:
    data = f.read()

print("fil:", data)

res = requests.get("https://google.com")
res.raise_for_status()
print(res.text)

with open('/airflow/xcom/return.json', 'w') as f:
        f.write(json.dumps(data))
