import os

import discord

from datetime import timedelta
from core import utils, database
from discord.ext import commands


class Utility(commands.Cog):
    """Cog that contains all utility commands."""
    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    async def __giveaway_cancel_message(self, reason: str):
        embed = discord.Embed(
            title="Giveaway",
            description=f"Giveaway creation cancelled. Reason: {reason}",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        return embed

    @commands.group(aliases=['g'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx):
        """Giveaway group."""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
                title="Giveaway",
                description=
                "No valid subcommand provided. Please use one of the following subcommands:"
                "\n`create`, `end`, `list`",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=embed)

    @giveaway.command(aliases=['c'])
    @commands.has_permissions(manage_guild=True)
    async def create(self, ctx):
        """Creates a giveaway."""
        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        embed = discord.Embed(
            title="Giveaway",
            description=":tada: Alright! Let's set up your giveaway!\n"
            "\nFirst, what channel do you want the giveaway in?"
            "\n(for example `#giveaways`) or use its ID (for example `731143785769074780`)."
            "Also, please make sure that the bot has send message permissions in the desired channel."
            "\nYou can type `cancel` at any time to cancel creation.\n\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        message = await ctx.send(embed=embed)

        chann_input = await self.bot.wait_for('message',
                                              timeout=30,
                                              check=check)

        if chann_input.content == "CANCEL".lower():
            embed = await self.__giveaway_cancel_message(
                "User cancelled giveaway creation.")

            await message.edit(embed=embed)

            return

        channel = int(
            chann_input.content.replace('<', '').replace('>',
                                                         '').replace('#', ''))

        channel = self.bot.get_channel(channel)

        if not channel:
            embed = await self.__giveaway_cancel_message(
                "User provided invalid channel.")

            await message.edit(embed=embed)

            return

        await chann_input.delete()

        embed = discord.Embed(
            title="Giveaway",
            description=
            f"Alright! the giveaway will be in {channel.mention}.\nNext, how long should the giveaway last?"
            f"\n\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

        time_input = await self.bot.wait_for('message',
                                             timeout=30,
                                             check=check)

        if time_input.content == "CANCEL".lower():
            embed = await self.__giveaway_cancel_message(
                "User cancelled giveaway creation.")

            await message.edit(embed=embed)

            return

        time = await utils.convert_time_into_epoch(time_input.content)

        if not time:
            embed = await self.__giveaway_cancel_message(
                "Invalid time format. Please use one of the following time formats:"
                "\n`seconds`, `minutes`, 'hours', 'days', `weeks`")

            await message.edit(embed=embed)

            return

        if time.time < 10:
            embed = await self.__giveaway_cancel_message(
                "Invalid time specified. Minimum amount of time that a giveaway can last is 10 seconds."
            )

            await message.edit(embed=embed)

            return

        await time_input.delete()

        embed = discord.Embed(
            title="Giveaway",
            description=
            f"Okay! The giveaway will last {time.time} seconds.\nNow, how many winners should there be?"
            f"\n\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

        winners_input = await self.bot.wait_for('message',
                                                timeout=30,
                                                check=check)

        if winners_input.content == "CANCEL".lower():
            embed = await self.__giveaway_cancel_message(
                "User cancelled giveaway creation.")

            await message.edit(embed=embed)

            return

        winners = int(winners_input.content)

        if winners < 1:
            embed = await self.__giveaway_cancel_message(
                "Invalid amount of winners specified.")

            await message.edit(embed=embed)

            return

        await winners_input.delete()

        embed = discord.Embed(
            title="Giveaway",
            description=f"Gotcha! The giveaway will have {winners} winners."
            f"\nNow, onto the last part. What do you want to give away?"
            f"\n\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

        item_input = await self.bot.wait_for('message',
                                             timeout=30,
                                             check=check)

        if item_input.content == "CANCEL".lower():
            embed = await self.__giveaway_cancel_message(
                "User cancelled giveaway creation.")

            await message.edit(embed=embed)

            return

        if len(item_input.content) > 2000:
            embed = await self.__giveaway_cancel_message(
                "Item name provided is too long.")

            await message.edit(embed=embed)

            return

        await item_input.delete()

        embed = discord.Embed(
            title="Giveaway",
            description=
            f"Very well. Here is a rundown of the information you provided",
            colour=self.emb_colour)

        embed.add_field(name="Channel", value=channel.mention)

        embed.add_field(name="Time", value=f"{time.time} seconds")

        embed.add_field(name="Winners", value=f"{winners}")

        embed.add_field(name="Item", value=item_input.content)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

        g_embed = discord.Embed(
            title="🎉 **GIVEAWAY** 🎉",
            description=
            f"{ctx.author.mention} hosted a giveaway for `{item_input.content}`!\n\nReact with 🎉 to enter the giveaway!"
            f"\n\nGiveaway end: <t:{time.epoch}:F> | <t:{time.epoch}:R>",
            colour=self.emb_colour)

        g_embed.set_footer(text=f"{winners} Winner(s) • Wavy",
                           icon_url=ctx.author.avatar_url)

        g_message = await channel.send(embed=g_embed)

        await g_message.add_reaction('🎉')

        await self.db.set_giveaway(ctx.message.guild.id, channel.id,
                                   g_message.id, winners, time.timedelta)

    @giveaway.command(aliases=['e', 'delete', 'remove'])
    @commands.has_permissions(manage_guild=True)
    async def end(self, ctx, message_id: int):
        """Ends a giveaway."""
        giveaway = await self.db.fetch_giveaway(ctx.message.guild.id,
                                                message_id)

        if giveaway:
            channel = self.bot.get_channel(giveaway.channel_id)

            if channel:
                try:
                    message = await channel.fetch_message(giveaway.message_id)
                except discord.errors.NotFound:
                    await self.db.remove_giveaway(giveaway.server_id,
                                                  giveaway.message_id)
                    return

                winners = []

                for reaction in message.reactions:
                    async for user in reaction.users():
                        if not user.bot and len(winners) <= giveaway.winners:
                            winners.append(user)

                if not winners:
                    await channel.send("no-one entered the giveaway.")

                    await self.db.remove_giveaway(giveaway.server_id,
                                                  giveaway.message_id)

                    return

                for winner in winners:
                    await channel.send(
                        f"{winner.mention} has won the giveaway!")

                embed = discord.Embed(
                    title="Giveaway",
                    description=
                    f"Ended the giveaway with message ID `{message_id}`.",
                    colour=self.emb_colour)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                await ctx.send(embed=embed)

        await self.db.remove_giveaway(ctx.message.guild.id, message_id)

    @giveaway.command(aliases=['l', 'show', 's'])
    async def list(self, ctx):
        """Lists all active giveaways in this guild."""
        giveaways = await self.db.fetch_giveaways_in_guild(ctx.message.guild.id
                                                           )

        embed = discord.Embed(title="Showing giveaways" if giveaways else
                              "No active giveaways could be found.",
                              colour=self.emb_colour)

        # TODO(Robert): Add pagination.

        for i in giveaways:
            epoch = int(i.end_time.timestamp())

            embed.add_field(
                name=f"Giveaway ID `{i.message_id}`",
                value=f"Giveaway end: <t:{epoch}:F> | <t:{epoch}:R>",
                inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Utility(bot))
