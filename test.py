import requests
import json
import os

api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL', 'https://api.personal.ai/v1/message')
memory_api_url = os.getenv('MEMORY_API_URL', 'https://api.personal.ai/v1/memory')

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


