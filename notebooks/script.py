import requests
import json
import time

print("hello")

with open("/workspace/notebooks/minfil.json") as f:
    data = f.read()

print("fil:", data)

print(1/0)

res = requests.get("https://google.com")
res.raise_for_status()
print(res.text)

with open('/airflow/xcom/return.json', 'w') as f:
        f.write(json.dumps(data))
