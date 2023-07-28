import requests
url = "http://192.168.1.169/greet"
x = requests.post(url, json={"msg":"hi"})
print(x.json())