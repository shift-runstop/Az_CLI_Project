import requests
import json
import os
import sys

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
    print("HElloooooo" ,response)
    if response.status_code == 200:
        ai_response = response.json()
        print("testing, why do you not run", ai_response)
        return ai_response
    else:
        return None

def main():
    api_key =  '{{user-api-key}}'
    message = sys.argv
    ai_response = send_ai_message(api_key, message)

    print("main", ai_response)
    if ai_response is not None:
        print(f"AI Response: {ai_response}")
    else:
        print("Error sending message to AI")

if __name__ == "__main__":
    main()
