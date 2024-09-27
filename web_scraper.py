import requests

url = input("Input the URL:\n")
headers = {"Accept": "text/plain"}
r = requests.get(url, headers=headers)
if r:
    print(r.text)
else:
    print("Invalid resource!")