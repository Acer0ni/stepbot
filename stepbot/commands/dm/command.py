import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

class dm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="dm")
    async def cmd_apply(self, interaction: discord.Interaction, role: discord.Role, message: str):
        if "step-bot" not in [role.name.lower() for role in interaction.user.roles]:
            await interaction.response.send_message(content="You are not allowed to use this command", ephemeral=True)
            print("not allowed to use this command")
            return

        
        channel = interaction.guild.get_channel(int(os.getenv("NERDPLAYGROUND_CHANNEL_ID"))) # nerd playground channel id

        if role is None:
            await interaction.response.send_message(content="Invalid Role Selected", ephemeral=True)
            return
            
        for member in role.members:
            try:
                # send a direct message to the member
                await member.send(message)
                
            except:
                # catch any errors and print them
                print(f"Failed to send a message to {member.name}.")
                await channel.send(f'Couldnt send the message to {member.name}')
        await interaction.response.send_message(f'Sent message to {len(role.members)} members.', ephemeral=True)
    
    async def setup(bot: commands.Bot): 

        await bot.add_cog(dm(bot),guild=discord.Object(id=os.getenv("GUILD_ID"))) 
        print("cog added")