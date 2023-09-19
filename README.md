---
id: "904dfba4-d813-4134-9102-57d48af9c009"
title: "README"
source: ""
aliases: ["README"]
---
Python branch of the Az CLI Project: https://github.com/shift-runstop/Az_CLI_Project

This is a python script to allow you to communicate with your [Personal AI](https://personal.ai) via CLI.

# Installation
* Clone the repository
```
git clone https://github.com/sRuxen/Az_CLI_Project-Python/pai.py
```
* add API key to config.json or use the following
```
python3 pai.py -key [YOUR API KEY HERE]
```

# Usage
send message to AI

``
python3 pai.py [Your Message Here.]
``

* Note, you need to use the -s argument to stack messages, they do not stack by default.

get help (list arguments)

``
python3 pai.py -h
``

# Configuration
The script saves its configuration to config.json by default.
Here you can define domain names for usage of sub profiles, the api key, and a local username so the AI knows who sent it a message


