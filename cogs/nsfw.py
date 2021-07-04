import os
import random

import discord

from core import request
from core import utils
from discord.ext import commands


class NSFW(commands.Cog):
    """Cog that contains all NSFW commands."""
    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.category_list = ["hot", "new", "top", "rising"]

    @commands.command()
    @commands.is_nsfw()
    async def hentai(self, ctx, category: str = None):
        """Sends a random image from r/hentai."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Hentai",
                                   description=loading_text,
                                   colour=self.emb_colour)

        temp_msg = await ctx.send(embed=temp_embed)

        if not category or category and category.lower(
        ) not in self.category_list:
            category = random.choice(self.category_list)

        post = await request.reddit("hentai", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=self.emb_colour)

        embed.set_image(url=post.image_url)

        embed.set_footer(text=f"👍 {post.upvotes} | 💬 {post.comments} • Wavy")

        await temp_msg.edit(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def porn(self, ctx, category: str = None):
        """Sends a random image from r/porn."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Porn",
                                   description=loading_text,
                                   colour=self.emb_colour)

        temp_msg = await ctx.send(embed=temp_embed)

        if not category or category and category.lower(
        ) not in self.category_list:
            category = random.choice(self.category_list)

        post = await request.reddit("porn", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=self.emb_colour)

        embed.set_image(url=post.image_url)

        embed.set_footer(text=f"👍 {post.upvotes} | 💬 {post.comments} • Wavy")

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["r34"])
    @commands.is_nsfw()
    async def rule34(self, ctx, query: str):
        """Searches rule34 and returns an image."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Rule 34",
                                   description=loading_text,
                                   colour=self.emb_colour)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.r34(query)

        embed = discord.Embed(title="Rule 34",
                              url=image.file_url,
                              colour=self.emb_colour)

        embed.set_image(url=image.file_url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(NSFW(bot))
