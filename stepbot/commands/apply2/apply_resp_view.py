import discord
from stepbot.commands.sheet import *
from stepbot.commands.apply2.denial_modal import DenialReasonModal
import traceback
import datetime

class ApplicationResponseView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = None
    async def get_applicant_from_interaction(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = interaction.message.embeds[0]
        date = embed.timestamp.date()
        channel = interaction.message.channel

        fields_values = {}
        for field in embed.fields:
            fields_values[field.name] = field.value
        fields_values['discord'] = embed.author.name.split('#')[0]
        fields_values['date'] = date.strftime("%d/%m/%Y")
        
        name = fields_values["discord"]
        applicant = guild.get_member_named(name)

        return applicant,channel,fields_values
    
    def has_leader_role(self, member: discord.Member) -> bool:
        leader_role = member.guild.get_role(int(os.getenv("LEADER_ROLE_ID")))
        return leader_role in member.roles


    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.has_leader_role(interaction.user):
            applicant, channel,field_values = await self.get_applicant_from_interaction(interaction)
            embed = interaction.message.embeds[0]
            print(f'[+] {interaction.user.name} has accepted {applicant.name} to {embed.footer.text} at {embed.timestamp.strftime("%m/%d/%Y")}\n')
            try:
                button.label = "Application accepted"
                self.timeout = 60
                await DenialReasonModal.disable_buttons(self)
                await interaction.message.edit(view=self)
                await applicant.send(f"Accepted. You can now apply to {embed.footer.text}. Please apply in game {applicant.mention}!")
                await interaction.response.send_message(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game. If you change your mind, please contact a leader.")
            except discord.Forbidden:
                await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
                print("forbidden exception")
            except discord.HTTPException:
                await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
                print("http exception")
                #print(f'{reaction.users} has accepted {name} to {embed.footer.text} at {date.strftime("%m/%d/%Y")}')
        else:
            await interaction.response.send_message(content="You are not allowed to use this command", ephemeral=True)
            print(f"/!\ {interaction.user.name} tried to use this command and is not allowed /!\\n")
            return
        
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.has_leader_role(interaction.user):
            applicant, channel,field_values = await self.get_applicant_from_interaction(interaction)
            modal = DenialReasonModal(applicant=applicant, channel=channel)
            await interaction.response.send_modal(modal)
            button.label = "Application denied"
            await DenialReasonModal.disable_buttons(self)
            await interaction.message.edit(view=self)
            self.timeout = 60
        else:
            await interaction.response.send_message(content="You are not allowed to use this command", ephemeral=True)
            print(f"/!\ {interaction.user.name} tried to use this command and is not allowed /!\ \n")
            return


    @discord.ui.button(label="Pending", style=discord.ButtonStyle.secondary, custom_id="pending")
    async def pending_button(self, interaction: discord.Interaction, button: discord.ui.Button,):
        if self.has_leader_role(interaction.user):
            applicant, channel, fields_values = await self.get_applicant_from_interaction(interaction)
            embed = interaction.message.embeds[0]
            try:
                button.label = "Application waitlisted"
                button.disabled = True
                await interaction.message.edit(view=self)
                await applicant.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
                await interaction.response.send_message(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
            except discord.Forbidden:
                await channel.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
                print("forbidden exception")
            except discord.HTTPException:
                await channel.send(f'Hey {applicant.mention}, we are full right now in {embed.footer.text}, you have been added to the waiting list, and we will get back to you when there is room.')
                print("http exception")
                print(f"Inserting data into {embed.footer.text} waiting list")
            insert_to_sheet(fields_values, 'stepbot', embed.footer.text)
        else:
            await interaction.response.send_message(content="You are not allowed to use this command", ephemeral=True)
            print(f"/!\ {interaction.user.name} tried to use this command and is not allowed /!\ \n")
            return


