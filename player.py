import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from ast import alias

ydl_opts = {
    'verbose': True,  # Enable verbose output
    # Add other options as needed
}

class player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.in_play = False
        self.paused = False

        self.m_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'} 
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %item, download=False)['entries'][0]
            except Exception:
                return False
            
            return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.m_queue) > 0:
            self.in_play = True

            mUrl = self.m_queue[0][0]['source'] #get next item in the queue

            self.m_queue.pop(0) #removes the song that is going to be played from the queue

            self.vc.play(discord.FFmpegPCMAudio(mUrl, **self.FFMPEG_OPTIONS), after= lambda e: self.play_next()) # takes the url and info from FFMPEG and unpacks it and then lambda function recursively calls the function
        else:
            self.in_play = False

    async def play_music(self, ctx):
        if len(self.m_queue) > 0:
            self.in_play = True
            mUrl = self.m_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.m_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to VC")
                    return
            else:
                await self.vc.move_to(self.m_queue[0][1])

            self.m_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(mUrl, **self.FFMPEG_OPTIONS), after= lambda e: self.play_next()) # takes the url and info from FFMPEG and unpacks it and then lambda function recursively calls the function
        
        else:
            self.in_play = False

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a song selected from YouTube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel #checks to see what voice channel user is in

        if voice_channel is None:
            #must have a voice channel or else bot will have nowhere to route to
            await ctx.send("Connect to a voice channel")
        elif self.paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Failed")
            else:
                await ctx.send("Song added to queue")
                self.m_queue.append([song, voice_channel])

                if self.in_play == False:
                    await self.play_music(ctx)

    @commands.command(name = "pause", help = "Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.in_play:
            self.in_play = False
            self.paused = True
            self.vc.pause()
        elif self.paused:
            self.in_play = True
            self.paused = False
            self.vc.resume()

    @commands.command(name = "resume", aliases = ["r", "res"], help = "Resumes playing of music")
    async def resume(self, ctx, *args):
        if self.paused == True:
            self.paused = False
            self.in_play = True
            self.vc.resume()

    @commands.command(name = "skip", aliases = ["s"], help = "Skips the current song being played")
    async def skip(self, ctx):
        if self.c != None and self.vc:
            self.vc.stop()

            await self.play_music(ctx)
    
    @commands.command(name="queue", aliases = ["q"], help = "Displays current songs in queue")
    async def queue(self, ctx):
        retVal = ""

        for i in range(0,len(self.m_queue)):
            if (i > 4): break
            retVal += self.m_queue[i][0]['title'] + '\n'

        if retVal != "":
            await ctx.send(retVal)
        else:
            await ctx.send("No music in the queue")

    @commands.command(name = "clear", aliases = ["c", "cl"], help = "Stops music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.in_play:
            self.vc.stop()
        self.m_queue = []
        await ctx.send("Music queue is cleared")
    
    @commands.command(name="leave", aliases = ["dc", "disconnect", "l", "d"], help= "Removes the bot from the VC")
    async def dc(self, ctx):
        self.in_play = False
        self.paused = False
        await self.vc.disconnect()



            


