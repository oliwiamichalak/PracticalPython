import json
import requests

def add_numbers(numbers):
    data = json.dumps(numbers)
    r = requests.post('http://127.0.0.1:8000/api/add-numbers?api_key=CappuccinoAssassino', data=data)
    res = json.loads(r.text)
    return res["result"]

print(add_numbers([1,2,3,4]))
print(add_numbers([1224,346534553]))

