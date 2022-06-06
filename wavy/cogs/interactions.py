import os

import discord

from ..utils import database, utils
from discord.ext import commands


class Interactions(commands.Cog):
    """Interaction commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)

    @commands.guild_only()
    @commands.slash_command(name="slap")
    async def slash_slap(self, ctx, member: discord.Member = None):
        """b-baka

        "I HATE YOU!" *runs away*

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

        Kisses someone. Now in 2D!

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

    @commands.guild_only()
    @commands.slash_command()
    async def massage(self, ctx, member: discord.Member = None):
        """That feels kinda nic- okay that straight up hurts

        Who doesn't like a good massage amirite?

        Options:
            member (optional): The member to massage.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="massage")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} massages {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def shoot(self, ctx, member: discord.Member = None):
        """Headshot

        Right in the face. Nice.

        Options:
            member (optional): The member to shoot.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="shoot")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} shoots {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def stare(self, ctx, member: discord.Member = None):
        """👁👄👁

        What is that guy looking at?

        Options:
            member (optional): The member to stare at.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="stare")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} stares at {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def bite(self, ctx, member: discord.Member = None):
        """Chomp

        Yummy.

        Options:
            member (optional): The member to stare at.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="bite")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} bites {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def hug(self, ctx, member: discord.Member = None):
        """wuv u

        You're so cute.

        Options:
            member (optional): The member to hug.
        """
        member = ctx.author if not member else member

        image = await utils.interaction(interaction_type="hug")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} hugs {member.display_name}",
            colour=self.emb_colour,
        )

        embed.set_image(url=image)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Interactions(bot))
