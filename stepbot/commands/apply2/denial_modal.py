import discord
import traceback



class DenialReasonModal(discord.ui.Modal, title='Deny Application'):
    def __init__(self, applicant: discord.Member, channel: discord.TextChannel):
        self.applicant = applicant
        self.channel = channel
        super().__init__()

    reason = discord.ui.TextInput(
        label='Enter the reason for denial',
        placeholder='Type your reason here...',
        style=discord.TextStyle.long,
        required=True,
        max_length=300,
    )

    async def disable_buttons(self):
        for button in self.children:
            if isinstance(button, discord.ui.Button):
                button.disabled = True

    async def on_submit(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        try:
            await interaction.response.send_message(f"Your Application was denied {self.applicant.mention} please check your Dm's for more information on the reason.")
            await self.applicant.send(f"Your application to {embed.footer.text} was denied for the following reason: {self.reason.value}")
        except discord.Forbidden:
            await self.channel.send(f"Your Application was denied {self.applicant.mention} please reach out to {embed.footer.text} leadership for more information on the reason.")
            print("forbidden exception")
        except discord.HTTPException:
            await self.channel.send(f"Your Application was denied {self.applicant.mention} please reach out to {embed.footer.text} leadership for more information on the reason.")
            print("http exception")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
