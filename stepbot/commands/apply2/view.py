import discord
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
from stepbot.commands.apply2.apply_modal import *

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
                discord.SelectOption(label='Abnormal', emoji='<a:bluecheck:1145758589584162876>', description='CP : 24m+ | Full team Prefered'),
                discord.SelectOption(label='Paradox', emoji='<a:redcheck:1145758812414939257>', description='CP : 18m+ | Full Team Prefered'),
                discord.SelectOption(label='Anomaly', emoji='<a:orangecheck:1145758814675669002>', description='CP : 15m+'),
                discord.SelectOption(label='Paranormal', emoji='<a:greencheck:1145758816978350230>', description='CP : 15m+'),
            ]
        super().__init__(placeholder='Select an option...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        clan_name = self.values[0]
        await interaction.response.send_modal(ApplyModal(clan_name=clan_name))

class SelectMenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class ApplyView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = None

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.green, custom_id="apply")
    async def callback(self, interaction, button):
        select_menu_view = SelectMenuView()
        await interaction.response.send_message("Choose from the dropdown:", view=select_menu_view, ephemeral=True)

class ClanView(commands.Cog):
    @app_commands.command(name="apply2")
    async def cmd_apply(self, interaction: discord.Interaction):
        member = interaction.user
        
        leader_role = int(os.getenv("LEADER_ROLE_ID"))
        print(leader_role)
        leader_role = member.guild.get_role(leader_role)
        
        if leader_role in member.roles:
            embed = Embed(title="Apply to one of AbNorMaL Syndicate clans", description="Welcome to the server, if you wish to apply to one of ours clans, please click on the button to start the process. ", color=0x0068cf)
            apply_view = ApplyView()
            await interaction.response.send_message(view=apply_view, embed=embed)
        else:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)



    

    
