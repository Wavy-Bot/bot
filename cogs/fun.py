import os
import random
import json

import discord

from core import utils
from core import request
from discord.ext import commands


class Fun(commands.Cog):
    """Cog that contains all fun commands."""
    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.category_list = ["hot", "new", "top", "rising"]
        self.interactions = json.load(open('interactions.json'))

    async def __temp_embed(self, ctx, title: str):
        loading_text = await utils.loading_text()

        temp_embed = discord.Embed(title=title,
                                   description=loading_text,
                                   colour=self.emb_colour)

        temp_msg = await ctx.send(embed=temp_embed)

        return temp_msg

    @commands.command()
    async def reddit(self, ctx, subreddit: str, category: str = None):
        """Sends a random post from the specified subreddit."""
        # Create a temp embed and send it whilst getting a post.
        # Edit the embed afterwards so only 1 message is needed,
        # and the user doesn't have to wait without getting a
        # response.

        temp_msg = await self.__temp_embed(ctx, "Reddit")

        if not category or category and category.lower(
        ) not in self.category_list:

            category = random.choice(self.category_list)

        post = await request.reddit(subreddit, category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Meme")

        if not category or category and category.lower(
        ) not in self.category_list:
            category = random.choice(self.category_list)

        post = await request.reddit("memes", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Dank meme")

        if not category or category and category.lower(
        ) not in self.category_list:
            category = random.choice(self.category_list)

        post = await request.reddit("dankmemes", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=self.emb_colour)

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
                              colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        aliases=['minecrafthead', 'minecraft_head', 'mchead', 'mc_head'])
    async def head(self, ctx, username: str):
        """Fetches the head of a Minecraft user."""
        data = await request.crafatar(username, "head")

        embed = discord.Embed(title=f"{data.uuid_class.name}'s head",
                              colour=self.emb_colour)

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
                              colour=self.emb_colour)

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
                              colour=self.emb_colour)

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
                              colour=self.emb_colour)

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

        embed = discord.Embed(title="pp size calculator™",
                              colour=self.emb_colour)

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
                              colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Cat")

        image = await request.sra_image("cat")

        embed = discord.Embed(title="Cat", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Dog")

        image = await request.sra_image("dog")

        embed = discord.Embed(title="Dog", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Sad cat")

        image = await request.sad_cat()

        embed = discord.Embed(title="Sad cat", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Duck")

        image = await request.duck()

        embed = discord.Embed(title="Duck", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Bird")

        image = await request.sra_image("bird")

        embed = discord.Embed(title="Bird", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Bunny")

        image = await request.bunny()

        embed = discord.Embed(title="Bunny", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Bear")

        if not category or category and category.lower(
        ) not in self.category_list:
            category = random.choice(self.category_list)

        post = await request.reddit("bears", category, ctx.message.channel)

        embed = discord.Embed(title=post.title,
                              url=post.link,
                              colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Fox")

        image = await request.sra_image("fox")

        embed = discord.Embed(title="Fox", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Shiba")

        image = await request.shiba()

        embed = discord.Embed(title="Shiba", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Sloth")

        image = await request.sloth()

        embed = discord.Embed(title="Sloth", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Panda")

        image = await request.sra_image("panda")

        embed = discord.Embed(title="Panda", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Red panda")

        image = await request.sra_image("red_panda")

        embed = discord.Embed(title="Red panda", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Koala")

        image = await request.sra_image("koala")

        embed = discord.Embed(title="Koala", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Raccoon")

        image = await request.sra_image("raccoon")

        embed = discord.Embed(title="Raccoon", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Kangaroo")

        image = await request.sra_image("kangaroo")

        embed = discord.Embed(title="Kangaroo", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Whale")

        image = await request.sra_image("whale")

        embed = discord.Embed(title="Whale", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "Lizard")

        image = await request.lizard()

        embed = discord.Embed(title="Lizard", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "HTTP cat")

        image = await request.http_cat(code)

        embed = discord.Embed(title="HTTP Cat", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "HTTP dog")

        image = await request.http_dog(code)

        embed = discord.Embed(title="HTTP Dog", colour=self.emb_colour)

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

        temp_msg = await self.__temp_embed(ctx, "HTTP duck")

        image = await request.http_duck(code)

        embed = discord.Embed(title="HTTP Duck", colour=self.emb_colour)

        embed.set_image(url=image)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await temp_msg.edit(embed=embed)

    @commands.command(aliases=["murder"])
    async def kill(self, ctx, member: discord.Member = None):
        """Kills the specified user."""
        member = ctx.author if not member else member

        responses = self.interactions["kill"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} kills {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def heal(self, ctx, member: discord.Member = None):
        """Heals the specified user."""
        member = ctx.author if not member else member

        responses = self.interactions["heal"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} heals {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        """Slaps the specified user."""
        member = ctx.author if not member else member

        responses = self.interactions["slap"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} slaps {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, member: discord.Member = None):
        """Punches the specified user."""
        member = ctx.author if not member else member

        responses = self.interactions["punch"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} punches {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        """Kisses the specified user."""
        member = ctx.author if not member else member

        responses = self.interactions["kiss"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} kisses {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def lick(self, ctx, member: discord.Member = None):
        """Licks the specified user. (oh and please do not question why this exists)"""
        member = ctx.author if not member else member

        responses = self.interactions["lick"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} licks {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def laugh(self, ctx, member: discord.Member = None):
        """Laughs at the specified user."""
        member = ctx.author if not member else member

        responses = self.interactions["laugh"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} laughs at {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def pocky(self, ctx, member: discord.Member = None):
        """Pocky challenge?"""
        member = ctx.author if not member else member

        responses = self.interactions["pocky"]

        embed = discord.Embed(
            title=
            f"{ctx.author.display_name} does the pocky challenge with {member.display_name}",
            colour=self.emb_colour)

        embed.set_image(url=f'{random.choice(responses)}')

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["cb"])
    async def cleverbot(self, ctx, *, text: str):
        """Talking robot human thing, woah"""
        await ctx.trigger_typing()

        res = await request.cleverbot(text, ctx.author.id)

        embed = discord.Embed(title="Cleverbot",
                              description=res,
                              colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
