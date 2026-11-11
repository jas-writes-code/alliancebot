import json

#text and data wrangling that i'll probably need fairly often

def loaddata():
    with open('config.json', 'r') as f:
        config = json.load(f)
    with open('commands.json', 'r') as f:
        commands = json.load(f)
    with open('data.json', 'r') as f:
        data = json.load(f)
    with open('queue.json', 'r') as f:
        queue = json.load(f)
    return config, commands, data, queue