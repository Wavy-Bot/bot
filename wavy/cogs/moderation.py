import os

import discord

from datetime import datetime, timedelta
from ..utils import utils, errors, database
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import default_permissions


class Moderation(commands.Cog):
    """Moderation commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    # NOTE(Robert): When Discord finally releases a proper permission system for slash commands I will use that
    #  instead of my ugly way of doing it.

    timeout = SlashCommandGroup(
        "timeout",
        "Discord time-out settings",
    )

    warn = SlashCommandGroup("warn", "Warn settings")

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason="No reason provided."):
        """Yeetus deletus

        Kicks the specified member from the server.

        Options:
            member: The user to kick.
            reason (optional): The reason for kicking the user.
        """
        await member.kick(reason=reason)

        embed = discord.Embed(title=f"Kicked {member}", colour=self.emb_colour)

        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Moderator", value=ctx.author, inline=False)

        embed.set_footer(
            text="Wavy • https://wavybot.com",
            icon_url=self.bot.user.display_avatar.url,
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason="No reason provided."):
        """Begone, thou scurvy dog

        GitHub Copilot decided to generate the text above for some reason.
        Bans the specified member from the server.

        Options:
            member: The user to ban.
            reason (optional): The reason for banning the user.
        """
        await member.ban(reason=reason)

        embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Moderator", value=ctx.author, inline=False)

        embed.set_footer(
            text="Wavy • https://wavybot.com",
            icon_url=self.bot.user.display_avatar.url,
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(ban_members=True)
    async def unban(self, ctx, member: str):
        """Be back, thou scurvy dog

        GitHub Copilot decided to generate the text above for some reason.
        Unbans the specified member from the server.

        Options:
            member: The user to unban. (In the following format: user#1234)
        """
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

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(kick_members=True, manage_messages=True)
    async def softban(
        self, ctx, member: discord.Member, days: int = 14, reason="No reason provided."
    ):
        """Yeets the specified member and deletes all their messages from the past x days.

        See text above, soft-bans the specified member from the server.

        Options:
            member: The user to soft-ban.
            days (optional): The number of days to delete messages from.
            reason (optional): The reason for soft-banning the user.
        """

        def check(m) -> bool:
            """Checks if the message author is the specified member."""
            return m.author == member

        days = datetime.utcnow() - timedelta(days=days)

        del_msg = await ctx.channel.purge(after=days, check=check)

        await member.kick(reason=reason)

        embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Messages removed", value=str(len(del_msg)), inline=False)

        embed.add_field(name="Moderator", value=ctx.author, inline=False)

        embed.set_footer(
            text="Wavy • https://wavybot.com",
            icon_url=self.bot.user.display_avatar.url,
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Roomba mode activated

        Clears the specified amount of messages from the current channel.

        Options:
            amount: The amount of messages to delete.
        """
        # Send message notifying the user that the messages are being deleted
        await ctx.respond(f"Clearing {amount} messages, please wait...", ephemeral=True)

        deleted = await ctx.channel.purge(limit=amount)

        embed = discord.Embed(
            title=f"{len(deleted)} messages have been deleted.",
            colour=self.emb_colour,
        )

        embed.set_footer(
            text="Wavy • https://wavybot.com",
            icon_url=self.bot.user.display_avatar.url,
        )

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(manage_messages=True)
    async def nuke(self, ctx):
        """Kaboom? Yes Rico, kaboom.

        Clears all of the messages from the current channel.
        """
        # Send message notifying the user that the messages are being deleted
        await ctx.respond("Nuking all messages, please wait...", ephemeral=True)

        await ctx.channel.purge()

        embed = discord.Embed(title="Nuked all messages.", colour=self.emb_colour)

        embed.set_image(
            url="https://media1.tenor.com/images/5b0fcef4b070f5316093ab591e3995a8/tenor.gif?itemid=17383346"
        )

        embed.set_footer(
            text="Wavy • https://wavybot.com",
            icon_url=self.bot.user.display_avatar.url,
        )

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Shut thou mouths

        Locks the specified channel.

        Options:
            channel (optional): The channel to lock.
        """
        channel = channel if channel else ctx.channel

        role = ctx.guild.default_role

        # Although your linter will probably say something along the lines of
        # 'PermissionOverwrite' object attribute 'send_messages' is read-only
        # (and the same for add_reactions), this works.
        perms = channel.overwrites_for(role)
        perms.send_messages = False
        perms.add_reactions = False

        await channel.set_permissions(role, overwrite=perms)

        embed = discord.Embed(title=f"Locked channel {channel}", colour=self.emb_colour)

        embed.add_field(name="Moderator", value=ctx.author, inline=False)

        embed.set_footer(
            text="Wavy • https://wavybot.com",
            icon_url=self.bot.user.display_avatar.url,
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    @default_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unshut thou mouths

        Unlocks the specified channel.

        Options:
            channel (optional): The channel to unlock.
        """
        channel = channel if channel else ctx.channel

        role = ctx.guild.default_role

        # Although your linter will probably say something along the lines of
        # 'PermissionOverwrite' object attribute 'send_messages' is read-only
        # (and the same for add_reactions), this works.
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

    @commands.guild_only()
    @timeout.command(name="add")
    @default_permissions(moderate_members=True)
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
        """Be quiet, peasant

        Times out a member for a specified duration. (This uses Discord's timeout feature!)

        Options:
            member: The member to time out.
            duration: The duration to time-out the member for.
            unit: The unit of time to time-out the member for.
            reason (optional): The reason for the time-out.
        """
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

    @commands.guild_only()
    @timeout.command(name="remove")
    @default_permissions(moderate_members=True)
    async def timeout_remove(
        self,
        ctx,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        """Talk to me, peasant

        Removes a time-out from a member. (This uses Discord's timeout feature!)

        Options:
            member: The member to remove the time-out from.
            reason (optional): The reason for the time-out removal.
        """
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

    @commands.guild_only()
    @warn.command(name="add")
    @default_permissions(kick_members=True)
    async def warn_add(
        self,
        ctx,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        """Warning: be warned

        Adds a warning to a member.

        Options:
            member: The member to add a warning to.
            reason (optional): The reason for the warning.
        """
        if member.bot:
            raise errors.Bot("Bots cannot get warned.")

        warn_id = await utils.gen_id()

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

    @commands.guild_only()
    @warn.command(name="remove")
    @default_permissions(kick_members=True)
    async def warn_remove(self, ctx, warn_id: str):
        """Look mom, no warning

        Removes a warning from a member.

        Options:
            warn_id: The ID of the warning to remove.
        """
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

    @commands.guild_only()
    @warn.command(name="list")
    async def warn_list(self, ctx, member: discord.Member = None):
        """Timmy should start sweating when he sees this

        Shows a list of warnings for a member.

        Options:
            member (optional): The member to show the warnings for.
        """
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
