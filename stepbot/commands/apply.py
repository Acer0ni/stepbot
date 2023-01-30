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
        self.clan_name = None

    @app_commands.command(name="apply")
    async def cmd_apply(self,interaction:discord.Interaction, clan_name: str):
        self.clan_name = clan_name.lower()
        if self.clan_name not in self.clan_names:
            #figure out making this a ephumerical embed later
            await interaction.response.send_message("Invalid clan name")
            return

        await interaction.response.send_modal(ApplyModal(clan_name=self.clan_name))
        
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
            await user.send(f" Accepted you can now apply to {self.clan_name}. Welcome to the clan {user.display_name}!")
            #print(f'{user} as the correct {user.roles}')
        elif reaction.emoji == "❌":
            await user.send(f"get outa here {user.display_name} we dont want you in {self.clan_name}")
        elif reaction.emoji == "🕐":
            for field in embed.fields:
                fields_values[field.name] = field.value
            #insert_to_sheet(fields_values,'stepbot','Sheet1')
            await user.send(f'hey {user.display_name}, we are full right now in {self.clan_name} but you have been added to the waiting list and we will get back to you when there is room.')
  
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(Apply(bot),guild=discord.Object(id=323528876770852864)) 
        print("cog added")
