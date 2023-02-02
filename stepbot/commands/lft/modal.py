import discord
import traceback
import datetime

class LftModall(discord.ui.Modal, title = 'LFT form'):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    ign = discord.ui.TextInput(
        label='Please enter your IGN',
        placeholder='Player1',
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )
    cp = discord.ui.TextInput(
        label='Please enter your CP',
        placeholder='10 000 000',
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )
    role = discord.ui.TextInput(
        label='Please enter the class',
        placeholder='Mage',
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )
    spending = discord.ui.TextInput(
        label='Please enter your spending level',
        placeholder='F2P',
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )

    def validate_name(self):
        num = 1
        names = self.ign.value.split(",")  # split the names by comma
        roles = self.role.value.split(",")

        if len(names) != num:  # check if the number of names entered is equal to 1
            raise ValueError(
                "Please input your IGN correctly")
        if len(roles) != num:  # check if the number of class entered is equal to 1
            raise ValueError(
                "Please input your class correctly")
        
        for ign in names:
            if len(ign.strip()) < 1:  # check if the names are not empty
                raise ValueError(
                    "Please input your IGN correctly")
        for role in roles:
            if len(role.strip()) < 1:  # check if the class are not empty
                raise ValueError(
                    "Please input your class correctly")
    
    def validate_cp(self):
        num = 1
        cps = self.cp.value.split(",")
        if len(cps) != num:
            raise ValueError(
                "Please input your CP correctly no commas")
        for cp in cps:
            if len(cp.strip()) < 1:
                raise ValueError(
                    "Please input your CP correctly no commas")
    
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
        embed = discord.Embed(title='Looking for team', color=0x9b59b6)
        embed.add_field(name='IGN', value=self.ign.value, inline=False)
        embed.add_field(name='CP', value=self.cp.value, inline=False)
        embed.add_field(name='Class', value=self.role.value, inline=False)
        embed.add_field(name='Spending', value=self.spending.value, inline=False)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.timestamp = date
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)