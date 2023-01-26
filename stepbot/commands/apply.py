from discord.ext import commands

class Apply(commands.Cog):

    @commands.command(name="apply")
    async def cmd_apply(self,ctx, clan_name: str):
        if clan_name == "abnormal":
            rules_message = await ctx.author.send("insert rules here abnormal")
            await rules_message.add_reaction("👍")
            await rules_message.add_reaction("👎")
        elif clan_name == "paradox":
            rules_message = await ctx.author.send("insert rules here other_clan")
            await rules_message.add_reaction("👍")
            await rules_message.add_reaction("👎")
        else:
            await ctx.author.send("Invalid clan name.")
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if reaction.emoji == "👍":
            await user.send("Here is the application form https://docs.google.com/forms/d/e/1FAIpQLSfurAyq_etyKwBl6guqHMCqK_U5CoxZX41mpYAanIXwACbK7g/viewform?usp=sf_link")
        elif reaction.emoji == "👎":
            await user.send("Thanks for your interest in our clan.")
