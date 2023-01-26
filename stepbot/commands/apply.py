from discord.ext import commands


class Apply(commands.Cog):

    @commands.command(name="apply")
    async def cmd_apply(self,ctx):
      rules_message =  await ctx.author.send("insert rules here")
      await rules_message.add_reaction("👍")
      await rules_message.add_reaction("👎")
