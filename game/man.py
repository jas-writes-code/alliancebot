import wrangler, tickqueue
from human_id import generate_id as newid
import time, random

def newGame(message):
    if message.guild:
        data = wrangler.load("gamedata")
        gid = newid(word_count=3)
        start = int(time.time())

        data[gid] = {
            "game": {
                "guild": message.guild.id,
                "admin": message.author.id,
                "cycle": 24,
                "start": start,
                "nextTick": 3600*24 + start
            },
            "players": {}
        }

        content = f"**New Game created!**\n"
        content += f"Join the game with `!join {gid}`!\n"
        content += f"This game is joinable until <t:{data[gid]['game']['nextTick']}:F>."

        wrangler.save("gamedata", data)

        return content
    else:
        return "This command must be executed in a server!"

def placePlayer(gid):
    data = wrangler.load("gamedata")
    posx = random.randint(1, 15)
    posy = random.randint(1, 15)
    if len(data[gid]["players"]) > 0:
        for player in data[gid]["players"]:
            if data[gid]["players"][player]["pos"][0] == posx and data[gid]["players"][player]["pos"][1] == posy:
                placePlayer(gid)
            else:
                pos = [posx, posy]
                return pos
    else:
        pos = [posx, posy]
        return pos

def newPlayer(message, gid):
    data = wrangler.load("gamedata")
    gid = gid[0]
    if gid in data:
        for game in data:
            for element in data[game]["players"]:
                if str(element) == str(message.author.id):
                    return "You cannot join more than one game! Leave a game using `!leave <Game ID>`"

        data[gid]["players"][str(message.author.id)] = {
            "pos": placePlayer(gid),
            "reach": 3.5,
            "ap": 0,
            "hp": 3
        }

        wrangler.save("gamedata", data)

        content = f"**You have joined `{gid}`!**\n"
        content += f"You have been placed on {data[gid]['players'][str(message.author.id)]['pos']}.\n"
        content += f"{data[gid]['players'][str(message.author.id)]['hp']} HP | {data[gid]['players'][str(message.author.id)]['ap']} AP |  {data[gid]['players'][str(message.author.id)]['reach']} Reach"
        return content
    else:
        return "Game not found. Did you enter the right ID"

def removePlayer(message, gid): #TODO: ap distribution on death
    data = wrangler.load("gamedata")
    gid = gid[0]
    check = tickqueue.check(message.author.id, "removePlayer", gid)
    if check == 0:
        if gid in data:
            if str(message.author.id) in data[gid]["players"]:
                tickqueue.add(message.author.id, "removePlayer", gid)
                return f"You are queued to be removed from {gid} at the next **Tick**. This will take place <t:{data[gid]['game']['nextTick']}:R>\n-# This action is not yet confirmed. Use `!confirm` to lock in all your queued actions."
            else:
                return "The game exists but you don't seem to be in it."
        else:
            return "Game not found."
    else:
        return check