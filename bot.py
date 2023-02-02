import discord
import os
import asyncio
from stepbot.commands.apply.command import Apply
from stepbot.commands.ap.command import Ap
from stepbot.commands.lft.command import Lft
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")


bot = commands.Bot(command_prefix="/",intents =intents)

@bot.tree.command(name="test",description="a test command")
async def first_slash_command(interaction: discord.Interaction,clan:str):
    await interaction.response.send_message(f"{clan=}")

@bot.event
async def on_ready():

    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"{bot.user.name} has connect to Discord:\n")

async def setup(bot:commands.bot):
    print("setup ran")
    await bot.add_cog(Apply(bot),guild=discord.Object(id=GUILD_ID))
    await Ap.setup(bot)
    await Lft.setup(bot)

asyncio.run(setup(bot))
bot.run(TOKEN)