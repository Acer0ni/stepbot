import discord
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
from stepbot.commands.lft.modal import CommentModal
import os

class ClassDropdown(discord.ui.Select):
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
        cpView = CPView()
        await interaction.response.send_message("Choose a CP from the dropdown:", view=cpView, ephemeral=True)
        print(f"/!\ Lft Modal sent to {interaction.user.name} /!\ \n")

class CPDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='4m-6m'),
            discord.SelectOption(label='6m-8m'),
            discord.SelectOption(label='8m-10m'),
            discord.SelectOption(label='10m-12m'),
            discord.SelectOption(label='12m-15m'),
            discord.SelectOption(label='15m-18m'),
            discord.SelectOption(label='18m-21m'),
            discord.SelectOption(label='21m-25m'),
            discord.SelectOption(label='25m-30m'),
            discord.SelectOption(label='30m-36m'),
            discord.SelectOption(label='36m-42m'),
            discord.SelectOption(label='42m-48m'),
            discord.SelectOption(label='48m-55m'),
            discord.SelectOption(label='55m+'),
        ]
        super().__init__(placeholder='Select an option...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cp_name = self.values[0]
        print(f"[+] {interaction.user.name} has selected {cp_name}\n")
        qbView = QBView()
        await interaction.response.send_message("Choose a QB from the dropdown:", view=qbView, ephemeral=True)
        print(f"/!\ Lft Modal sent to {interaction.user.name} /!\ \n")

class QBDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='1/day', emoji='1️⃣'),
            discord.SelectOption(label='2/day', emoji='2️⃣'),
            discord.SelectOption(label='3/day', emoji='3️⃣'),
            discord.SelectOption(label='4/day', emoji='4️⃣'),
            discord.SelectOption(label='5/day', emoji='5️⃣'),
            discord.SelectOption(label='6+/day', emoji='6️⃣'),
        ]
        super().__init__(placeholder='Select an option...', min_values=1, max_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        qb_name = self.values[0]
        print(f"[+] {interaction.user.name} has selected {qb_name}\n")
        spendingView = SpendingView()
        await interaction.response.send_message("Choose a spending from the dropdown:", view=spendingView, ephemeral=True)
        print(f"/!\ Lft Modal sent to {interaction.user.name} /!\ \n")

class SpendingDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Free to play'),
            discord.SelectOption(label='passes only'),
            discord.SelectOption(label='Season packs'),
            discord.SelectOption(label='pearls'),
            discord.SelectOption(label='weekly pack'),
            discord.SelectOption(label='everything available'),
        ]
        super().__init__(placeholder='Select an option...', min_values=1, max_values=4, options=options)
    async def callback(self, interaction: discord.Interaction):
        spending_name = self.values[0]
        print(f"[+] {interaction.user.name} has selected {spending_name}\n")
        await interaction.response.send_modal(CommentModal())
        print(f"/!\ Lft Modal sent to {interaction.user.name} /!\ \n")
     
class ClassView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ClassDropdown())
        
class CPView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CPDropdown())

class QBView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(QBDropdown())

class SpendingView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SpendingDropdown())

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
    