import discord
import traceback
import datetime

class lftModall(discord.ui.View, title = 'LFT form'):

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

