import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="!",intents =intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connect to Discord:\n")


bot.run(TOKEN)