# import discord
# from discord.ext import commands
# import os
# from youtube_dl import YoutubeDL
# from ast import alias
# from player import player
# from helper import helper

# intents= discord.Intents.default()
# intents.message_content = True

# bot = commands.Bot(command_prefix="!", intents=intents) #Any command with the prefix of ! will be recognized by the bot

# bot.remove_command('help')


# bot.add_cog(player(bot))
# bot.add_cog(helper(bot))

# bot.run(os.getenv("TOKEN"))

import discord
from discord.ext import commands
import os

#import all of the cogs
from helper import helper
from player import player



intents= discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#remove the default help command so that we can write out own
bot.remove_command('help')

#register the class with the bot
# bot.add_cog(helper(bot))
# bot.add_cog(player(bot))

#start the bot with our token
# bot.run(os.getenv("TOKEN"))

@bot.event
async def on_ready():
    await bot.add_cog(player(bot))
    await bot.add_cog(helper(bot))

bot.run(os.getenv("TOKEN"))

