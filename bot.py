import discord
import os
import asyncio
from stepbot.commands.apply.command import Apply
from stepbot.commands.ap.command import Ap
from stepbot.commands.admincommands.command import AdminCommands
from stepbot.commands.lft.command import Lft
from stepbot.commands.dm.command import dm
from stepbot.commands.open_report.command import report
from stepbot.commands.close_report.command import close_report
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")


bot = commands.Bot(command_prefix="/",intents =intents)


@bot.event
async def on_ready():

    
    print(f"{bot.user.name} has connect to Discord:\n")

async def setup(bot:commands.bot):
    print("setup ran")
    await bot.add_cog(Apply(bot),guild=discord.Object(id=GUILD_ID))
    await bot.add_cog(AdminCommands(bot),guild=discord.Object(id=GUILD_ID))
    await Ap.setup(bot)
    await Lft.setup(bot)
    await dm.setup(bot)
    await report.setup(bot)
    await close_report.setup(bot)

asyncio.run(setup(bot))
bot.run(TOKEN)