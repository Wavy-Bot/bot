import os
import random

import discord

from ..utils import database, utils
from discord.ext import commands


class Fun(commands.Cog):
    """Fun commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    @commands.guild_only()
    @commands.slash_command()
    async def meme(self, ctx):
        """Funny meme, monke approves

        Sends a random meme from r/memes, r/meme, r/dankmemes or r/memes_of_the_dank.
        """
        meme = await self.db.fetch_meme()

        if meme.over_18:
            raise commands.NSFWChannelRequired(channel=ctx.channel)

        embed = discord.Embed(title=meme.title, url=meme.url, colour=self.emb_colour)

        embed.set_image(url=meme.image)

        embed.set_footer(text=f"👍 {meme.ups} | 💬 {meme.comments} • Wavy")

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def ship(self, ctx, first: str, second: str):
        """😳

        Ships 2 users or things together.

        Options:
            first: The first thing to ship.
            second: The second thing to ship.
        """
        percentage = random.randint(0, 100)
        bar = await utils.progress_bar(percentage=percentage)

        embed = discord.Embed(
            title="❤️ **MATCHMAKING** ❤️",
            description=f"\n{first} - {second}",
            colour=self.emb_colour,
        )

        embed.add_field(name=f"{percentage}%", value=bar, inline=True)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def howgay(self, ctx, member: discord.Member = None):
        """🏳‍🌈 gay detection machine 🏳‍🌈

        Detects how gay someone is. TAKE THIS WITH A GRAIN OF SALT,
        THIS IS OBVIOUSLY A JOKE AND I DO NOT WANT TO HURT ANYONE WITH THIS.

        Options:
            member (optional): The member to detect the gay of.
        """
        member = ctx.author if not member else member

        percentage = random.randint(0, 100)
        bar = await utils.progress_bar(percentage=percentage)

        embed = discord.Embed(
            title="🏳️‍🌈 **gay detection machine** 🏳️‍🌈", colour=self.emb_colour
        )

        embed.add_field(name=f"{member} is {percentage}% gay", value=bar, inline=True)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def pp(self, ctx, member: discord.Member = None):
        """pp size calculator™

        Calculates the size of someone's fellow uhm... member.

        Options:
            member: The member to calculate the pp size of.
        """
        member = ctx.author if not member else member

        size = random.randint(0, 20)

        # This is ugly, I know.
        pp = "8" + "=" * size + "D"

        embed = discord.Embed(title="pp size calculator™", colour=self.emb_colour)

        embed.add_field(name=f"{member.name}'s pp size", value=pp, inline=True)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="8ball")
    async def eightball(self, ctx, *, question: str):
        """Woah, magic.

        Ask a yes/no question and I'll answer it.

        Options:
            question: The question to ask.
        """
        responses = await utils.message(message_type="eightball")

        embed = discord.Embed(
            title=question, description=responses, colour=self.emb_colour
        )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
