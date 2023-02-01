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
        date = embed.timestamp.date()
        fields_values = {}
        if user.id == self.bot.user.id: 
            return
        if reaction.message.author.id != self.bot.user.id:
            return
        if "tester" not in [role.name.lower() for role in user.roles]:
            print("unauthorized")
            reaction.message.channel.send(f"{user.display_name} you are not authorized to react to tgis message")
            return
        if reaction.emoji == "✅":
            await user.send(f" Accepted you can now apply to {self.clan_name}. Please apply in game {embed.author}!")
        elif reaction.emoji == "❌":
            await user.send(f"Thanks you for considering {self.clan_name}, but your application as been rejected {embed.author.name}")
        elif reaction.emoji == "🕐":
            for field in embed.fields:
                fields_values[field.name] = field.value
            fields_values['discord'] = embed.author.name
            fields_values['date'] = date.strftime("%m/%d/%Y")
            print(fields_values)
            name = fields_values["discord"]
            guild = self.bot.get_guild(323528876770852864)
            applicant =guild.get_member_named(name)
            await applicant.send("f'hey {name}, we are full right now in {self.clan_name} but you have been added to the waiting list and we will get back to you when there is room.'")
            insert_to_sheet(fields_values,'stepbot',self.clan_name)
            # print(f'hey {reaction.message.mentions[0].name}, we are full right now in {self.clan_name} but you have been added to the waiting list and we will get back to you when there is room.')

  
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(Apply(bot),guild=discord.Object(id=323528876770852864)) 
        print("cog added")
