import os
import random

import discord

from ..utils import database, classes, utils
from discord.ext import commands


class Fun(commands.Cog):
    """Fun commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    @commands.guild_only()
    @commands.slash_command()
    async def snipe(self, ctx):
        """Headshot"""
        snipe = await self.db.fetch_snipe(
            server_id=ctx.guild.id, channel_id=ctx.channel.id
        )

        if snipe:
            embed = discord.Embed(
                title="Snipe",
                colour=self.emb_colour,
            )

            embed.add_field(
                name="Author",
                value=f"<@{snipe.member_id}> ({snipe.member_id})",
                inline=False,
            )
            embed.add_field(
                name="Message",
                value=f"```{snipe.content}```"
                if not snipe.content.startswith("`") and not snipe.content.endswith("`")
                else snipe.content,
                inline=False,
            )

            if snipe.attachments:
                embed.add_field(
                    name="Attachments",
                    value="\n".join(snipe.attachments),
                    inline=False,
                )
        else:
            embed = discord.Embed(
                title="Snipe",
                description="No deleted messages for this channel could be found.",
                colour=self.emb_colour,
            )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def meme(self, ctx):
        """Funny meme, monke approves"""
        post = await self.db.fetch_meme()

        meme = classes.RedditPost(
            subreddit=post["subreddit"],
            title=post["title"],
            over_18=post["over_18"],
            url=post["url"],
            image=post["image"],
            ups=post["ups"],
            comments=post["comments"],
        )

        if meme.over_18:
            raise commands.NSFWChannelRequired(channel=ctx.channel)

        embed = discord.Embed(title=meme.title, url=meme.url, colour=self.emb_colour)

        embed.set_image(url=meme.image)

        embed.set_footer(text=f"👍 {meme.ups} | 💬 {meme.comments} • Wavy")

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def ship(self, ctx, first: str, second: str):
        """😳"""
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
        """🏳‍🌈 gay detection machine 🏳‍🌈"""
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
        """pp size calculator™"""
        member = ctx.author if not member else member

        size = random.randint(0, 20)

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
        """Woah, magic."""
        responses = [
            "It is certain",
            "It is decidebly so.",
            "Without a doubt",
            "Yes - definetely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no",
            "Outlook not so good.",
            "Very doubtful.",
        ]

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
    @commands.user_command(name="Slap")
    async def user_slap(self, ctx, member: discord.Member = None):
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
    async def slash_kiss(self, ctx, member: discord.Member = None):
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
    @commands.user_command(name="Kiss")
    async def user_kiss(self, ctx, member: discord.Member = None):
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
    @commands.user_command(name="Lick")
    async def user_lick(self, ctx, member: discord.Member = None):
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
