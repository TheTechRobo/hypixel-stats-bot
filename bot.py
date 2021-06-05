import discord
try:
    from Token import HYPIXEL_API_KEY, DISCORD_API_KEY
except ImportError:
    print("\tFATAL!\tCould not load Token.py file. Please change the Token.example.py to your liking and make sure that it is valid Python syntax")
    raise
