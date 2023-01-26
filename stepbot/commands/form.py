from discord import ui

questions = ['What is your in game name?', 'What clan are you applying for?', 'How many members of your team are applying?',
             'What is the CP of the requested members?', 'What is the clals of the requested members?']


class Questionnaire(ui.Modal, title='Questionnaire Response'):

    async def on_submit(self, ctx, interaction: discord.Interaction):
        answers = []
        for i in questions:
            await self.send(i)
            try:
                message = await self.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timout=30)
            except:
                break
            if len(questions) != len(answers):
                pass  # gj wait for leadershitp
            else:
                pass  # try again
