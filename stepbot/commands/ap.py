from discord.ext import commands
from discord import app_commands
import discord


class Ap(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="ap")
    async def cmd_ap(self,interaction:discord.Interaction):
        embed = discord.Embed()
        embed.set_image(url = "https://discord.com/channels/1008278641660149860/1068022264219574282/1069720758433104023")
        await interaction.response.send_message(embed=embed,ephemeral=False)





    async def setup(bot: commands.Bot): 

        await bot.add_cog(Ap(bot),guild=discord.Object(id=323528876770852864)) 
        print("cog added")

