import discord
import traceback
import datetime
import os
from dotenv import load_dotenv


class RefusedModal(discord.ui.Modal, title='Refusal reason'):

    def __init__(self, clan_name, *args, **kwargs):
        self.clan_name = clan_name
        self.ABNORMAL_THREAD_ID = int(os.getenv("ABNORMAL_THREAD_ID"))
        self.PARADOX_THREAD_ID = int(os.getenv("PARADOX_THREAD_ID"))
        self.ANOMALY_THREAD_ID = int(os.getenv("ANOMALY_THREAD_ID"))
        self.PARANORMAL_THREAD_ID = int(os.getenv("PARANORMAL_THREAD_ID"))
        super().__init__(*args, **kwargs)

    # This is a short, single-line input, where user can submit the number of players applying
    reason = discord.ui.TextInput(
        label='Refusal reason',
        placeholder='Too low CP',
        style=discord.TextStyle.long,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        refusal_reason = self.reason.value

        # delete this line after testing
        
        await interaction.response.send_message(content=refusal_reason, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
