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

        size = random.randint(0, 20)

        pp = "8" + "=" * size + "D"

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

    @commands.command()
    async def cat(self, ctx):
        """Fetches a random image of a cat."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Cat",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("cat")

        embed = discord.Embed(title="Cat", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        """Fetches a random image of a dog."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Dog",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("dog")

        embed = discord.Embed(title="Dog", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=['sadcat', 'crying_cat', 'cryingcat'])
    async def sad_cat(self, ctx):
        """Fetches a random image of a sad cat."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Sad cat",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sad_cat()

        embed = discord.Embed(title="Sad cat", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=['quack'])
    async def duck(self, ctx):
        """Fetches a random image of a duck."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Duck",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.duck()

        embed = discord.Embed(title="Duck", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=['birb'])
    async def bird(self, ctx):
        """Fetches a random image of a bird."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Bird",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("bird")

        embed = discord.Embed(title="Bird", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=['rabbit'])
    async def bunny(self, ctx):
        """Fetches a random image of a bunny."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Bunny",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.bunny()

        embed = discord.Embed(title="Bunny", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def bear(self, ctx, category: str = None):
        """Sends a random bear from r/bears."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Bear",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        if not category or category and category.lower() not in CATEGORY_LIST:
            category = random.choice(CATEGORY_LIST)

        post = await request.reddit("bears", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=EMB_COLOUR)

        embed.set_image(url=post.image_url)

        embed.set_footer(text=f"👍 {post.upvotes} | 💬 {post.comments} • Wavy")

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        """Fetches a random image of a fox."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Fox",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("fox")

        embed = discord.Embed(title="Fox", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["shibe"])
    async def shiba(self, ctx):
        """Fetches a random image of a shiba."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Shiba",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.shiba()

        embed = discord.Embed(title="Shiba", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def sloth(self, ctx):
        """Fetches a random image of a sloth."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Sloth",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sloth()

        embed = discord.Embed(title="Sloth", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def panda(self, ctx):
        """Fetches a random image of a panda."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Panda",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("panda")

        embed = discord.Embed(title="Panda", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["redpanda"])
    async def red_panda(self, ctx):
        """Fetches a random image of a red panda."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Red panda",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("red_panda")

        embed = discord.Embed(title="Red panda", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def koala(self, ctx):
        """Fetches a random image of a koala."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Koala",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("koala")

        embed = discord.Embed(title="Koala", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def raccoon(self, ctx):
        """Fetches a random image of a raccoon."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Raccoon",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("raccoon")

        embed = discord.Embed(title="Raccoon", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def kangaroo(self, ctx):
        """Fetches a random image of a kangaroo."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Kangaroo",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("kangaroo")

        embed = discord.Embed(title="Kangaroo", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command()
    async def whale(self, ctx):
        """Fetches a random image of a whale."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Whale",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.sra_image("whale")

        embed = discord.Embed(title="Whale", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["zuckerberg"])
    async def lizard(self, ctx):
        """Fetches a random image of a lizard."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="Lizard",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.lizard()

        embed = discord.Embed(title="Lizard", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["httpcat"])
    async def http_cat(self, ctx, code: int):
        """Fetches an HTTP cat with the specified status code."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="HTTP Cat",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.http_cat(code)

        embed = discord.Embed(title="HTTP Cat", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["httpdog"])
    async def http_dog(self, ctx, code: int):
        """Fetches an HTTP dog with the specified status code."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="HTTP Dog",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.http_dog(code)

        embed = discord.Embed(title="HTTP Dog", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["httpduck"])
    async def http_duck(self, ctx, code: int):
        """Fetches an HTTP duck with the specified status code."""
        # Create a temp embed and send it whilst getting an image.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title="HTTP Duck",
                                   description=loading_text,
                                   colour=EMB_COLOUR)

        temp_msg = await ctx.send(embed=temp_embed)

        image = await request.http_duck(code)

        embed = discord.Embed(title="HTTP Duck", colour=EMB_COLOUR)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
