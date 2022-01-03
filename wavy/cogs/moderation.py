import os

import discord

from datetime import datetime, timedelta
from discord.ext import commands


class Moderation(commands.Cog):
    """Moderation commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)

    # TODO(Robert): Discord does not have a proper permission system for slash commands yet,
    #  so I cannot make moderation commands yet.

    @commands.slash_command()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided."):
        """Yeetus deletus"""
        if commands.has_permissions(kick_members=True):
            await member.kick(reason=reason)

            embed = discord.Embed(title=f"Kicked {member}", colour=self.emb_colour)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)

    @commands.slash_command()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided."):
        """Begone, thou scurvy dog"""
        if commands.has_permissions(kick_members=True):
            await member.ban(reason=reason)

            embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)

    @commands.slash_command()
    async def unban(self, ctx, member: str) -> None:
        """Be back, thou scurvy dog"""
        if commands.has_permissions(kick_members=True):
            # NOTE(Robert): I am aware that there are numerous other ways to do this,
            #               but this just seemed like the most user-friendly one.
            banned_members = await ctx.guild.bans()

            member_name, member_discriminator = member.split("#")

            for entry in banned_members:
                member = entry.user

                if (member.name, member.discriminator) == (
                    member_name,
                    member_discriminator,
                ):
                    await ctx.guild.unban(member)

                    embed = discord.Embed(
                        title=f"Unbanned {member}", colour=self.emb_colour
                    )

                    embed.add_field(name="Moderator", value=ctx.author, inline=False)

                    embed.set_footer(
                        text="Wavy • https://wavybot.com",
                        icon_url=self.bot.user.display_avatar.url,
                    )

                    await ctx.respond(embed=embed)

                    # Stop the loop

                    return

    @commands.slash_command()
    async def softban(
        self, ctx, member: discord.Member, *, reason="No reason provided."
    ):
        """Yeets the specified member and deletes all their messages from the past 14 days."""

        def check(m) -> bool:
            """Checks if the message author is the specified member."""
            return m.author == member

        if commands.has_permissions(kick_members=True, manage_messages=True):

            days = datetime.utcnow() - timedelta(days=14)

            del_msg = await ctx.channel.purge(after=days, check=check)

            await member.kick(reason=reason)

            embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(
                name="Messages removed", value=str(len(del_msg)), inline=False
            )

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)

    @commands.slash_command()
    async def clear(self, ctx, amount: int):
        """Roomba mode activated"""
        if commands.has_permissions(manage_messages=True):
            # NOTE(Robert): You might be thinking: "why does he add 1 to the amount of messages?"
            #               Well, this is so it also deletes the author's "/clear" message.
            deleted = await ctx.channel.purge(limit=amount + 1)

            embed = discord.Embed(
                title=f"{len(deleted) - 1} messages have been deleted.",
                colour=self.emb_colour,
            )

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            message = await ctx.respond(embed=embed)

    @commands.slash_command()
    async def nuke(self, ctx):
        """Kaboom? Yes Rico, kaboom."""
        if commands.has_permissions(manage_messages=True):
            await ctx.channel.purge()

            embed = discord.Embed(title="Nuked all messages.", colour=self.emb_colour)

            embed.set_image(
                url="https://media1.tenor.com/images/5b0fcef4b070f5316093ab591e3995a8/tenor.gif?itemid=17383346"
            )

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)

    @commands.slash_command()
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Shut thou mouths"""
        if commands.has_permissions(manage_channels=True):
            channel = channel if channel else ctx.channel

            role = ctx.guild.default_role

            perms = channel.overwrites_for(role)

            perms.send_messages = False
            perms.add_reactions = False

            await channel.set_permissions(role, overwrite=perms)

            embed = discord.Embed(
                title=f"Locked channel {channel}", colour=self.emb_colour
            )

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)

    @commands.slash_command()
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unshut thou mouths"""
        if commands.has_permissions(manage_channels=True):
            channel = channel if channel else ctx.channel

            role = ctx.guild.default_role

            perms = channel.overwrites_for(role)

            perms.send_messages = None
            perms.add_reactions = None

            await channel.set_permissions(role, overwrite=perms)

            embed = discord.Embed(
                title=f"Unlocked channel {channel}", colour=self.emb_colour
            )

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)

    # TODO(Robert): Add warn commands.


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Moderation(bot))
