from discord.ext import commands
from discord import app_commands
from stepbot.commands.lft.modal import *
import discord

class Lft(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="lft")
    async def cmd_lft(self, interaction : discord.Interaction):
        """
        Post your information on a lft list for other teams to see.
        """
        await interaction.response.send_modal(LftModall())
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(Lft(bot),guild=discord.Object(id=323528876770852864)) 
        print("cog added")