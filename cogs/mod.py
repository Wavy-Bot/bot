import os

import discord

from datetime import datetime, timedelta
from discord.ext import commands


class Moderation(commands.Cog):
    """Cog that contains all moderation commands."""
    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)

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


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Moderation(bot))
