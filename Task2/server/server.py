import json
from typing import List
from fastapi import FastAPI

app = FastAPI()


@app.post('/api/add-numbers') # decorator 

def add_numbers(numbers: List[int], api_key: str):
    if api_key != "CappuccinoAssassino":  # this is NOT how to handle keys, just for fun
        return {
            "result": None,
            "error": True,
            "error_msg": "Access denied"
        }

    acc = 0
    for n in numbers:
        acc += n
    return {
        "result": acc,
        "error": False,
        "error_msg": None
    }

'''
result = add_numbers([1,2,3,4,5,])
r_json = json.dumps(result)
print(r_json)
'''
