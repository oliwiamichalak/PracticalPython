import json
from openai import OpenAI
import requests
import time
import sys # for sys.exit() in debug


tools = [{
    "type": "function",
    "name": "gps_to_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City without country, e.g London"
            }
        },
        "required": [
            "location"
        ],
        "additionalProperties": False
    }
}]

USER_AGENT = "ChatSimApp"

api_key = open("demo.key").read().strip()

client = OpenAI(api_key=api_key)

log = []

def city_to_gps(city):
    time.sleep(1) # just bad throttling example
    r = requests.get('https://nominatim.openstreetmap.org/search.php',
                     params = {
                        "city": city,
                        "format": "jsonv2" 
                     },
                     headers= {
                         "User-Agent": USER_AGENT
                     }

                    )
    
    result = r.json()
    if len(result) == 0:
        return None
    
    lat= result[0]['lat']
    lon = result[0]['lon']

    return lat, lon

def gps_to_weather(lat, lon):

    time.sleep(1) # just bad throttling example
    r = requests.get('https://api.open-meteo.com/v1/forecast',
                     params = {
                        "latitude": lat,
                        "longitude": lon,
                        "daily": "temperature_2m_max"
                     },
                     headers= {
                         "User-Agent": USER_AGENT
                     }
                    )
    
    result = r.json()
    return f'{result["daily"]["temperature_2m_max"][0]} C'



print("You can start your chat now")
skip_input = False
while True: 
    try:
        if not skip_input:
            input_text= input("? ")
    except KeyboardInterrupt:
        break

    log.append({
        "role": "user",
        "content": input_text
        })
    response = client.responses.create(
        model="gpt-4.1-nano", #cheapest option
        input=log,
        tools=tools
    )

    # print(response) #all info that is in response, like output, content and type

    for o in response.output:
        if o.type == "message":
            log.append(o)
            print(f"\x1b[1;32m{o.content[0].text}\x1b[m")
            skip_input = False
        elif o.type == "function_call":
            log.append(o)
            args = json.loads(o.arguments)
            if o.name == "gps_to_weather":
                lat, lon = city_to_gps(args['location'])
                result = gps_to_weather(lat, lon)

                log.append({
                    'type': 'function_call_output',
                    'call_id': o.call_id, # to distinguish if calling two func in one time
                    'output': str(result)
                })
                skip_input = True
                continue
     
            raise Exception(f"Unknown function: {o.name}")
    # print(f"\x1b[1;32m{response.output_text}\x1b[m")

print("End.")
