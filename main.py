import discord
from discord.ext import commands
import asyncio
from music_cog import music_cog
from help_cog import help_cog

intents = discord.Intents(messages=True, message_content=True, members=True, guilds=True, voice_states=True)
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help")

asyncio.run(bot.add_cog(help_cog(bot)))
asyncio.run(bot.add_cog(music_cog(bot)))


bot.run("MTA3ODA3MTYxOTg4NjUxODM3Mg.G43Eev.L5U5QD7lZ0ZD_MX4T411zw-iX6zNd9U53K2fj0")
client.run("MTA3ODA3MTYxOTg4NjUxODM3Mg.G43Eev.L5U5QD7lZ0ZD_MX4T411zw-iX6zNd9U53K2fj0")