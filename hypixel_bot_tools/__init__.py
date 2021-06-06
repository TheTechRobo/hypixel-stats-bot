def getuuid(username):
    """
    Gets the UUID of a player from their username, using the Mojang API
    """
    req = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").text
    req = json.loads(req)
    return req['id']
def translaterank(rank):
    """
    Takes the rank. You need to find the rank on your own.
    Returns the rank, all formatted with things like [MVP++] instead of MVP_PLUS_PLUS, and removes special formatting characters from prefixes.
    """
    # originally i had implemented this with if statements but then i thought of this (i had got up to vip+ with the if statements)
    #the following if statements are exceptions
    if rank == "SUPERSTAR": rank = "MVP_PLUS_PLUS"
    if rank == "YOUTUBER": rank = "YOUTUBE"
    if rank is None: return "Regular"
    rank = rank.replace("_","").replace("PLUS","+")
    for letter in "abcdefghijklmnopqrstuvwxyz0123456789_[]§": #safe since there aren't lowercases in ranks and ive never seen numbers in ranks before
        rank = rank.replace(letter,"")
    return f"[{rank}]"
def checkapi(key):
    """
    Checks if the API key is exhausted from requests; if so, returns False. If not, returns None.
    """
    req = requests.get(f"https://api.hypixel.net/key?key={key}").text
    req = json.loads(req)
    if req['record']['queriesInPastMin'] >= 120:
        return False
