
#! /usr/bin/env/python3

#SETUP======================================================#

import json
import os
import sys

#pip install requests
import requests 

#pip install python-dotenv
from dotenv import load_dotenv 


#MAIN SCRIPT================================================#

#get api key from .env
load_dotenv()
api_key = os.getenv('API_KEY') 

# define urls for message and memory
message_url = 'https://api.personal.ai/v1/message'
memory_url = 'https://api.personal.ai/v1/memory'

def concat(args, sep=" "): 
    #return concatinaton of arguments if there is 1 or more (error prevention)
    if len(args) >= 1: 
        return sep.join(args)
    
def send_message(message):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    payload = json.dumps({ #json.dumps to ensure json format is sent as *requried*
        "Text": message #message (string data) to send AI.
    })

    #send message to AI.
    response = requests.request("POST", message_url, headers=headers, data=payload)
    response_data = response.json()

    try:
        return response_data['ai_message']
    except: 
        "unable to fetch message response"

def stack_memory(text):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = json.dumps({ #json.dumps to ensure json format is sent as *requried*
        "Text": text, #text data to stack to AI's memory.
        "SourceName": "CLI", #source name *required* by api.
    })

    #send memory data to server
    response = requests.request("POST", memory_url, headers=headers, data=payload, timeout=60)
    
    #print response (debug purpouses)
    print(response)
    

        
def main(): #this is where we will bring it together

    cli_input = sys.argv[1:] #get arguments for message
    message = concat(cli_input) #concat into message string or none

    if message: #if there is a message to send to the ai
        
        #send message to ai. store and print response.
        response = str(send_message(message))
        print("\n " + str(response))

        #stack message sent to ai and ai response.
        stack_memory(
            "recieved message: " + message +
            "\n AI response:" + response)
            #!!!!currently returns error 500, internal server error.!!!!

#if there is an api key, run main (script bugs out end errors without it
# due to lack of key in line 36)
if len(api_key) > 0:
    main()
else:
    #if there isnt a key, inform user key is missing.
    print("api key missing") 
    #-- refine later to inform of .env file
    #-- possibly auto create .env file ?