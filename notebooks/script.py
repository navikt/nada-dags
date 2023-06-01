import requests

print("hello")

with open("minfil.txt") as f:
    data = f.read()

print("fil:", data)

res = requests.get("https://google.com")
res.raise_for_status()
print(res.text)
