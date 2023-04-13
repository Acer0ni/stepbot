from discord.ext import commands
from discord import app_commands
import discord


class Ap(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="ap")
    async def cmd_ap(self,interaction:discord.Interaction):
        """
        Explains how activity points work for clans.
        """
        embed = discord.Embed()
        embed.set_image(url = "https://i.imgur.com/xWJT204.png")
        await interaction.response.send_message(embed=embed,ephemeral=True)





    async def setup(bot: commands.Bot): 

        await bot.add_cog(Ap(bot),guild=discord.Object(id=1008278641660149860)) 
        print("cog added")

