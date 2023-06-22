import discord
from discord.ext import commands

class helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
        ```
        General commands:
        !help - displays all available commands
        !p <keywords> - finds the song on YouTube and plays it in current channel.
        !q - displays current music queue
        !skip - skips song being played
        !clear - Stops the music and clears the queue
        !leave - Disconnected the bot from the voice channel
        !pause - pauses the current song being played or resumes if already paused
        !resume - resumes current song
        ```
        """ 
        self.text_channel_list = []

        @commands.Cog.listener()
        async def on_ready1(self):
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    self.text_channel_list.append(channel)
            
            await self.send_to_all(self.help_message)

        @commands.command(name="help", aliases = ["h"], help = "Displays all the available commands")
        async def help(self, ctx):
            await ctx.send(self.help_message)

        async def send_to_all(self, msg):
            for text_channel in self.text_channel_list:
                await text_channel.send(msg)    
