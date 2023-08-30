import discord
from discord.ext import commands
from discord import app_commands
from stepbot.commands.group.modal import GroupModal
import os

class group(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD_ID = int(os.getenv("GUILD_ID"))

    @app_commands.command(name="group")
    async def cmd_apply(self, interaction: discord.Interaction):
        """
        Find or create a group for diablo 4
        """
        await interaction.response.send_modal(GroupModal())
        embed = interaction.message.embeds[0]
        fields_values = {}
        for field in embed.fields:
            fields_values[field.name] = field.value
        player_info = { "Discord" : interaction.user.name, "Battle Net" : fields_values["Battle Net"], "Class" : fields_values["Class"], "Disponibility" : ["Disponibility"]}
        print(f"{player_info}")
        # view = View()
        # view.add_item(player_info['Discord'])
        # view.add_item(player_info['Battle Net'])
        # view.add_item(player_info['Class'])
        # view.add_item(player_info['Disponibility'])
        # view.add_item(Button(style=discord.ButtonStyle.green, label="Accept"))
        

    # async def setup(bot: commands.Bot): 

    #     await bot.add_cog(leadership(bot),guild=discord.Object(id=1008278641660149860)) 
    #     print("cog added1")
