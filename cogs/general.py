import os

import discord

from discord.ext import commands

EMB_COLOUR = int(os.getenv("COLOUR"), 16)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot."""

        embed = discord.Embed(
            title="Pong :ping_pong:",
            description=f"Heartbeat: {round(self.bot.latency * 1000)}ms",
            colour=EMB_COLOUR)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    # Add cog to bot
    bot.add_cog(General(bot))
