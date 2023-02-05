from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from stepbot.commands.apply.modal import ApplyModal
from stepbot.commands.sheet import *
import gspread
import os

import discord


class Apply(commands.Cog):
    clan_name = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.clan_names = ["abnormal", "paradox", "anomaly", "paranormal"]
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.ABNORMAL_THREAD_ID = int(os.getenv("ABNORMAL_THREAD_ID"))
        self.PARADOX_THREAD_ID = int(os.getenv("PARADOX_THREAD_ID"))
        self.ANOMALY_THREAD_ID = int(os.getenv("ANOMALY_THREAD_ID"))
        self.PARANORMAL_THREAD_ID = int(os.getenv("PARANORMAL_THREAD_ID"))
        
    @app_commands.command(name="apply")
    async def cmd_apply(self, interaction: discord.Interaction, clan_name: str):
        """
        Apply to one of the Clans.(please check requirements first)
        """
        self.clan_name = clan_name.lower()
        if self.clan_name not in self.clan_names:
            await interaction.response.send_message(content="Invalid clan name", ephemeral=True)
            return

        await interaction.response.send_modal(ApplyModal(clan_name=self.clan_name))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.id == self.bot.user.id:
            return
        if reaction.message.author.id != self.bot.user.id:
            return    
        if reaction.message.channel.id not in [self.ABNORMAL_THREAD_ID, self.PARADOX_THREAD_ID, self.ANOMALY_THREAD_ID, self.PARANORMAL_THREAD_ID]:
            return
        embed = reaction.message.embeds[0]
        date = embed.timestamp.date()
        guild = self.bot.get_guild(self.GUILD_ID)
        channel = reaction.message.channel
        mention_id = reaction.message.guild.get_member_named(
            embed.author.name).mention
        fields_values = {}

        for field in embed.fields:
            fields_values[field.name] = field.value
        fields_values['discord'] = embed.author.name
        fields_values['date'] = date.strftime("%m/%d/%Y")
        name = fields_values["discord"]
        applicant = guild.get_member_named(name)


      
        if "tester" not in [role.name.lower() for role in user.roles]:
            print(f'{name}as reacted to a message he is not authorized to react to')
            await reaction.message.channel.send(
                f"{name} you are not authorized to react to this message")
            await reaction.remove(user)
            return
        
        if reaction.emoji == "✅":
            await applicant.send(f" Accepted you can now apply to {embed.footer.text}. Please apply in game {mention_id}!")
            await channel.send(f"{mention_id} you have been accepted to {embed.footer.text}, please apply in game.")
            print(f'{reaction.users} has accepted {name} to {embed.footer.text} at {date.strftime("%m/%d/%Y")}')

        elif reaction.emoji == "❌":
            await applicant.send(f"Thanks you for considering {embed.footer.text}, but your application as been rejected {mention_id}")
            await channel.send(f"Thanks you for considering {embed.footer.text}, but your application as been rejected {mention_id}")
            print(f'{reaction.users} has rejected {name} from {embed.footer.text} at {date.strftime("%m/%d/%Y")}')

        elif reaction.emoji == "🕐":
            await applicant.send(f'hey {mention_id}, we are full right now in {embed.footer.text} but you have been added to the waiting list and we will get back to you when there is room.')
            await channel.send(f'hey {mention_id}, we are full right now in {embed.footer.text} but you have been added to the waiting list and we will get back to you when there is room.')
            print(f"Inserting data into {embed.footer.text} waiting list")
            insert_to_sheet(fields_values, 'stepbot', embed.footer.text)
