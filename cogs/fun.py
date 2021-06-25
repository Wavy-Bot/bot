import os
import random

import discord

from core import utils
from core import request
from discord.ext import commands

EMB_COLOUR = int(os.getenv("COLOUR"), 16)
CATEGORY_LIST = ["hot", "new", "top", "rising"]


class Fun(commands.Cog):
    """Cog that contains all fun commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddit(self, ctx, subreddit: str, category: str = None):
        """Sends a random post from the specified subreddit."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Reddit",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        if not category or category and category.lower() not in CATEGORY_LIST:

            category = random.choice(CATEGORY_LIST)

        post = await request.reddit(subreddit, category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=EMB_COLOUR)

        embed.set_image(url=post.image_url)

        embed.set_footer(text=f"👍 {post.upvotes} | 💬 {post.comments} • Wavy")

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def meme(self, ctx, category: str = None):
        """Sends a random meme from r/memes."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Meme",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        if not category or category and category.lower() not in CATEGORY_LIST:
            category = random.choice(CATEGORY_LIST)

        post = await request.reddit("memes", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=EMB_COLOUR)

        embed.set_image(url=post.image_url)

        embed.set_footer(text=f"👍 {post.upvotes} | 💬 {post.comments} • Wavy")

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def dankmeme(self, ctx, category: str = None):
        """Sends a random dank meme from r/dankmemes."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Dank meme",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        if not category or category and category.lower() not in CATEGORY_LIST:
            category = random.choice(CATEGORY_LIST)

        post = await request.reddit("dankmemes", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=EMB_COLOUR)

        embed.set_image(url=post.image_url)

        embed.set_footer(text=f"👍 {post.upvotes} | 💬 {post.comments} • Wavy")

        await temp_msg.edit(embed=embed)

    @commands.command(
        aliases=['minecraftuuid', 'minecraft_uuid', 'mcuuid', 'mc_uuid'])
    async def uuid(self, ctx, username: str):
        """Fetches the UUID of a Minecraft user."""
        data = await request.minecraft_uuid(username)

        embed = discord.Embed(title=f"{data.name}'s UUID",
                              description=f"`{data.uuid}`",
                              colour=EMB_COLOUR)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        aliases=['minecrafthead', 'minecraft_head', 'mchead', 'mc_head'])
    async def head(self, ctx, username: str):
        """Fetches the head of a Minecraft user."""
        data = await request.crafatar(username, "head")

        embed = discord.Embed(title=f"{data.uuid_class.name}'s head",
                              colour=EMB_COLOUR)

        embed.set_image(url=data.url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        aliases=['minecraftskin', 'minecraft_skin', 'mcskin', 'mc_skin'])
    async def skin(self, ctx, username: str):
        """Fetches the skin of a Minecraft user."""
        data = await request.crafatar(username, "body")

        embed = discord.Embed(title=f"{data.uuid_class.name}'s head",
                              colour=EMB_COLOUR)

        embed.set_image(url=data.url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def ship(self, ctx, first, second):
        """Ships 2 things or users together."""
        bar = await utils.progress_bar()

        embed = discord.Embed(title="❤️ **MATCHMAKING** ❤️",
                              description=f"\n{first} - {second}",
                              colour=EMB_COLOUR)

        embed.add_field(name=f"{bar.percentage}%", value=bar.bar, inline=True)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['gayr8', 'gayrate'])
    async def howgay(self, ctx, member: discord.Member = None):
        """Gay detection machine."""
        member = ctx.author if not member else member

        bar = await utils.progress_bar()

        embed = discord.Embed(title="🏳️‍🌈 **gay detection machine** 🏳️‍🌈",
                              colour=EMB_COLOUR)

        embed.add_field(name=f"{member} is {bar.percentage}% gay",
                        value=bar.bar,
                        inline=True)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['penis', 'peepee'])
    async def pp(self, ctx, member: discord.Member = None):
        """Peepee size calculator™"""
        member = ctx.author if not member else member

        # NOTE(Robert): Please, for the love of god, do not
        #               do this this way. This is only
        #               temporary.

        pp = "8"
        size = (random.randint(0, 15))

        for i in range(size):

            pp += "="

        pp += "D"

        embed = discord.Embed(title="Peepee size calculator™",
                              colour=EMB_COLOUR)

        embed.add_field(name=f"{member.name}'s penis", value=pp, inline=True)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball', 'eight-ball', '8-ball'])
    async def eightball(self, ctx, *, question):
        """Woah, magic."""
        responses = [
            'It is certain', 'It is decidebly so.', 'Without a doubt',
            'Yes - definetely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', "Don't count on it.",
            'My reply is no.', 'My sources say no', 'Outlook not so good.',
            'Very doubtful.'
        ]

        embed = discord.Embed(title=question,
                              description=random.choice(responses),
                              colour=EMB_COLOUR)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
