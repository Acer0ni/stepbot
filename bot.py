import discord
import os
import asyncio
from stepbot.commands.apply.command import Apply
from stepbot.commands.ap.command import Ap
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="/",intents =intents)

@bot.tree.command(name="test",description="a test command")
async def first_slash_command(interaction: discord.Interaction,clan:str):
    await interaction.response.send_message(f"{clan=}")

@bot.event
async def on_ready():

    await bot.tree.sync(guild=discord.Object(id=323528876770852864))
    print(f"{bot.user.name} has connect to Discord:\n")

async def setup(bot):
    print("setup ran")
    await Apply.setup(bot)
    await Ap.setup(bot)

asyncio.run(setup(bot))
bot.run(TOKEN)