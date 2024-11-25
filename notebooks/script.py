import requests
import json
import time

print("hello")

with open("/airflow/xcom/return.json", "w") as f:
    f.write(json.dumps({"hei": "hei"}))
