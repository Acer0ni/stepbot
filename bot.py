import discord
import os
import asyncio
from stepbot.commands.apply.command import Apply
from stepbot.commands.ap.command import Ap
from stepbot.commands.admincommands.command import AdminCommands
from stepbot.commands.lft.command import Lft,LftView
from stepbot.commands.dm.command import dm
from stepbot.commands.open_report.command import report
from stepbot.commands.close_report.command import close_channel
from stepbot.commands.leadership.command import leadership
from stepbot.commands.group.command import group
from stepbot.commands.apply2.view import ClanView, ApplyView
from stepbot.commands.apply2.apply_resp_view import ApplicationResponseView
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")


bot = commands.Bot(command_prefix="/",intents =intents)

@bot.event
async def on_ready():
    print(f"[+] {bot.user.name} is now connected to Discord:\n")

@bot.event
async def on_disconnect():
    print(f'[-] {bot.user.name} has disconnected from Discord:\n')

@bot.event
async def on_resumed():
    print(f'[+] {bot.user.name} has resumed connection to Discord:\n')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        return
    print(f'[-] An error has occured when running {ctx.command.name}:\n[-] Error: {error}')   



async def setup(bot:commands.bot):
    await bot.add_cog(Apply(bot),guild=discord.Object(id=GUILD_ID))
    await bot.add_cog(AdminCommands(bot),guild=discord.Object(id=GUILD_ID))
    await Ap.setup(bot)
    await bot.add_cog(ClanView(bot),guild=discord.Object(id=GUILD_ID))
    await bot.add_cog(Lft(bot),guild=discord.Object(id=GUILD_ID))
    await dm.setup(bot)
    await report.setup(bot)
    await close_channel.setup(bot)
    await bot.add_cog(leadership(bot),guild=discord.Object(id=GUILD_ID))
    await bot.add_cog(group(bot),guild=discord.Object(id=GUILD_ID))
    print("[+] All cogs have been loaded successfully")
    bot.add_view(ApplicationResponseView())
    bot.add_view(ApplyView())
    #bot.add_view(LftView())
    print("[+] All views have been loaded successfully")

asyncio.run(setup(bot))
bot.run(TOKEN)