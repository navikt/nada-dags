import requests
import json
import time
from testmappe.fil import myfunc

myfunc()

print("hello")

with open("/workspace/notebooks/minfil.json") as f:
    data = f.read()

print("fil:", data)
