# api - a server that allows you to send and receive data using code

import requests
import json

response = requests.get("")

res = json.loads(response.text)

print(response.status_code)
for data in res:
    print(data)

