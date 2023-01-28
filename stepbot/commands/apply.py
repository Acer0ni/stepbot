from discord.ext import commands
from discord import app_commands
import discord
from stepbot.modals.apply import ApplyModal

class Apply(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="apply")
    async def cmd_apply(self,interaction:discord.Interaction, clan_name: str):
        await interaction.response.send_modal(ApplyModal(clan_name=clan_name.lower(),bot=self.bot))
        
    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     if user.bot:
    #         return
    #     if reaction.emoji == "👍":
    #         await user.send("Here is the application form https://docs.google.com/forms/d/e/1FAIpQLSfurAyq_etyKwBl6guqHMCqK_U5CoxZX41mpYAanIXwACbK7g/viewform?usp=sf_link")
    #     elif reaction.emoji == "👎":
    #         await user.send("Thanks for your interest in our clan.")
    
    async def setup(bot: commands.Bot):

        await bot.add_cog(Apply(bot),guild=discord.Object(id=323528876770852864))
        print("cog added")
