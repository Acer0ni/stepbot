from discord.ext import commands
from discord import app_commands
from stepbot.modals.apply import ApplyModal
from stepbot.commands.sheet import *
import gspread
import discord

class Apply(commands.Cog):
   

    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.clan_names =  ["abnormal","paradox","anomaly","paranormal"]

    @app_commands.command(name="apply")
    async def cmd_apply(self,interaction:discord.Interaction, clan_name: str):
        if clan_name.lower() not in self.clan_names:
            #figure out making this a ephumerical embed later
            await interaction.response.send_message("Invalid clan name")
            return

        await interaction.response.send_modal(ApplyModal(clan_name=clan_name.lower()))
        
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction : discord.Reaction, user : discord.User):
        embed = reaction.message.embeds[0]
        fields_values = {}
        if user.id == self.bot.user.id: 
            return
        if reaction.message.author.id != self.bot.user.id:
            return
        if "tester" not in [role.name.lower() for role in user.roles]:
            print("unauthorized")
            return
        if reaction.emoji == "✅":
            await reaction.message.channel.send(f"{user.mention} accepted")
            #print(f'{user} as the correct {user.roles}')
        elif reaction.emoji == "❌":
            await reaction.message.channel.send(f"{user.mention} rejected")
        elif reaction.emoji == "🕐":
            for field in embed.fields:
                fields_values[field.name] = field.value
            #insert_to_sheet(fields_values,'stepbot','Sheet1')
            await reaction.message.channel.send(f'{user.mention} added to waiting list')
  
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(Apply(bot),guild=discord.Object(id=323528876770852864)) 
        print("cog added")
