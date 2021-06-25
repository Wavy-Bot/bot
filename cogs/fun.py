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

    @commands.command()
    async def uuid(self, ctx, username: str):
        """Fetches the UUID of a Minecraft user."""
        data = await request.minecraft_uuid(username)

        embed = discord.Embed(title=f"{data.name}'s UUID",
                              description=f"`{data.uuid}`",
                              colour=EMB_COLOUR)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def head(self, ctx, username: str):
        """Fetches the head of a Minecraft user."""
        data = await request.crafatar(username, "head")

        embed = discord.Embed(title=f"{data.uuid_class.name}'s head",
                              colour=EMB_COLOUR)

        embed.set_image(url=data.url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def skin(self, ctx, username: str):
        """Fetches the skin of a Minecraft user."""
        data = await request.crafatar(username, "body")

        embed = discord.Embed(title=f"{data.uuid_class.name}'s head",
                              colour=EMB_COLOUR)

        embed.set_image(url=data.url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
