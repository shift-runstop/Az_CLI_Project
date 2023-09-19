
#! /usr/bin/env/python3

#IMPORTS======================================================#

import json
import os
import argparse

import requests #pip install requests

#CONFIG=======================================================#

default_config = {
'api_key' : None,
'UserName': None,
'DomainName_sendMessage':None,
'DomainName_stackMessage':None,
'DomainName_stackResponse':None,
}

def load_config(name="config.json"):
    try:
        f = open(name, "r")
        cfg = json.loads(f.read())
        f.close()
        return cfg
    except:
        f = open(name, "w")
        f.write(json.dumps(default_config, indent=4))
        f.close()
        return default_config

config = load_config()

def save_config():
    f = open("config.json", "w")
    f.write(json.dumps(config, indent=4))
    f.close()    

#ARGUMENTS====================================================#

#define argument parser thing.
parser = argparse.ArgumentParser(
            prog='PAI Command Line Interface',
            description='A tool for interaction with PAI AI from the command line',
            epilog='**Work In Progress**')

#define arguments
parser.add_argument('-s', '-stack', dest='stack', action='store_true', help='stack message and ai response') #optional true or false argument
parser.add_argument('-c', '--config', metavar='CONFIG FILE', help='for loading a config that is not the default. must be .json file.') #value argument
parser.add_argument('-key', dest='api_key', metavar='API KEY') #value argument
parser.add_argument('message', nargs='*', help='type message to AI after arguments') #positional argument : 'message'. nargs='*' ensures we get same usable output as sys.argv[1:]

#set parsed arguments as variable.
args = parser.parse_args()

#handle argument values acordingly

if args.api_key: # -key
    config['api_key'] = args.api_key
    save_config()

if args.config: # -c --config
    config = load_config(args.config)

#=========CONSTANT VARIABLE DEFINITIONS

api_key = config['api_key']
message_url = 'https://api.personal.ai/v1/message'
memory_url = 'https://api.personal.ai/v1/memory'

#MAIN SCRIPT================================================#

#return concatinaton arguments if there is more than 1
def concat(args, sep=" "): 
    if len(args) >= 1: 
        return sep.join(args)

#send message to AI 
def send_message(message): 
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
    }
    payload = json.dumps({ #json.dumps to ensure json format is sent as *requried*
        "Text": message, #message (string data) to send AI.
        'DomainName':config['DomainName_sendMessage'],
        'UserName':config['UserName'],
    })

    #actual sending of payload (message) to AI via API.
    response = requests.request("POST", message_url, headers=headers, data=payload)
    response_data = response.json()

    try:
        return response_data['ai_name'], response_data['ai_message']
    except: 
        "unable to fetch message response"

#save memory to stack. use same domain as sending to unless otherwise defined on function call.
def stack_memory(text, domain=config['DomainName_sendMessage']): #stack memory to AI
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
    }

    payload = json.dumps({ #json.dumps to ensure json format is sent as *requried*
        "Text": text, #text data to stack to AI's memory.
        "SourceName": "CLI", #source name *required* by api.
        "DomainName":domain
    })

    #send memory data to server
    response = requests.request("POST", memory_url, headers=headers, data=payload, timeout=60)


#this is where we will bring it together
def main(): 
    message = concat(args.message) #concatinate list into usable message string

    if message: #if there is a message to send to the ai
        
        #send message to ai. store the response and the name of the ai that responds
        ai_name, response = send_message(message)

        print("\n" + str(ai_name) + " > " + str(response) + "\n")

        #stack message sent to ai and ai response if stack is set to true (see arguments)
        if args.stack:
            #for sending to 2 diffent domains
            if config['DomainName_stackMessage'] != config['DomainName_stackResponse']:
                stack_memory("recieved message: " + str(message), config['DomainName_stackMessage'])
                stack_memory("AI response: " + str(response), config['DomainName_stackResponse'])
                print("stacked message to: " + config['DomainName_stackMessage'] + "\nstacked response to: " + config['DomainName_stackResponse'])
            #for sending to 1 domain
            else:   
                stack_memory(
                    "recieved message: " + str(message) +
                    "\n AI response:" + str(response))                    
                print("stacked.\n")
        else:
            print("[not stacked]\n")

#if there is an api key, run main (script bugs out end errors without it
# due to lack of key in line 36)
if api_key:
    main()
else:
    #if there isnt a key, inform user key is missing.
    print("api key missing") 