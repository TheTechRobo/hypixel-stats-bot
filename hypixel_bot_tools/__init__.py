import requests, json
from .errors import *
def getuuid(username):
    """
    Gets the UUID of a player from their username, using the Mojang API
    """
    req = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if req.status_code == 204:
        raise InvalidPlayer(username)
    return json.loads(req.text)['id']
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

def overall(HYPIXEL_API_KEY,player,TranslateRank=True,ConvertToUUID=True):
    """
    Downloads main player stats, gets the correct rank.
    If you don't want it to translate it (from e.g. SUPERSTAR to [MVP++], VIP_PLUS to [VIP+], etc), set TranslateRank to False. (It will still add the correct rank to the dictionary.)
    If you'd like to get the UUID yourself, instead of setting "player" variable to the username, set ConvertToUUID to False. That will skip changing the player variable into a UUID.
    It is not async since it is meant to be used in any module, not just discord.py.
    """
    if ConvertToUUID:
        player = getuuid(player)
    req = requests.get(f"https://api.hypixel.net/player?uuid={player}&key={HYPIXEL_API_KEY}")
    contents = json.loads(req.text)
    if contents['success'] is False:
        raise UnknownError(contents)
    contents = contents['player']
    for i in ("prefix","rank","monthlyPackageRank","newPackageRank"):
        try:
            print(f"{i}: {contents[i]}")
            sgfdf = contents[i]
            if sgfdf == "NONE":
                continue
            contents['rank'] = sgfdf
            break
        except KeyError:
            continue
    try:
        contents['rank']
    except KeyError:
        contents['rank'] = None
    if TranslateRank: contents['rank'] = translaterank(contents['rank'])
    return contents
def friends(HYPIXEL_API_KEY,player,ConvertToUUID=True):
    """If you'd like to get the UUID yourself, instead of setting "player" variable to the username, set ConvertToUUID to False. That will skip changing the username into a UUID.
    Additionally, it doesn't get any other player data, such as the rank, or any information about the friends (including their names - all it gives is the UUIDs of the sender and the receiver!). For those, you may want to use the overall() function."""
    if ConvertToUUID: player = getuuid(player)
    req = json.loads(requests.get(f"https://api.hypixel.net/friends?key={HYPIXEL_API_KEY}&uuid={player}").text)
    if req['success'] is False:
        raise UnknownError(req)
    return req
def countfriends(data):
    """
    Pass in the output of friends() (or compatible) as data.
    """
    return len(data['records'])
def recentgames(HYPIXEL_API_KEY,player,ConvertToUUID=True):
    """If you'd like to provide the UUID yourself, set ConvertToUUID to False. That'll skip the conversion of username provided to UUID."""
    if ConvertToUUID: player = getuuid(player)
    req = json.loads(requests.get(f"https://api.hypixel.net/recentgames?key={HYPIXEL_API_KEY}&uuid={player}").text)
    if req['success'] is False:
        raise UnknownError(req)
    return req
def status(HYPIXEL_API_KEY,player,ConvertToUUID=True):
    """If you'd like to provide the UUID yourself, set ConvertToUUID to False. That'll skip the conversion of username provided to UUID.
    WARNING: Hypixel allows players to disable this api access, in which case it'll look like they're offline. For more info, see https://github.com/HypixelDev/PublicAPI/wiki/Common-Questions."""
    if ConvertToUUID: player = getuuid(player)
    req = json.loads(requests.get(f"https://api.hypixel.net/status?key={HYPIXEL_API_KEY}&uuid={player}").text)
    if req['success'] is False:
        raise UnknownError(req)
    return req
def guild(HYPIXEL_API_KEY,data,TYPE):
    """
    This one's a bit complicated.
    Set TYPE to "id" to retrieve the guild data by its ID.
    Set TYPE to "player" to retrieve the guild data by a member's UUID. (This function does NOT change a username to a UUID; you can do that yourself with the getuuid function included in this module.
    Set TYPE to "name" to retrieve the guild data by its name.
    DATA should be set to the guild ID, player UUID, or guild name, depending on the TYPE you chose.
    URL used: f"https://api.hypixel.net/guild?key={HYPIXEL_API_KEY}&{TYPE}={data}
    """
    req = json.loads(requests.get(f"https://api.hypixel.net/guild?key={HYPIXEL_API_KEY}&{TYPE}={data}").text)
    if req['success'] is False: raise UnknownError(req)
    return req
def _sqrt(num): return num ** 0.5
def RawXPToLevel(xp):
    """
    Accepts the number of Xp (API: player.networkExp), and returns the level.
    Quite a long number, you may want to round it.
    Kudos to https://hypixel.net/threads/convert-network-exp-to-network-level.1912930 for the formula :D
    """
    return (_sqrt((2 * xp) + 30625) / 50) - 2.5
def RestOfTheFunctions():
    """
    The rest of the functions are still a work in progress.
    """
    raise BaseException
