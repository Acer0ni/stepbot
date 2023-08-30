import discord
from stepbot.commands.sheet import *
from stepbot.commands.apply2.denial_modal import DenialReasonModal
import traceback
import datetime

class ApplicationResponseView(discord.ui.View):
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
    


    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        applicant, channel,field_values = await self.get_applicant_from_interaction(interaction)
        embed = interaction.message.embeds[0]
        try:
            print(applicant)
            button.label = "Application accepted"
            await interaction.message.edit(view=self)
            await applicant.send(f"Accepted. You can now apply to {embed.footer.text}. Please apply in game {applicant.mention}!")
            await interaction.response.send_message(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
        except discord.Forbidden:
            await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
            print("forbidden exception")
        except discord.HTTPException:
            await channel.send(f"{applicant.mention} you have been accepted to {embed.footer.text}, please apply in game.")
            print("http exception")
            #print(f'{reaction.users} has accepted {name} to {embed.footer.text} at {date.strftime("%m/%d/%Y")}')
        
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        applicant, channel,field_values = await self.get_applicant_from_interaction(interaction)
        modal = DenialReasonModal(applicant=applicant, channel=channel)
        await interaction.response.send_modal(modal)
        button.label = "Application denied"
        await interaction.message.edit(view=self)


    @discord.ui.button(label="Pending", style=discord.ButtonStyle.secondary, custom_id="pending")
    async def pending_button(self, interaction: discord.Interaction, button: discord.ui.Button,):
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
        button.label = "Application waitlisted"
        insert_to_sheet(fields_values, 'stepbot', embed.footer.text)