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
def sqrt(num): return num ** 0.5
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
    em = discord.Embed(
        title=f"{contents['displayname']}'{_('s Hypixel Stats')}",
        footer=_("Thanks for using Hypibot!"))
    em.add_field(name=_("UUID"),value=getuuid(player),inline=True)
    em.add_field(name=_("Rank"), value=contents['rank'],inline=True)
    networkEXP = contents['networkExp']
    em.add_field(name=_("Network Level"),value=f"{(sqrt((2 * networkEXP) + 30625) / 50) - 2.5} ({_('raw')} {contents['networkExp']})",inline=True)
    await thing.edit(embed=em, content="Player data down below.")
# }}}
# {{{ Run bot
bot.run(DISCORD_API_KEY)
# }}}
