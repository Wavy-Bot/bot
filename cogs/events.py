from discord.ext import commands


class Events(commands.Cog):
    """Class that contains all the bot events."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is done preparing the data received from Discord."""
        print(f'Logged in as\n{self.bot.user.name}\n{self.bot.user.id}')


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Events(bot))
