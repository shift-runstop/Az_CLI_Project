import requests
import json
import os
import sys

api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL', 'https://api.personal.ai/v1/message')
memory_api_url = os.getenv('MEMORY_API_URL', 'https://api.personal.ai/v1/memory')

def send_ai_message(api_key, message):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = {"Text": message}
    print(payload)
    response = requests.request("POST", base_url, headers=headers, json=payload)
    print("Gimme a 200" ,response)
    if response.status_code == 200:
        ai_response = response.json()
        print("ok you run now", ai_response)
        return ai_response
    else:
        return None

def main():
    message = "Hello"
    ai_response = send_ai_message(api_key, message)

    print("main", ai_response)
    if ai_response is not None:
        print(f"AI Response: {ai_response}")
    else:
        print("Error sending message to AI")

if __name__ == "__main__":
    main()
