# {{{ Imports
import discord, requests, json, time
from discord.ext import commands
from hypixel_bot_tools import *
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
async def hypixel(ctx,player):
    """
    Checks overall stats
    """
    if checkapi(HYPIXEL_API_KEY) is False:
        await ctx.send(_(":warning: Ran out of API queries per minute. Please wait a little while before continuing..."))
        return False
    thing = await ctx.send(_("Fetching player data... If this message doesn't go away, the bot is _definitely_ not broken. :soundsrightbud:"))
    req = requests.get(f"https://api.hypixel.net/player?uuid={getuuid(player)}&key={HYPIXEL_API_KEY}")
    contents = json.loads(req.text)
    if contents['success'] is False:
        await thing.edit(content=_("Invalid player name!"))
    contents = contents['player']
    for i in ("prefix","rank","monthlyPackageRank","newPackageRank"):
        try:
            contents['rank'] = contents[i]
        except KeyError:
            continue
    try:
        contents['rank']
    except KeyError:
        contents['rank'] = None
    print(contents)
    em = discord.Embed(
        title=f"{contents['displayname']}'{_('s Hypixel Stats')}",
        footer=_("Thanks for using Hypibot!"))
    em.add_field(name=_("UUID"),value=getuuid(player),inline=True)
    em.add_field(name="Rank", value=translaterank(contents['rank']),inline=True)
    await thing.edit(embed=em, content="Player data down below.")
# }}}
# {{{ Run bot
bot.run(DISCORD_API_KEY)
# }}}
