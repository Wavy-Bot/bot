import os
import json

import discord

from core import database, utils
from datetime import datetime, timedelta
from discord.ext import commands


class Moderation(commands.Cog):
    """Cog that contains all moderation commands."""
    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    @commands.command(aliases=["yeet"])
    @commands.has_permissions(kick_members=True)
    async def kick(self,
                   ctx,
                   member: discord.Member = None,
                   *,
                   reason="No reason provided."):
        """Kicks the specified member."""
        await member.kick(reason=reason)

        embed = discord.Embed(title=f"Kicked {member}", colour=self.emb_colour)

        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Moderator",
                        value=ctx.message.author,
                        inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["begone"])
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  ctx,
                  member: discord.Member = None,
                  *,
                  reason="No reason provided."):
        """Bans the specified member."""
        await member.ban(reason=reason)

        embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Moderator",
                        value=ctx.message.author,
                        inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True, manage_messages=True)
    async def softban(self,
                      ctx,
                      member: discord.Member = None,
                      *,
                      reason="No reason provided."):
        """Kicks the specified member and deletes all their messages from the past 14 days."""
        def check(m):
            """Checks if the message author is the specified member."""
            return m.author == member

        days = datetime.utcnow() - timedelta(days=14)

        del_msg = ctx.channel.purge(after=days, check=check)

        await member.kick(reason=reason)

        embed = discord.Embed(title=f"Banned {member}", colour=self.emb_colour)

        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Messages removed",
                        value=str(len(del_msg)),
                        inline=False)

        embed.add_field(name="Moderator",
                        value=ctx.message.author,
                        inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        """Unbans the specified member."""
        # NOTE(Robert): I am aware that there are numerous other ways to do this,
        #               but this just seemed like the most user-friendly one.
        banned_members = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')

        for entry in banned_members:
            member = entry.user

            if (member.name, member.discriminator) == (member_name,
                                                       member_discriminator):
                await ctx.guild.unban(member)

                embed = discord.Embed(title=f"Unbanned {member}",
                                      colour=self.emb_colour)

                embed.add_field(name="Moderator",
                                value=ctx.message.author,
                                inline=False)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                await ctx.send(embed=embed)

                # Stop the loop

                return

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Clears the specified amount of messages."""
        # NOTE(Robert): You might be thinking: "why does he add 1 to the amount of messages?"
        #               Well, this is so it also deletes the author's "%clear"
        #               (or whatever prefix they might be using) message.
        deleted = await ctx.channel.purge(limit=amount + 1)

        embed = discord.Embed(
            title=f"{len(deleted) - 1} messages have been deleted.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["purgeall", "purge_all"])
    @commands.has_permissions(manage_messages=True)
    async def nuke(self, ctx):
        """Nukes all messages in a channel."""
        await ctx.channel.purge()

        embed = discord.Embed(title="Nuked all messages.",
                              colour=self.emb_colour)

        embed.set_image(
            url=
            "https://media1.tenor.com/images/5b0fcef4b070f5316093ab591e3995a8/tenor.gif?itemid=17383346"
        )

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self,
                   ctx,
                   member: discord.Member,
                   time=None,
                   *,
                   reason="No reason provided."):
        """Mutes the specified member."""
        fetch_mute = await self.db.fetch_mute(ctx.message.guild.id, member.id)

        if not fetch_mute:

            fetch_role = await self.db.fetch_role(ctx.message.guild.id, "mute")

            if fetch_role:
                role = discord.utils.get(ctx.guild.roles,
                                         id=fetch_role.role_id)

                if not role:

                    fetch_role = None

            if not fetch_role:
                embed = discord.Embed(
                    title="Mute",
                    description=
                    "Creating mute role since no mute role has been configured.",
                    colour=self.emb_colour)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                await ctx.send(embed=embed)

                role = await ctx.message.guild.create_role(
                    name="Muted", reason="No mute role was configured.")

                for channel in ctx.guild.text_channels:

                    perms = channel.overwrites_for(role)

                    perms.send_messages = False
                    perms.add_reactions = False

                    await channel.set_permissions(role, overwrite=perms)

                for channel in ctx.guild.voice_channels:
                    perms = channel.overwrites_for(role)

                    perms.speak = False

                    await channel.set_permissions(role, overwrite=perms)

                positions = {
                    role:
                    ctx.message.guild.get_member(
                        self.bot.user.id).top_role.position - 1
                }

                await ctx.message.guild.edit_role_positions(positions=positions
                                                            )

                await self.db.set_role(ctx.message.guild.id, role.id, "mute")

            else:
                role = discord.utils.get(ctx.guild.roles,
                                         id=fetch_role.role_id)

            await member.add_roles(role)

            embed = discord.Embed(title=f"Muted {member}",
                                  colour=self.emb_colour)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(name="Moderator",
                            value=ctx.message.author,
                            inline=False)

            if time:
                old_time = time

                converted_time = await utils.convert_time(time)

                time = converted_time

                if time:
                    if not time.time < 10:
                        embed.add_field(name="Time",
                                        value=old_time,
                                        inline=False)
                        time = time.timedelta
                    elif time.time == 0:
                        time = None
                    else:
                        embed = discord.Embed(
                            title=f"Could not mute {member}",
                            description=
                            "Time cannot be shorter than 10 seconds.",
                            colour=self.emb_colour)

                        embed.set_footer(text="Wavy • https://wavybot.com",
                                         icon_url=self.bot.user.avatar_url)

                        await ctx.send(embed=embed)

                        return

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await self.db.set_mute(ctx.message.guild.id, member.id, time)

        else:
            embed = discord.Embed(title=f"Could not mute {member}",
                                  description="Member has already been muted.",
                                  colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['removemute'])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes the specified member."""
        fetch_mute = await self.db.fetch_mute(ctx.message.guild.id, member.id)

        if fetch_mute:

            fetch_role = await self.db.fetch_role(ctx.message.guild.id, "mute")

            if fetch_role:
                role = discord.utils.get(ctx.guild.roles,
                                         id=fetch_role.role_id)

                if role:

                    await member.remove_roles(role)

            await self.db.remove_mute(ctx.guild.id, member.id)

            embed = discord.Embed(title=f"Unmuted {member}",
                                  colour=self.emb_colour)

            embed.add_field(name="Moderator",
                            value=ctx.message.author,
                            inline=False)

        else:
            embed = discord.Embed(title=f"{member} has not been muted",
                                  colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Locks the specified channel."""
        channel = channel if channel else ctx.message.channel

        role = ctx.message.guild.default_role

        perms = channel.overwrites_for(role)

        perms.send_messages = False
        perms.add_reactions = False

        await channel.set_permissions(role, overwrite=perms)

        embed = discord.Embed(title=f"Locked channel {channel}",
                              colour=self.emb_colour)

        embed.add_field(name="Moderator",
                        value=ctx.message.author,
                        inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlocks the specified channel."""
        channel = channel if channel else ctx.message.channel

        role = ctx.message.guild.default_role

        perms = channel.overwrites_for(role)

        perms.send_messages = None
        perms.add_reactions = None

        await channel.set_permissions(role, overwrite=perms)

        embed = discord.Embed(title=f"Unlocked channel {channel}",
                              colour=self.emb_colour)

        embed.add_field(name="Moderator",
                        value=ctx.message.author,
                        inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx):
        """Gets the last deleted message."""
        with open("snipe.json", "r") as json_file:
            snipe_file = json.load(json_file)

        json_file.close()

        if str(ctx.message.guild.id) in snipe_file and str(
                ctx.message.channel.id) in snipe_file[str(
                    ctx.message.guild.id)]:
            embed = discord.Embed(title="Snipe",
                                  description=snipe_file[str(
                                      ctx.message.guild.id)][str(
                                          ctx.message.channel.id)]['content'],
                                  colour=self.emb_colour)

            if snipe_file[str(ctx.message.guild.id)][str(
                    ctx.message.channel.id)]['attachments']:
                embed.add_field(
                    name="Attachments",
                    value=str(snipe_file[str(ctx.message.guild.id)][str(
                        ctx.message.channel.id)]['attachments']),
                    inline=False)
        else:
            embed = discord.Embed(
                title="Snipe",
                description=
                "No deleted messages for this channel have been found.",
                colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Moderation(bot))
