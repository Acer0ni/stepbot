import discord
from discord.ext import commands
from discord import app_commands
import traceback
from dotenv import load_dotenv
import os

class dm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="dm")
    async def cmd_apply(self, interaction: discord.Interaction, role: discord.Role, message: str):
        count = 0
        failed = 0
        channel = interaction.guild.get_channel(int(os.getenv("NERDPLAYGROUND_CHANNEL_ID"))) # nerd playground channel id

        if "stepbot" not in [role.name.lower() for role in interaction.user.roles]:
            await interaction.response.send_message(content="You are not allowed to use this command", ephemeral=True)
            print(f"/!\ {member.name}tried to use this command and is not allowed /!\ \n")
            return        
            
        for member in role.members:
            try:
                # send a direct message to the member
                await member.send(message)
                count += 1
                print(f"[+]\tSent a message to {member.name}.")
                print(f"[+]\tSent a message to {count}/{len(role.members)} members.\n")
            except:
                # catch any errors and print them
                failed += 1
                print(f"[-]\tFailed to send a message to {member.name}.")
                print(f"[-]\tFailed to send a message to {failed}/{len(role.members)} members.\n")
                await channel.send(f'Couldnt send the message to {member.name}')
        await channel.send(f'/!\ Sent message to {count}/{len(role.members)} members and failed to sent a message to {failed}/{len(role.members)} /!\.')
    
    async def setup(bot: commands.Bot): 
        await bot.add_cog(dm(bot),guild=discord.Object(id=os.getenv("GUILD_ID"))) 
        print(f"[+] DM command Cog added")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)