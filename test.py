#! /usr/bin/env/python3

import requests
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
url = 'https://api.personal.ai/v1/message'

def concat(*args, sep=" "):
    return sep.join(args)

def send_ai_message(api_key, message):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = json.dumps({
        "Text": concat(*message)
    })

    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def main():
    message = sys.argv[1:]
    send_ai_message(api_key, message)

if __name__ == "__main__":
    main()

