import discord
import traceback
import datetime
import os
from dotenv import load_dotenv


class LeaderModal(discord.ui.Modal, title='Leadership form'):

    def __init__(self, clan_name, *args, **kwargs):
        self.clan_name = clan_name
        self.ALL_LEADER_ABNORMAL = int(os.getenv("ALL_LEADER_ABNORMAL"))
        self.ALL_LEADER_PARADOX = int(os.getenv("ALL_LEADER_PARADOX"))
        self.ALL_LEADER_ANOMALY = int(os.getenv("ALL_LEADER_ANOMALY"))
        self.ALL_LEADER_PARANORMAL = int(os.getenv("ALL_LEADER_PARANORMAL"))
        super().__init__(*args, **kwargs)

    # This is a short, single-line input, where user can submit the number of players applying
    ign = discord.ui.TextInput(
        label='What is your in-game name?',
        style=discord.TextStyle.short,
        placeholder='Artzx',
        required=True,
    )
    # This is a long, multi-line input, where user can submit the IGN of the player(s) applying
    experience = discord.ui.TextInput(
        label='How long have you been playing the game?',
        style=discord.TextStyle.short,
        placeholder='1 year',
        required=True,
    )
    # This is a long, multi-line input, where user can submit the CP of the player(s) applying
    good_elder = discord.ui.TextInput(
        label='What would make you a qualified elder?',
        style=discord.TextStyle.long,
        placeholder='Im as good as it gets',
        required=True,
    )
    # This is a long, multi-line input, where user can submit the role of the player(s) applying
    time_zone = discord.ui.TextInput(
        label='What is your time zone?',
        placeholder='Est, Cst, Mst, Pst, etc.',
        style=discord.TextStyle.short,
        required=True,
        max_length=10
    )
    what_role = discord.ui.TextInput(
        label='What role do you want to play in the clan?',
        style=discord.TextStyle.long,
        placeholder='Cp recording, recruitment, planning, etc.',
        required=True,
    )

    def get_clan_id_from_name(self):
        leader_role_id = None
        match self.clan_name.lower():
            case "abnormal":
                leader_role_id = self.ALL_LEADER_ABNORMAL
            case "paradox":
                leader_role_id = self.ALL_LEADER_PARADOX
            case "anomaly":
                leader_role_id = self.ALL_LEADER_ANOMALY
            case "paranormal":
                leader_role_id = self.ALL_LEADER_PARANORMAL
            case _:
                raise ValueError("invalid clan name")
        return leader_role_id
    
    async def create_channel(self, interaction: discord.Interaction):
        guild = interaction.guild
        leader_role_id = self.get_clan_id_from_name()
        leader_role = guild.get_role(leader_role_id)
        overwrite = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            leader_role: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        channel_name = f"Leadership Application-{interaction.user.name}-{interaction.user.id}"
        channel = await guild.create_text_channel(channel_name, overwrites=overwrite)
        return channel

    async def on_submit(self, interaction: discord.Interaction):
        # print(f"Validating {interaction.user} application")
        # self.validate_on_submit()
        # print(f"application of {interaction.user} is valid ")
        create_channel = await self.create_channel(interaction)
        date = datetime.datetime.now()
        leader_role_id = self.get_clan_id_from_name()
        leader_role = interaction.guild.get_role(leader_role_id)
        

        embed = discord.Embed(title='Application Submition', color=discord.Color.blue())
        embed.add_field(name='What is your in-game name?', value=self.ign.value, inline=False)
        embed.add_field(name='How long have you been playing the game?', value=self.experience.value, inline=False)
        embed.add_field(name='What would make you a qualified elder?', value=self.good_elder.value, inline=False)
        embed.add_field(name='What is your timezone', value=self.time_zone.value, inline=False)
        embed.add_field(name='What role do you want to play in the clan?', value=self.what_role.value, inline=False)
        embed.set_author(name=interaction.user,icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.set_footer(text=self.clan_name)

        embed.timestamp = date
        msg = await create_channel.send(embed=embed)
        await msg.pin()
        await create_channel.send(interaction.user.mention)
        await create_channel.send(leader_role.mention)
        print(f"application of {interaction.user} sent to {create_channel.name}")

        # delete this line after testing
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error, ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
