import os
import secrets

import discord

from datetime import datetime, timedelta
from ..utils import utils, errors, database
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages


class Moderation(commands.Cog):
    """Moderation commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    timeout = SlashCommandGroup(
        "timeout",
        "Discord time out settings",
    )

    warn = SlashCommandGroup("warn", "Warn settings")

    @commands.guild_only()
    @commands.slash_command()
    async def kick(self, ctx, member: discord.Member, reason="No reason provided."):
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
        raise commands.MissingPermissions(["kick_members"])

    @commands.guild_only()
    @commands.slash_command()
    async def ban(self, ctx, member: discord.Member, reason="No reason provided."):
        """Begone, thou scurvy dog"""
        if commands.has_permissions(ban_members=True):
            await member.ban(reason=reason)

            embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)
        raise commands.MissingPermissions(["ban_members"])

    @commands.guild_only()
    @commands.slash_command()
    async def unban(self, ctx, member: str):
        """Be back, thou scurvy dog"""
        if commands.has_permissions(ban_members=True):
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
                    break
        raise commands.MissingPermissions(["ban_members"])

    @commands.guild_only()
    @commands.slash_command()
    async def softban(self, ctx, member: discord.Member, reason="No reason provided."):
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
        raise commands.MissingPermissions(["kick_members", "manage_messages"])

    @commands.guild_only()
    @commands.slash_command()
    async def clear(self, ctx, amount: int):
        """Roomba mode activated"""
        if commands.has_permissions(manage_messages=True):
            deleted = await ctx.channel.purge(limit=amount)

            embed = discord.Embed(
                title=f"{len(deleted) - 1} messages have been deleted.",
                colour=self.emb_colour,
            )

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)
        raise commands.MissingPermissions(["manage_messages"])

    @commands.guild_only()
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
        raise commands.MissingPermissions(["manage_messages"])

    @commands.guild_only()
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
        raise commands.MissingPermissions(["manage_channels"])

    @commands.guild_only()
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
        raise commands.MissingPermissions(["manage_channels"])

    @commands.guild_only()
    @timeout.command(name="add")
    async def timeout_add(
        self,
        ctx,
        member: discord.Member,
        duration: int,
        unit: discord.Option(
            str,
            "unit",
            choices=["Seconds", "Minutes", "Hours", "Days", "Weeks"],
            required=True,
        ),
        reason: str = "No reason provided.",
    ):
        """Be quiet, peasant"""
        if commands.has_permissions(moderate_members=True):
            if not member.timed_out:
                time_delta = await utils.convert_time_into_timedelta(
                    time=duration, unit=unit
                )
                await member.timeout_for(duration=time_delta, reason=reason)

                embed = discord.Embed(
                    title=f"Timed out {member}",
                    colour=self.emb_colour,
                )

                embed.add_field(
                    name="Duration", value=f"{duration} {unit.lower()}", inline=False
                )

                embed.add_field(name="Reason", value=reason, inline=False)

                embed.add_field(name="Moderator", value=ctx.author, inline=False)

                embed.set_footer(
                    text="Wavy • https://wavybot.com",
                    icon_url=self.bot.user.display_avatar.url,
                )

                await ctx.respond(embed=embed)

                return
            raise errors.Timeout(
                "That member is already timed out. Use `/timeout remove` to remove the timeout."
            )
        raise commands.MissingPermissions(["moderate_members"])

    @commands.guild_only()
    @timeout.command(name="remove")
    async def timeout_remove(
        self,
        ctx,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        """Talk to me, peasant"""
        if commands.has_permissions(moderate_members=True):
            if member.timed_out:
                await member.remove_timeout(reason=reason)

                embed = discord.Embed(
                    title=f"Removed timeout from {member}",
                    colour=self.emb_colour,
                )

                embed.add_field(name="Reason", value=reason, inline=False)

                embed.add_field(name="Moderator", value=ctx.author, inline=False)

                embed.set_footer(
                    text="Wavy • https://wavybot.com",
                    icon_url=self.bot.user.display_avatar.url,
                )

                await ctx.respond(embed=embed)

                return
            raise errors.Timeout(
                "That member is not timed out. Use `/timeout add` to add a timeout."
            )
        raise commands.MissingPermissions(["moderate_members"])

    @commands.guild_only()
    @warn.command(name="add")
    async def warn_add(
        self,
        ctx,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        """Warning: be warned"""
        if commands.has_permissions(kick_members=True):
            if member.bot:
                raise errors.Bot("Bots cannot get warned.")

            warn_id = secrets.token_urlsafe(8)

            await self.db.set_warn(
                server_id=ctx.guild.id,
                member_id=member.id,
                warn_id=warn_id,
                reason=reason,
            )

            embed = discord.Embed(title=f"Warned {member}", colour=self.emb_colour)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(name="Moderator", value=ctx.author, inline=False)

            embed.add_field(name="Warn ID", value=f"`{warn_id}`", inline=False)

            embed.set_footer(
                text="Wavy • https://wavybot.com",
                icon_url=self.bot.user.display_avatar.url,
            )

            await ctx.respond(embed=embed)
        raise commands.MissingPermissions(["kick_members"])

    @commands.guild_only()
    @warn.command(name="remove")
    async def warn_remove(self, ctx, warn_id: str):
        """Look mom, no warning"""
        if commands.has_permissions(kick_members=True):
            warn = await self.db.remove_warn(server_id=ctx.guild.id, warn_id=warn_id)
            if warn:
                embed = discord.Embed(
                    title=f"Removed warning `{warn_id}`", colour=self.emb_colour
                )

                embed.set_footer(
                    text="Wavy • https://wavybot.com",
                    icon_url=self.bot.user.display_avatar.url,
                )

                await ctx.respond(embed=embed)
            else:
                raise errors.WarnNotFound(warn_id=warn_id)
        raise commands.MissingPermissions(["kick_members"])

    @commands.guild_only()
    @warn.command(name="list")
    async def warn_list(self, ctx, member: discord.Member = None):
        """Timmy should start sweating when he sees this"""
        member = ctx.author if not member else member

        warns = await self.db.fetch_warns(member_id=member.id)

        embed = discord.Embed(
            title=f"Showing warns for {member}" if warns else f"{member} has no warns.",
            colour=self.emb_colour,
        )

        # TODO(Robert): Add pagination.

        for i in warns:
            embed.add_field(
                name=f"Warn ID `{i.id}`",
                value=f"**Reason**: {i.reason}",
                inline=False,
            )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Moderation(bot))
