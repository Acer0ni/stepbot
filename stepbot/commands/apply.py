from discord.ext import commands
from discord import app_commands
import discord
from stepbot.modals.apply import ApplyModal

class Apply(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="apply")
    async def cmd_apply(self,interaction:discord.Interaction, clan_name: str):
        await interaction.response.send_modal(ApplyModal(clan_name=clan_name.lower()))
        
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction : discord.Reaction, user : discord.User):
       
        if user.id == self.bot.user.id: 
            return
        if reaction.message.author.id != self.bot.user.id:
            return
        if "tester" not in [role.name.lower() for role in user.roles]:
            return
        if reaction.emoji == "✅":
            await reaction.message.channel.send("accepted")
            #print(f'{user} as the correct {user.roles}')
        elif reaction.emoji == "❌":
            await reaction.message.channel.send("rejected")
  
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(Apply(bot),guild=discord.Object(id=323528876770852864)) 
        print("cog added")
