import requests
import json
import os
from datetime import datetime
import pytz

api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL', 'https://api.personal.ai/v1/message')
memory_api_url = os.getenv('MEMORY_API_URL', 'https://api.personal.ai/v1/memory')

def get_local_time():
    user_tz = datetime.now(pytz.utc).astimezone().tzinfo
    local_time = datetime.now(user_tz).strftime('%a, %d %b %Y %H:%M:%S %Z')
    return local_time

def send_ai_message(api_key, message):
    base_url = 'https://api.personal.ai/v1/message'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    payload = {"Text": message}

    response = requests.post(base_url, headers=headers, json=payload)

    if response.status_code == 200:
        ai_response = response.json()['ai_message']
        return ai_response
    else:
        return None

def main():
    api_key =  '{{user-api-key}}'
    local_time = get_local_time()
    message = f"Hi, I'm sending a test message please respond with a ""Testing 321 Done"" Sent at {local_time}"

    ai_response = send_ai_message(api_key, message)

    if ai_response is not None:
        print(f"AI Response: {ai_response}")
    else:
        print("Error sending message to AI")

if __name__ == "__main__":
    main()
