import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.vc = []
        self.is_stop = False
        self.yt_params = {
            "format": "bestaudio/best",
            'noplaylist': True,
            'restrictfilenames': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            }
        self.ffmpeg_options = {
            'options': '-vn'
            }
    
    def search_yt(self, item):
        with YoutubeDL(self.yt_params) as ytdl:
            data = ytdl.extract_info(item, download=True)
        return {'source': data['formats'][0]['url'], 'title': data['title'], 'fileName': ytdl.prepare_filename(data)}
    
    async def play_next(self, ctx):
        if self.queue.qsize() != 0:
            if not self.is_stop:
                fileName = await self.queue.get()
                self.vc[0].play(discord.FFmpegPCMAudio(fileName['fileName'], **self.ffmpeg_options), after=lambda e: asyncio.run(self.play_next()))
        else:
            await ctx.send("There is no music left in the queue.")
    
    async def play_song(self, ctx):
        if self.queue.qsize() != 0:
            if self.vc[0] != None:
                fileName = await self.queue.get()
                self.vc[0].play(discord.FFmpegPCMAudio(fileName['fileName'], **self.ffmpeg_options), after=lambda e: asyncio.run(self.play_next(ctx)))
                await ctx.send(f"Playing: {fileName['title']}")
            else:
                await ctx.send("The bot is not connected to a voice channel.")

    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel !")
        else:
            try:
                self.vc.append(await ctx.author.voice.channel.connect())
            except discord.errors.ClientException:
                pass

    @commands.command(name="play", help="Play the Youtube audio. Connect to the channel if already not.")
    async def play(self, ctx, url):
        self.is_stop = True
        song = self.search_yt(url)
        await self.join(ctx)
        try:
            if self.vc[0] != None:
                await self.queue.put(song)
                len_queue = self.queue.qsize()
                if len_queue == 0:
                    pass
                elif len_queue == 1:
                    await ctx.send("Your song is the next one.")
                elif len_queue == 2:
                    await ctx.send(f"Adding this song to the queue. There is 1 song ahead.")
                else:
                    await ctx.send(f"Adding this song to the queue. There are {len_queue-1} songs ahead.")
                if not self.vc[0].is_playing():
                    await self.play_song(ctx)
        except IndexError:
            pass


    @commands.command(name="pause", help="Pause current the audio")
    async def pause(self, ctx):
        if self.vc[0] != None:
            if not self.vc[0].is_paused():
                self.vc[0].pause()
            else: 
                await ctx.send("The bot is not playing any music right now. Use !play_song to play a music.")
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    
    @commands.command(name="resume", help="Resume the current audio")
    async def resume(self, ctx):
        if self.vc[0] != None:
            if self.vc[0].is_paused():
                self.vc[0].resume()
                self.is_stop = True
            elif self.vc[0].is_playing():
                await ctx.send("A music is already playing. Use !pause to pause it.")
            else:
                await ctx.send("There is no music on pause")
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    
    @commands.command(name="skip", help="Pass the current audio")
    async def next(self, ctx):
        if self.vc[0] != None:
            if self.queue.qsize() == 0:
                await ctx.send("There is no other audio in the queue")
                return
            await self.stop(ctx)
            await self.play_song(ctx)
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    
    @commands.command(name="stop", help="Stop the current audio")
    async def stop(self, ctx):
        if self.vc[0] != None:
            if self.vc[0].is_playing():
                self.vc[0].stop()
                self.is_stop = True
            else:
                await ctx.send("The bot is not playing anything at the moment.")
        else:
            await ctx.send("The bot is not connected to a voice channel.")   

    @commands.command(name="leave", help="Tells the bot to leave the voice channel")
    async def leave(self, ctx):
        if self.vc[0] != None:
            await self.vc[0].disconnect()
            self.vc.pop()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    
    @commands.command(name="clear", help="Clear the queue")
    async def clear(self, ctx):
        if not self.queue.empty():
            len_queue = self.queue.qsize()
            for _ in range(len_queue):
                try:
                    self.queue.get_nowait()
                except:
                    pass
            if len_queue > 1:
                await ctx.send(f"Cleared {len_queue} elements")
            else:
                await ctx.send(f"Cleared {len_queue} element")
        else:
            await ctx.send("The queue is already empty")
    
    @commands.command(name="queue", help="Display the number of element in the queue.")
    async def get_queue(self, ctx):
        len_queue = self.queue.qsize()
        if len_queue > 1:
            await ctx.send(f"There are {len_queue} elements in the queue.")
        else:
            await ctx.send(f"There is {len_queue} element in the queue.")