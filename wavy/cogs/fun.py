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
            title=question, description=random.choice(responses), colour=self.emb_colour
        )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="slap")
    async def slash_slap(self, ctx, member: discord.Member = None):
        """b-baka

        Slaps someone.

        Options:
            member (optional): The member to slap.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="slap")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} slaps {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.user_command(name="Slap")
    async def user_slap(self, ctx, member: discord.Member):
        """b-baka"""
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="slap")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} slaps {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="kiss")
    async def slash_kiss(self, ctx, member: discord.Member):
        """🤪

        Kisses someone.

        Options:
            member (optional): The member to kiss.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="kiss")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} kisses {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.user_command(name="Kiss")
    async def user_kiss(self, ctx, member: discord.Member):
        """🤪"""
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="kiss")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} kisses {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="lick")
    async def slash_lick(self, ctx, member: discord.Member = None):
        """woah woah woah, you actually gonna do this?

        Licks someone. You guys have weird fetishes smh my head.

        Options:
            member (optional): The member to lick.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="lick")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} licks {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.user_command(name="Lick")
    async def user_lick(self, ctx, member: discord.Member):
        """woah woah woah, you actually gonna do this?"""
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="lick")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} licks {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="laugh")
    async def slash_laugh(self, ctx, member: discord.Member = None):
        """funniest laugh ever

        Laughs at someone. Yeah, I also don't know why I added this.

        Options:
            member (optional): The member to laugh at.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="laugh")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} laughs at {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.user_command(name="Laugh at")
    async def user_laugh(self, ctx, member: discord.Member = None):
        """funniest laugh ever"""
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="laugh")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} laughs at {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="pocky")
    async def slash_pocky(self, ctx, member: discord.Member = None):
        """kewl pockers

        Does the pocky challenge with someone. Such wow.

        Options:
            member (optional): The member to do the pocky challenge with.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="pocky")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} does the pocky challenge with {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.user_command(name="Pocky challenge")
    async def user_pocky(self, ctx, member: discord.Member = None):
        """kewl pockers"""
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="pocky")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} does the pocky challenge with {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
