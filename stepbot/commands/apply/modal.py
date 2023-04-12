import discord
import traceback
import datetime
import os
from dotenv import load_dotenv


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
        placeholder='1',
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

    # get the thread id based on the clan name passed in

    def get_clan_id_from_name(self):
        thread_id = None
        match self.clan_name:
            case "abnormal":
                thread_id = self.ABNORMAL_THREAD_ID
            case "paradox":
                thread_id = self.PARADOX_THREAD_ID
            case "anomaly":
                thread_id = self.ANOMALY_THREAD_ID
            case "paranormal":
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
        for ign in names:
            if len(ign.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "please input the correct number of names separated by a comma")

    def validate_cp(self):  # same as validate_name
        num = int(self.number.value)
        cps = self.cp.value.split(",")
        if len(cps) != num:
            raise ValueError( "please input the correct number of cp values separated by a comma")
        for cp in cps:
            if len(cp.strip()) < 1:  # check if the names are not empty
                raise ValueError("please input the correct number of cp values separated by a comma")
        for cp in cps:
            try:
                int(cp.strip())  # check if the cp values are numbers
            except ValueError:
                raise ValueError(
                    "please input only numbers for cp values separated by a comma")

    def validate_role(self):
        num = int(self.number.value)
        roles = self.role.value.split(",")
        if len(roles) != num:
            raise ValueError("please input the correct number of roles seperated by comma")
        
    def validate_on_submit(self):  # validate all the fields
        for value in ["number", "name", "cp", "role"]:  # loop through all the fields
            # get the validator for the field
            if validator := getattr(self, f"validate_{value}", None):
                if not callable(validator):  # check if the validator is callable
                    raise RuntimeError(
                        f"validator attribute found but not callable {validator}")
                validator()

    async def on_submit(self, interaction: discord.Interaction):
        self.validate_on_submit()
        date = datetime.datetime.now()

        embed = discord.Embed(title='Application Submitted',
                              description=f'IGN: {self.number.value}')
        embed.add_field(name='Number',
                        value=self.number.value, inline=False)
        embed.add_field(name='IGN', value=self.ign.value, inline=False)
        embed.add_field(name='CP', value=self.cp.value, inline=False)
        embed.add_field(name='Role', value=self.role.value, inline=False)
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.set_footer(text=self.clan_name)

        embed.timestamp = date
        thread_id = self.get_clan_id_from_name()
        clan_thread = interaction.client.get_channel(thread_id)
        msg = await clan_thread.send(embed=embed)
        await clan_thread.send(interaction.user.mention)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("🕐")

        print(f'{interaction.user} submitted an application for {self.clan_name} at {date}')

        # delete this line after testing
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

