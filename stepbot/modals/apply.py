import discord
import traceback


class ApplyModal(discord.ui.Modal, title='Apply'):
    
    def __init__(self, clan_name, *args, **kwargs):
        self.clan_name = clan_name
        super().__init__(*args, **kwargs)

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
    # get the tread id based on the clan name passed in

    def get_clan_id_from_name(self):
        thread_id = None
        match self.clan_name:
            case "abnormal":
                thread_id = 1068628252974911620  # To hide in .env file
            case "paradox":
                thread_id = 1068691717605302422  # To hide in .env file
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
        names = self.name.value.split(",")  # split the names by comma
        if len(names) != num:  # check if the number of names entered is equal to the number of players applying
            raise ValueError(
                "please input the correct number of names separated by a comma")
        for name in names:
            if len(name.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "please input the correct number of names separated by a comma")

    def validate_cp(self):  # same as validate_name
        num = int(self.number.value)
        cps = self.cp.value.split(",")
        if len(cps) != num:
            raise ValueError(
                "please input the correct number of cp values separated by a comma")
        for name in cps:
            if len(name.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "please input the correct number of cp values separated by a comma")

    def validate_on_submit(self): # validate all the fields
        for value in ["number", "name", "cp", "role"]: # loop through all the fields
            if validator := getattr(self, f"validate_{value}", None): # get the validator for the field
                if not callable(validator): # check if the validator is callable
                    raise RuntimeError(
                        f"validator attribute found but not callable {validator}")
                validator()

    async def on_submit(self, interaction: discord.Interaction):
        self.validate_on_submit()
        embeds = []
        
        embed = discord.Embed(title='Application Submitted',
                              description=f'IGN: {self.number.value}')
        embed.add_field(name='Number of players applying',
                        value=self.number.value, inline=False)
        embed.add_field(name='IGN', value=self.name.value, inline=False)
        embed.add_field(name='CP', value=self.cp.value, inline=False)
        embed.add_field(name='Role', value=self.role.value, inline=False)
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        thread_id = self.get_clan_id_from_name()
        clan_thread = interaction.client.get_channel(thread_id)
        msg = await clan_thread.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
       # await msg.add_reaction("🕐")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        embeds.append(msg.id)
        print(embeds)
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
