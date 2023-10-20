import discord
import traceback
import datetime

class CommentModal(discord.ui.Modal, title="Other comment"):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    comment = discord.ui.TextInput(
        label="Please enter any other comment",
        placeholder="Enter your comment here",
        style=discord.TextStyle.long,
        min_length=1,
        max_length=1000,
    )
    async def on_submit(self, interaction: discord.Interaction):
        comment = self.comment._value
        print(f"[+] {interaction.user.name} has entered {comment}\n")
        #logic here
        print(f"/!\ Lft Modal sent to {interaction.user.name} /!\ \n")
        await interaction.response.send_message("Your LFT has been saved, you'll be notified if someone is interested in your post", ephemeral=True)
