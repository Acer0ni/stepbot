import discord
from discord.ext import commands
from discord import app_commands
from stepbot.commands.leadership.modal import LeaderModal
import os

class leadership(commands.Cog):
    clan_name = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.clan_names = ["abnormal", "paradox", "anomaly", "paranormal"]
        self.GUILD_ID = int(os.getenv("GUILD_ID"))

    @app_commands.command(name="leadership")
    async def cmd_apply(self, interaction: discord.Interaction, clan_name: str):
        """
        Apply to one of the Clans.(Please check requirements first)
        """
        self.clan_name = clan_name.lower()
        if self.clan_name not in self.clan_names:
            await interaction.response.send_message(content="Invalid clan name", ephemeral=True)
            return
        await interaction.response.send_modal(LeaderModal(clan_name=self.clan_name))
        

    # async def setup(bot: commands.Bot): 

    #     await bot.add_cog(leadership(bot),guild=discord.Object(id=1008278641660149860)) 
    #     print("cog added1")