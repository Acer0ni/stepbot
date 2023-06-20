import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

class close_channel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="close_channel")
    async def cmd_apply(self, interaction: discord.Interaction):
        if "stepbot" not in [role.name.lower() for role in interaction.user.roles]:
            await interaction.response.send_message(content="You are not allowed to use this command", ephemeral=True)
            return
            
        guild = interaction.guild
        # leader_role = discord.utils.get(guild.roles, id=949428797478948864)
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            if not channel.name.startswith("report-") or not channel.name.startswith("leadership-"):
                await interaction.response.send_message(content="This command can only be used in report or leadership channel", ephemeral=True)
            return
            
        # overwrite = {
        # guild.default_role: discord.PermissionOverwrite(read_messages=False),
        # leader_role: discord.PermissionOverwrite(read_messages=True),
        # interaction.user: discord.PermissionOverwrite(read_messages=False)
        # }
        author_id = int(channel.name.split('-')[-1])
        author = interaction.guild.get_member(author_id)

        archive_category = discord.utils.get(interaction.guild.categories, name='archive')
        if archive_category is None:
            archive_category = await interaction.guild.create_category('archive')

        await channel.edit(category=archive_category, sync_permissions=True)
        print(f"Archived {channel.name} by {interaction.user.name}")
        await interaction.response.send_message(content="channel has been archived.", ephemeral=True)
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(close_channel(bot),guild=discord.Object(id=os.getenv("GUILD_ID"))) 
        print("cog added")