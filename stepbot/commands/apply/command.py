from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from stepbot.commands.apply.modal import ApplyModal
from stepbot.commands.apply.refused import RefusedModal
#from stepbot.commands.sheet import *
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
        self.LEADER_ROLE = os.getenv("LEADER_ROLE")
        
    @app_commands.command(name="apply")
    async def cmd_apply(self, interaction: discord.Interaction, clan_name: str):
        """
        Apply to one of the Clans.(Please check requirements first)
        """
        self.clan_name = clan_name.lower()
        if self.clan_name not in self.clan_names:
            await interaction.response.send_message(content="Invalid clan name", ephemeral=True)
            return

        await interaction.response.send_modal(ApplyModal(clan_name=self.clan_name))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        user = self.bot.get_user(payload.user_id)
        if payload.user_id == self.bot.user.id:
            return
        if message.author.id != self.bot.user.id:
            return
        if message.channel.id not in [self.ABNORMAL_THREAD_ID, self.PARADOX_THREAD_ID, self.ANOMALY_THREAD_ID, self.PARANORMAL_THREAD_ID]:
            return
        emoji = payload.emoji
        reaction = discord.Reaction(message=message, data={"emoji": {"name": emoji.name, "id": emoji.id}, "me": False})


        # Create a discord.Reaction object
        has_leader_role = any(role.name.lower() == self.LEADER_ROLE.lower() for role in member.roles)
        if not has_leader_role:
            await reaction.remove(user)
            print(f"{member.mention} you are not allowed to use this command")
            return


        # Fetch the user who added the reaction
        user = self.bot.get_user(payload.user_id)
        embed = reaction.message.embeds[0]
        date = embed.timestamp.date()
        channel = reaction.message.channel
        mention_id = reaction.message.guild.get_member_named(
            embed.author)
        fields_values = {}

        for field in embed.fields:
            fields_values[field.name] = field.value
        fields_values['discord'] = embed.author.name.split('#')[0]
        fields_values['date'] = date.strftime("%d/%m/%Y")
        name = fields_values["discord"]
        applicant = guild.get_member_named(name)
        
        
        
        if reaction.emoji == "✅":
            try:
                print(applicant)
                await applicant.send(f"Accepted. You can now apply to {embed.footer.text}. Please apply in game {applicant.mention}!")
                await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
            except discord.Forbidden:
                await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
                print("forbidden exception")
            except discord.HTTPException:
                await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
                print("http exception")
            print(f'{reaction.users} has accepted {name} to {embed.footer.text} at {date.strftime("%m/%d/%Y")}')

        elif reaction.emoji == "❌":
            try:
                await payload.send_modal(RefusedModal())
                # await applicant.send(f"Thank you for considering {embed.footer.text}, but your application as been rejected. {applicant.mention}")
                # await channel.send(f"Thank you for considering {embed.footer.text}, but your application as been rejected. {applicant.mention}")
            except discord.Forbidden:
                await channel.send(f"Thank you for considering {embed.footer.text}, but your application as been rejected. {applicant.mention}")
                print("forbidden exception")
            except discord.HTTPException:
                await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
                print("http exception")
            print(f'{reaction.user} has rejected {name} from {embed.footer.text} at {date.strftime("%m/%d/%Y")}')

        elif reaction.emoji == "🕐":
            try:
                await applicant.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
                await channel.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
            except discord.Forbidden:
                await channel.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
                print("forbidden exception")
            except discord.HTTPException:
                await channel.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
                print("http exception")
            print(f"Inserting data into {embed.footer.text} waiting list")
            #insert_to_sheet(fields_values, 'stepbot', embed.footer.text)
