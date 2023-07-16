import discord
import traceback
import datetime
import os
from discord.ui import View, Button
from dotenv import load_dotenv


class GroupModal(discord.ui.Modal, title='Group Finder'):

    # This is a short, single-line input, where user can submit the number of players applying
    btag = discord.ui.TextInput(
        label='What is your in-game name?',
        style=discord.TextStyle.short,
        placeholder='Artzx',
        required=True,
    )
    # This is a long, multi-line input, where user can submit the IGN of the player(s) applying
    character = discord.ui.TextInput(
        label='How long have you been playing the game?',
        style=discord.TextStyle.short,
        placeholder='1 year',
        required=True,
    )
    # This is a long, multi-line input, where user can submit the CP of the player(s) applying
    availability = discord.ui.TextInput(
        label='What would make you a qualified elder?',
        style=discord.TextStyle.long,
        placeholder='Im as good as it gets',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # This is called when the user presses the submit button.
        embed = discord.Embed(title="Group Finder", description="Player info")
        embed.set_author(name=interaction.user,icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.add_field(name="Battle Net", value=self.btag.value, inline=False)
        embed.add_field(name="Class", value=self.character.value, inline=False)
        embed.add_field(name="Disponibility", value=self.availability.value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        interaction.response.e
        return embed
        
       
        # delete this line after testing
        #await interaction.response.send_message(view=view, ephemeral=True)
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)