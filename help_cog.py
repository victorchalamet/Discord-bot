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
            if channel.name == 'bot-commands':
                await channel.send(self.help_message)

    def is_channel(ctx):
        return ctx.channel.name == 'bot-commands'
    
    @commands.command(name="help", help="Display all the available commands.")
    @commands.check(is_channel)
    async def help(self, ctx):
        await ctx.send(self.help_message)