import requests
import json
import os
import sys

api_key = os.getenv('API_KEY')
base_url = 'https://api.personal.ai/v1/message'

def send_ai_message():
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = json.dumps({
                "Text": "Hello"
    })

    print(payload)
    response = requests.request("POST", base_url, headers=headers, data=payload)
    print(response.text)

def main():
    message = sys.argv[1:]
    send_ai_message()

if __name__ == "__main__":
    main()
