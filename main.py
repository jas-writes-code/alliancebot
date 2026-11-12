from discord import *
import wrangler
from game import man
import shlex
#bot and command handling

config = wrangler.load("config")

client = Client(intents=Intents.all())
key = config["key"]

async def newGame(message, args):
    async with message.channel.typing():
        back = await man.newGame(message)
        await message.reply(back)

async def newPlayer(message, gid):
    async with message.channel.typing():
        back = await man.newPlayer(message, gid)
        await message.reply(back)

async def removePlayer(message, gid):
    async with message.channel.typing():
        back = man.removePlayer(message, gid)
        await message.reply(back)

async def listCommands(message, args):
    config = wrangler.load("config")
    prefix = config["prefix"][str(message.guild.id)]
    content = "**Alliance Commands:**\n\n"
    commands = wrangler.load("commands")
    for element in commands:
        item = commands[element]
        content += f"**{prefix}{element}:** {item['info']}\n"
        content += f"Takes arguments: {item['args']}"
        content += "\n\n"

    content = wrangler.newlength(content)
    for element in content:
        await message.reply(element)

@client.event
async def on_message(message):
    if message.guild:
        prefix = config["prefix"][str(message.guild.id)]
    else:
        prefix = "!"
    commands = wrangler.load("commands")
    if not message.author.bot or message.author.system:
        if message.content.startswith(prefix):
            parts = shlex.split(message.content.strip())
            cmd = parts[0].lstrip(prefix)
            args = parts[1:]
            if cmd in commands:
                action_name = commands[cmd]["command"]
                func = globals().get(action_name)
                if callable(func):
                    await func(message, args)
                else:
                    print(f"No function defined for action '{action_name}'")

@client.event
async def on_guild_join(guild):
    prefixes = wrangler.load("config")
    prefixes["prefix"][str(guild.id)] = "!"
    wrangler.save("config", prefixes)

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

client.run(str(key))