import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import traceback

# The guild in which this slash command will be registered.
# It is recommended to have a test guild to separate from your "production" bot
TEST_GUILD = discord.Object(323528876770852864)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self) # Create a command tree

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        # Sync the application command with Discord.
        await self.tree.sync(guild=TEST_GUILD)


class Apply(discord.ui.Modal, title='Apply',):
    # This is a short, single-line input, where user can submit the number of players applying
    number = discord.ui.TextInput(
        label='Number of players applying',
        placeholder='1',
        style=discord.TextStyle.short,
        required=True,
        max_length=1
    )
    # This is a long, multi-line input, where user can submit the IGN of the player(s) applying
    name = discord.ui.TextInput(
        label='Please enter IGN of requested members',
        style=discord.TextStyle.long,
        placeholder='Player1, Player2, Player3',
        required=True,
        max_length=300,
    )
    cp = discord.ui.TextInput(
        label='Please enter the CP of requested members',
        style=discord.TextStyle.long,
        placeholder='10 000 000, 20 000 000, 30 000 000',
        required=True,
        max_length=100,
    )
    role = discord.ui.TextInput(
        label='Please enter the class',
        placeholder='Mage, Warrior, etc.',
        style=discord.TextStyle.long,
        required=True,
        max_length=100,
    )


    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Application Submitted', description=f'IGN: {self.number.value}')
        embed.add_field(name='Number of players applying', value=self.number.value, inline=False)
        embed.add_field(name='IGN', value=self.name.value, inline=False)
        embed.add_field(name='CP', value=self.cp.value, inline=False)
        embed.add_field(name='Role', value=self.role.value, inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


client = MyClient()


@client.tree.command(guild=TEST_GUILD, description="test slash command")
async def apply(interaction: discord.Interaction):
    # Send the modal with an instance of our `Feedback` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(Apply())


client.run(TOKEN)