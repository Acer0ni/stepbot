import discord
import os
import asyncio
from stepbot.commands.apply import Apply
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="/",intents =intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connect to Discord:\n")

# async def setup(bot):
#     await bot.add_cog(MyModal(bot))

# asyncio.run(setup(bot))
bot.run(TOKEN)