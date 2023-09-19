
#! /usr/bin/env/python3

#SETUP======================================================#

import json
import os
import argparse

#pip install requests
import requests 

#load config.json
config = {
'api_key' : '',
}
try:
    f = open("config.json", "r")
    config = json.loads(f.read())
    f.close()
except:
    f = open("config.json", "w")
    f.write(json.dumps(config))
    f.close()

def save_config():
    f = open("config.json", "w")
    f.write(json.dumps(config))
    f.close()    

#setup argpass
parser = argparse.ArgumentParser(
            prog='PAI Command Line Interface',
            description='A tool for interaction with PAI AI from the command line',
            epilog='**Work In Progress**')

#define arguments

parser.add_argument('-s', '-stack', dest='stack', action='store_true', help='stack message and ai response') #optional true or false argument
parser.add_argument('-key', dest='api_key', metavar='API KEY')
parser.add_argument('message', nargs='*', help='type message to AI after arguments') #positional argument : 'message'. nargs='*' ensures we get same usable output as sys.argv[1:]

#set parsed arguments as variable.
args = parser.parse_args()

if args.api_key:
    config['api_key'] = args.api_key
    save_config()

# define constants
api_key = config['api_key']
message_url = 'https://api.personal.ai/v1/message'
memory_url = 'https://api.personal.ai/v1/memory'

#MAIN SCRIPT================================================#
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
        "Text": message, #message (string data) to send AI.
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

        
def main(): #this is where we will bring it together
    message = concat(args.message) #concat into message string or none

    if message: #if there is a message to send to the ai
        
        #send message to ai. store and print response.
        response = str(send_message(message))
        print("\n " + "> " + str(response) + "\n")

        #stack message sent to ai and ai response if stack is set to true (see arguments)
        if args.stack:
            stack_memory(
                "recieved message: " + message +
                "\n AI response:" + response)
            print("stacked.\n")
        else:
            print("not stacked.\n")

#if there is an api key, run main (script bugs out end errors without it
# due to lack of key in line 36)
if api_key:
    main()
else:
    #if there isnt a key, inform user key is missing.
    print("api key missing") 