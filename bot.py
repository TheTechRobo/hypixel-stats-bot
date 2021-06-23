# {{{ Imports
import discord, requests, json, time
from discord.ext import commands
from hypixel_bot_tools import *
import hypixel_bot_tools.errors
hypierror = hypixel_bot_tools.errors
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
async def uuid(ctx, username):
    """
    Gets the UUID of a player. based on their username.
    """
    status = await ctx.send(_("Loading from API..."))
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
    except hypierror.InvalidPlayer:
        await thing.edit(content=_(":warning: Invalid player!"));raise
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
            for i in ("gameType","mode","map"):
                try:item[i]
                except KeyError:
                    if i == "gameType":
                        raise
                    item[i] = "N/A"
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
    em.add_field(name="\u200b",value="\u200b",inline=True)#newline; \u200b is a zero width space that is allowed by dcord
    em.add_field(name=_("Online?"),value=statusAPI_Message,inline=True)
    em.add_field(name=_("Current Game"),value=currentStatus_Message,inline=True)
    await thing.edit(embed=em, content="Player data down below.")
@bot.command()
async def bedwars(ctx, player, ConvertToUUID=True):
    if checkapi(HYPIXEL_API_KEY) is False: #todo; use exceptions instead
        await ctx.send(_(":warning: Ran out of API queries per minute. Please wait a little while before continuing..."))
        return False
    try: contents = overall(HYPIXEL_API_KEY, player, ConvertToUUID=ConvertToUUID)
    except KeyError: raise InvalidPlayer
    data = contents['stats']['Bedwars']
    em = discord.Embed(
        title=_("%s's Bedwars Stats" % contents['displayname']),
        footer=_("Thanks for using Hypibot!")
    )
    em.add_field(name=_("Experience"), value=data['Experience'],inline=True)
    em.add_field(name=_("Coins"),value=data['coins'],inline=True)
    await ctx.send(embed=em)
    for i in ("eight_one","eight_two","three_three","two_four","four_four"):
        await ctx.send(bedwarsToHuman(i))
# }}}
# Error handling {{{
@bot.event
async def on_command_error(ctx, error):
    """
    Does some stuff in case of cooldown error.
    Stolen from brewbot.
    """
    if hasattr(ctx.command, 'on_error'): #https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
        return
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandOnCooldown):
        potentialMessages = [f'This command is on cooldown, please wait {int(error.retry_after)}s.']
        message = (random.choice(potentialMessages))
        print('\nSomeone tried to do a command that was on cooldown')
    elif isinstance(error, commands.MissingRequiredArgument):
        strerror = str(error).split(' ')[0]
        message = _("You seem to be missing a required argument \"{strerror}\". Run `{PREFIX}help [command]` for more information.").format(PREFIX=PREFIX, strerror=strerror)
    elif isinstance(error, hypierror.HypixelApiDown):
        message = _("We couldn't contact the hypixel API. Is the service down?")
    elif isinstance(error, hypierror.InvalidPlayer):
        message = _("This seems to be an invalid player - it doesn't have an entry on Mojang's API.\nTry running {PREFIX}bedwars {uuid} False to search by UUID instead. Run {PREFIX}help bedwars for more info.").format(PREFIX=PREFIX, uuid=error)
    else:
        message = "Unknown error !"
    em = discord.Embed(title=_("⚠️ Oops! ⚠️"), description=message)
    em.set_footer(text=error)
    await ctx.send(embed=em)
    raise(error)
# }}}
# {{{ Run bot
if __name__ == "__main__":
    bot.run(DISCORD_API_KEY)
# }}}
