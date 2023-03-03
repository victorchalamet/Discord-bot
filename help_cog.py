import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
!help - Display all the available commands.
!play <url> - Play the Youtube audio. Connect to the voice channel if already not.
!pause - Pause the current audio.
!resume - Resume the current audio.
!skip - Skip the current audio.
!stop - Stop the current audio.
!leave - Leave the voice channel.
!queue - Display the number of elements in the queue.
```
"""

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        for channel in guild.text_channels:
            if channel.id == 1078432477414170675:
                await channel.send(self.help_message)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.find("!", 0,1) != -1 and message.channel.name != "bot-commands" and not message.author.bot:
            await message.channel.send("You are not in the right channel to enter commands. Go to the bot-commands channel.")
    
    @commands.command(name="help", help="Display all the available commands.")
    async def help(self, ctx):
        await ctx.send(self.help_message)