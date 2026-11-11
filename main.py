from discord import *
import wrangler
import shlex
#bot and command handling

config = wrangler.load("config")

client = Client(intents=Intents.all())
key = config["key"]
prefix = config["prefix"]

async def listCommands(message, args):
    content = "**Alliance Commands:**\n\n"
    commands = wrangler.load("commands")
    for element in commands:
        item = commands[element]
        content += f"**{prefix}{element}:** {item['info']}\n"
        content += f"Takes arguments: {item['args']}"
        content += "\n\n"
    await message.reply(wrangler.newlength(content))

@client.event()
async def on_message(message):
    prefix = config["prefix"][str(message.server.id)]
    if not message.author.bot or message.author.system:
        if message.content.startswith(prefix):
            parts = shlex.split(message.content.strip())
            cmd = parts[0].lstrip(prefix)
            args = parts[1:]
            if cmd in config["commands"]:
                action_name = config["commands"][cmd]["command"]
                func = globals().get(action_name)
                if callable(func):
                    await func(message, args)
                else:
                    print(f"No function defined for action '{action_name}'")

@client.event()
async def on_guild_join(guild):
    prefixes = wrangler.load("config")["prefix"]
    prefixes[str(guild.id)] = "!"

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

client.run(str(key))