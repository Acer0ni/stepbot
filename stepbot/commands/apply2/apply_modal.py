import discord
import traceback
import datetime
from stepbot.commands.apply2.apply_resp_view import *
import os

class ApplyModal(discord.ui.Modal, title='Application form'):
    def __init__(self, clan_name, *args, **kwargs):
        self.clan_name = clan_name
        self.ABNORMAL_THREAD_ID = int(os.getenv("ABNORMAL_THREAD_ID"))
        self.PARADOX_THREAD_ID = int(os.getenv("PARADOX_THREAD_ID"))
        self.ANOMALY_THREAD_ID = int(os.getenv("ANOMALY_THREAD_ID"))
        self.PARANORMAL_THREAD_ID = int(os.getenv("PARANORMAL_THREAD_ID"))
        super().__init__(*args, **kwargs)

    # This is a short, single-line input, where user can submit the number of players applying
    number = discord.ui.TextInput(
        label='Number of players applying',
        placeholder='Input a number between 1-4',
        style=discord.TextStyle.short,
        required=True,
        max_length=1,
    )
    # This is a long, multi-line input, where user can submit the IGN of the player(s) applying
    ign = discord.ui.TextInput(
        label='IGN of requested members separated by commas',
        style=discord.TextStyle.long,
        placeholder='Player1, Player2, Player3',
        required=True,
        max_length=300,
    )
    # This is a long, multi-line input, where user can submit the CP of the player(s) applying
    cp = discord.ui.TextInput(
        label='CP of requested members separated by comma',
        style=discord.TextStyle.long,
        placeholder='10 000 000, 20 000 000, 30 000 000',
        required=True,
        max_length=100,
    )
    # This is a long, multi-line input, where user can submit the role of the player(s) applying
    role = discord.ui.TextInput(
        label='Please enter the class',
        placeholder='Mage, Warrior, Hunter, Shaman, Druid, Gladiator, Warlock, Assassin.',
        style=discord.TextStyle.long,
        required=True,
        max_length=100,
    )
    teammates = discord.ui.TextInput(
        label='teammates already in the clan (if applicable)',
        placeholder='Player1, Player2, Player3',
        style=discord.TextStyle.short,
        required=False,
    )
    # get the thread id based on the clan name passed in

    def get_clan_id_from_name(self):
        thread_id = None
        match self.clan_name:
            case "Abnormal":
                thread_id = self.ABNORMAL_THREAD_ID
            case "Paradox":
                thread_id = self.PARADOX_THREAD_ID
            case "Anomaly":
                thread_id = self.ANOMALY_THREAD_ID
            case "Paranormal":
                thread_id = self.PARANORMAL_THREAD_ID
            case _:
                raise ValueError("invalid clan name")
        return thread_id

    def validate_number(self):  # validate the number of players applying
        try:
            num = int(self.number.value)  # get the number of players applying
            if num < 1 or num > 4:  # check if the number of players applying is between 1-4
                raise ValueError()

        except ValueError:
            raise ValueError(
                "number of members applying must be a number between 1-4")

    def validate_name(self):
        num = int(self.number.value)  # get the number of players applying
        names = self.ign.value.split(",")  # split the names by comma
        roles = self.role.value.split(",")

        if len(names) != num:  # check if the number of names entered is equal to the number of players applying
            raise ValueError(
                "please input the correct number of names separated by a comma")
        if len(roles) != num:  # check if the number of names entered is equal to the number of players applying
            raise ValueError(
                "please input the correct number of classes separated by a comma")
        
        for ign in names:
            if len(ign.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "please input the correct number of names separated by a comma")
        for role in roles:
            if len(role.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "please input the correct number of classes separated by a comma")

    def validate_cp(self):  # same as validate_name
        num = int(self.number.value)
        cps = self.cp.value.split(",")
        if len(cps) != num:
            raise ValueError(
                "please input the correct number of cp values separated by a comma")
        for cp in cps:
            if len(cp.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "please input the correct number of cp values separated by a comma")

    def validate_on_submit(self):  # validate all the fields
        for value in ["number", "name", "cp", "role"]:  # loop through all the fields
            # get the validator for the field
            if validator := getattr(self, f"validate_{value}", None):
                if not callable(validator):  # check if the validator is callable
                    raise RuntimeError(
                        f"validator attribute found but not callable {validator}")
                validator()

    async def on_submit(self, interaction: discord.Interaction):
        print(f"[+] Validating {interaction.user} application")
        self.validate_on_submit()
        print(f"[+] application of {interaction.user} is valid ")
        date = datetime.datetime.now()

        embed = discord.Embed(title=f'Application Submitted by {interaction.user.name}')
        embed.add_field(name='Number of applicant(s): ',value=self.number.value, inline=True)
        embed.add_field(name='Name of applicant(s): ', value=self.ign.value, inline=True)
        embed.add_field(name=' ', value=' ')
        embed.add_field(name='CP of applicant(s)', value=self.cp.value, inline=False)
        embed.add_field(name='Class of applicant(s)', value=self.role.value, inline=False)
        embed.add_field(name='Teammates in clan:', value=self.teammates.value, inline=False)
        embed.set_author(name=interaction.user,icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.set_footer(text=self.clan_name)
        embed.set_image(url='https://i.imgur.com/10JUDEm.jpg')

        embed.timestamp = date
        thread_id = self.get_clan_id_from_name()
        clan_thread = interaction.client.get_channel(thread_id)
        view = ApplicationResponseView()
        await clan_thread.send(embed=embed, view=view)

        await clan_thread.send(interaction.user.mention)
        print(f"[+] Application of {interaction.user} sent to {clan_thread}")

        # delete this line after testing
        await interaction.response.send_message(content=f"Your application has been received and sent to {clan_thread.mention}", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
