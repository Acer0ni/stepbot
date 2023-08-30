import discord
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
from stepbot.commands.apply2.apply_modal import *

class Dropdown(discord.ui.Select):
    def __init__(self):
        # Define the options you want in the select menu
        options = [
                discord.SelectOption(label='Abnormal', emoji='<a:bluecheck:1145758589584162876>'),
                discord.SelectOption(label='Paradox', emoji='<a:redcheck:1145758812414939257>'),
                discord.SelectOption(label='Anomaly', emoji='<a:orangecheck:1145758814675669002>'),
                discord.SelectOption(label='Paranormal', emoji='<a:greencheck:1145758816978350230>'),
            ]

        super().__init__(placeholder='Select an option...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # This is what happens when an option is selected
        clan_name = self.values[0]
        await interaction.response.send_modal(ApplyModal(clan_name=clan_name))

class SelectMenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class ApplyView(discord.ui.View):
    def __init__(self, embed: discord.Embed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed = embed
        self.timeout = None

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.green)
    async def callback(self, interaction, button):
        select_menu_view = SelectMenuView()
        await interaction.response.send_message("Choose from the dropdown:", view=select_menu_view, ephemeral=True)

class ClanView(commands.Cog):
    @app_commands.command(name="apply2")
    async def cmd_apply(self, interaction: discord.Interaction):
        embed = Embed(title="Apply to one of AbNorMaL Syndicate clans", description="Welcome to the server, if you wish to apply to one of ours clans, please click on the button to start the process. ", color=0x0068cf)
        apply_view = ApplyView(embed=embed)
        await interaction.response.send_message(view=apply_view, embed=embed)


    

    
