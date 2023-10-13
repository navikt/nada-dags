import requests
import json
import time

print("hello")

with open("/workspace/notebooks/minfil.json") as f:
    data = f.read()

print("fil:", data)
