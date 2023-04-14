import discord
from discord.ext import commands
from discord import app_commands
import os

class report(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="report")
    async def cmd_apply(self, interaction: discord.Interaction, message: str, message_link: str):
        guild = interaction.guild
        leader_role = discord.utils.get(guild.roles, id=int(os.getenv("CONFLICT_ROLE_ID")))

        overwrite = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            leader_role: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }

        channel_name = f"Report-{interaction.user.name}-{interaction.user.id}"
        channel = await guild.create_text_channel(channel_name, overwrites=overwrite)
        print(f"Created report channel {channel_name} for {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})")

        embed = discord.Embed(title="Report", description=message, color=discord.Colour.red(), timestamp=interaction.created_at)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.add_field(name="Reported By", value=interaction.user.mention,inline=False)
        embed.add_field(name="Joined Server At", value=interaction.user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        embed.add_field(name="Sent from", value=f"[Jump to message]({message_link})",inline=False)
        await channel.send(embed=embed)
        await channel.send(leader_role.mention)
        await channel.send(interaction.user.mention)
        await interaction.response.send_message(f'Report sent to {leader_role.mention}', ephemeral=True)

    async def setup(bot: commands.Bot): 

        await bot.add_cog(report(bot),guild=discord.Object(id=os.getenv("GUILD_ID"))) 
        print("cog added")