import wrangler

def add(user, action, *args):
    queue = wrangler.load("queue")
    if len(queue) == 0:
        queue = {
            "pending": [],
            "locked": []
        }
    queue["pending"].append({
        "user": str(user),
        "action": str(action),
        "args": args
    })
    wrangler.save("queue", queue)

def confirm(user):
    queue = wrangler.load("queue")
    for element in queue["pending"]:
        if str(element["user"]) == str(user):
            queue["locked"].append(element)
            queue["pending"].remove(element)
    wrangler.save("queue", queue)

def check(user, action, *args):
    queue = wrangler.load("queue")
    comp = {
        "user": str(user),
        "action": str(action),
        "args": list(args)
    }
    if len(queue) > 0:
        if comp in queue["pending"]:
            argus = ""
            for element in args:
                argus += f"{element} "
            return f"This action is already in the queue, but it is *not yet locked in*. You can still unqueue it with `!unqueue {comp['action']} {argus}`."
        elif comp in queue["locked"]:
            return "This action is already locked in and can not be cancelled!"
        else:
            return 0
    return 0

'''def removePlayer(message, gid): #TODO: add to queue system, ap distribution on death
    data = wrangler.load("gamedata")
    gid = gid[0]
    if gid in data:
        if str(message.author.id) in data[gid]["players"]:
            del data[gid]["players"][str(message.author.id)]
            wrangler.save("gamedata", data)
            return f"You are no longer participating in {gid}"
        else:
            return "The game exists but you don't seem to be in it."
    else:
        return "Game not found."'''