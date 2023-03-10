import discord
from discord.ext import commands
import asyncio
from music_cog import music_cog
from help_cog import help_cog
import os
from dotenv import load_dotenv #type: ignore

intents = discord.Intents(messages=True, message_content=True, members=True, guilds=True, voice_states=True)
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help") # Remove the original help command because I create one

asyncio.run(bot.add_cog(help_cog(bot)))
asyncio.run(bot.add_cog(music_cog(bot)))

load_dotenv()

bot.run(os.getenv('bot_token'))
client.run(os.getenv('bot_token'))