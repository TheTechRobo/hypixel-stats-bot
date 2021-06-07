# {{{ Imports
import discord, requests, json, time
from discord.ext import commands
from hypixel_bot_tools import *
import hypixel_bot_tools.errors
# }}}
# {{{ Get token
try:
    from Token import HYPIXEL_API_KEY, DISCORD_API_KEY, PREFIX
except ImportError:
    print("\tFATAL!\tCould not load Token.py file. Please change the Token.example.py to your liking and make sure that it is valid Python syntax")
    raise
# }}} 
# {{{ Setup bot
bot = commands.Bot(command_prefix=PREFIX)
@bot.event
async def on_ready():
    print("Ready for action Rider sir!")
    print("PAW PATROL! PAW PATROL! WE'LL BE THERE ON THE DOUBLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
# }}}
# {{{ pre-gettext wrapper
def _(string):
    return string
# }}}
# {{{ Command
@bot.command(name="uuid")
async def uuid(ctx, username=None): #TODO: instead of doingusername=None, add an error handler if this doesnt get fulfilled
    """
    Gets the UUID of a player. based on their username.
    """
    if checkapi(HYPIXEL_API_KEY) is False:
        await ctx.send(_(":warning: Ran out of API queries per minute. Please wait a little while before continuing..."))
        return False
    status = await ctx.send(_("Loading from API..."))
    if username is None:
        await status.edit(_("Error: you must specify player name"))
        return
    req = getuuid(username)
    await status.edit(content=_("Player UUID: %s") % req)
@bot.command()
async def ping(ctx):
    '''I'm a good person! TOTALLY not stolen from https://www.programcreek.com/python/?code=Der-Eddy%2Fdiscord_bot%2Fdiscord_bot-master%2Fcogs%2Futility.py'''
    ping = ctx.message
    pong = await ctx.send('**:ping_pong:** Pong! (If the bot gets stuck here please contact the developers)')
    delta = pong.created_at - ping.created_at
    delta = int(delta.total_seconds() * 1000)
    hi1 = time.time()
    await pong.edit(content=f':ping_pong: Pong! ({delta} ms)\n*Finding Discord message edit latency...*')
    hi2 = time.time()
    await pong.edit(content=f':ping_pong: Pong! ({delta} ms)\n*Discord message edit latency: {hi2 - hi1}*')
@bot.command(name="hypixel",aliases=("h","stats"))
async def hypixel(ctx,player,ConvertToUUID=True):
    """
    Checks overall stats
    Change ConvertToUUID to False if you want to pass in the UUID, example: `$h <UUID> False` instead of `$h <PlayerName>`.
    """
    if checkapi(HYPIXEL_API_KEY) is False:
        await ctx.send(_(":warning: Ran out of API queries per minute. Please wait a little while before continuing..."))
        return False
    thing = await ctx.send(_("Fetching player data... If this message doesn't go away, the bot is _definitely_ not broken. :soundsrightbud:"))
    try:
        contents = overall(HYPIXEL_API_KEY,player,ConvertToUUID)
    except hypixel_bot_tools.errors.InvalidPlayer:
        await thing.edit(content=_(":warning: Invalid player!"));raise
    print(contents)
    lenfriends = countfriends(friends(HYPIXEL_API_KEY,player,ConvertToUUID))
    try:
        statusAPI = contents['settings']['apiSession']
    except KeyError:
        statusAPI = True
    if not statusAPI:
        statusAPI_Message = _("API access disabled")
        currentStatus_Message = _("Unavailable - API access disabled")
    else:
        item = status(HYPIXEL_API_KEY,player,ConvertToUUID)['session']
        statusAPI_Message = item['online']
        try:
            currentStatus_Message = f"{item['gameType']} ({_('mode')} {item['mode']}); {_('on map')} {item['map']}"
        except KeyError:
            currentStatus_Message = _("Offline")
    for i in ("karma",): #these are fields that might not exist
        try:
            contents[i]
        except KeyError:
            contents[i] = 0
            continue
    em = discord.Embed(
        title=f"{contents['displayname']}'{_('s Hypixel Stats')}",
        footer=_("Thanks for using Hypibot!"))
    em.add_field(name=_("UUID"),value=getuuid(player),inline=True)
    em.add_field(name=_("Rank"), value=contents['rank'],inline=True)
    em.add_field(name=_("Network Level"),value=f"{round(RawXPToLevel(contents['networkExp']),2)} ({_('raw')} {contents['networkExp']})",inline=True)
    em.add_field(name=_("Karma"),value=contents['karma'],inline=True)
    em.add_field(name=_("Friends"),value=lenfriends,inline=True)
    em.add_field(name="\u200b",value="\u200b",inline=False)#newline; \u200b is a zero width space that is allowed by dcord
    em.add_field(name=_("Online?"),value=statusAPI_Message,inline=True)
    em.add_field(name=_("Current Game"),value=currentStatus_Message,inline=True)
    await thing.edit(embed=em, content="Player data down below.")
# }}}
# {{{ Run bot
if __name__ == "__main__":
    bot.run(DISCORD_API_KEY)
# }}}
