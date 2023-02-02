from discord.ext import commands
from discord import app_commands
import discord

class lft(commands.bot):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="lft")
    async def cmd_lft(self,interaction:discord.Interaction):
        """
        Post your information on a lft list for other teams to see.
        """
    