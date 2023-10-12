import discord
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
import os

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Assasin', emoji='<:class_assassin:1130684641091801239>'),
            discord.SelectOption(label='Hunter', emoji='<:class_hunter:1130684645101535262>'),
            discord.SelectOption(label='Warlock', emoji='<:class_warlock:1130684646796042240>'),
            discord.SelectOption(label='Shaman', emoji='<:class_shaman:1130685189102768188>'),
            discord.SelectOption(label='Gladiator', emoji='<:class_gladiator:1130684661861990421>'),
            discord.SelectOption(label='Warrior', emoji='<:class_warrior:1130685292941148210>'),
            discord.SelectOption(label='Mage', emoji='<:class_mage:1130685050522964098>'),
            discord.SelectOption(label='Druid', emoji='<:class_druid:1130684942226038805>'),
        ]
        super().__init__(placeholder='Select an option...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        class_name = self.values[0]
        print(f"[+] {interaction.user.name} has selected {class_name}\n")
        #logic to be filled in here
        print(f"/!\ Lft Modal sent to {interaction.user.name} /!\ \n")

class ClassView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class LftView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = None

    @discord.ui.button(label="LFT", style=discord.ButtonStyle.green, custom_id="lft")
    async def callback(self, interaction, button):
        print(f"/!\ {interaction.user.name} has clicked on the lft button /!\ \n")
        class_view = ClassView()
        await interaction.response.send_message("Choose a class from the dropdown:", view=class_view, ephemeral=True)

class Lft(commands.Cog):
    @app_commands.command(name="lft")
    async def cmd_lft(self, interaction : discord.Interaction):
        member = interaction.user
        
        leader_role = int(os.getenv("LEADER_ROLE_ID"))
        leader_role = member.guild.get_role(leader_role)
        
        if leader_role in member.roles:
            print(f"[+] {interaction.user.name} has clicked on the lft button\n")
            embed = Embed(title="Post your information or fetch information for new team", description="Please choose one of the two options to start the process", color=0x0068cf)
            lft_view = LftView()
            await interaction.response.send_message(view=lft_view, embed=embed)
        else:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    