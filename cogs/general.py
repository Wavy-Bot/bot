import os

import discord

from discord.ext import commands

EMB_COLOUR = int(os.getenv("COLOUR"), 16)


class General(commands.Cog):
    """Cog that contains all general commands."""
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

    @commands.command(aliases=['stats'])
    async def botinfo(self, ctx):
        """Sends info about the bot."""
        embed = discord.Embed(title="Wavy", colour=EMB_COLOUR)

        embed.add_field(name='General Stats',
                        value=f'• Guilds: {len(self.bot.guilds)}\n'
                        f'• Users: {len(list(self.bot.get_all_members()))} \n'
                        f'• Shards: {self.bot.shard_count}\n'
                        f'• Cogs: {len(self.bot.cogs)}\n'
                        f'• Commands: {len(self.bot.commands)}\n'
                        f'• Emojis: {len(self.bot.emojis)}\n'
                        f'• Voice Instances: {len(self.bot.voice_clients)}',
                        inline=True)

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        # Send embed

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(General(bot))
