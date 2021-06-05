# {{{ Imports
import discord, requests, json
from discord.ext import commands
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
# {{{ Commands
def getuuid(username):
    req = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").text
    req = json.loads(req)
    return req['id']
@bot.command(name="uuid")
async def uuid(ctx, username=None): #TODO: instead of doingusername=None, add an error handler if this doesnt get fulfilled
    """
    Gets the UUID of a player. based on their username.
    """
    if username is None:
        await ctx.send(_("Error: you must specify player name"))
        return
    req = getuuid(username)
    await ctx.send(f"Player UUID: {req}")
# }}}
# {{{ Run bot
bot.run(DISCORD_API_KEY)
# }}}
