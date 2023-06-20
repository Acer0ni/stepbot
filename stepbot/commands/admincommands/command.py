import discord
import os
from discord.ext import commands




class AdminCommands(commands.Cog):


    def __init__(self,bot:commands.bot):
        self.bot = bot
        self.GUILD_ID = int(os.getenv("GUILD_ID"))

    
    @commands.command(name = "sync")
    async def cmd_sync(self,ctx:commands.context):
        if "developer" not in [role.name.lower() for role in ctx.author.roles]:
            await ctx.send("command not authorized")
        else:
            await self.bot.tree.sync(guild=discord.Object(id=self.GUILD_ID))
            await ctx.send("tree synced")
            print("tree synced")