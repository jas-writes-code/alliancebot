from discord import *
import wrangler
import shlex

config, commands, data, queue = wrangler.loaddata()

client = Client(intents=Intents.all())
key = config["key"]

@client.event()
async def on_message(message):
    if not message.author.bot or message.author.system:
        if message.content.startswith("!"):
            parts = shlex.split(message.content.strip())
            cmd = parts[0].lstrip("!")
            args = parts[1:]
            if cmd in config["commands"]:
                action_name = config["commands"][cmd]["command"]
                func = globals().get(action_name)
                if callable(func):
                    await func(message, args)
                else:
                    print(f"No function defined for action '{action_name}'")

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

client.run(str(key))