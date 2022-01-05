import os
import secrets

import discord

from datetime import datetime, timedelta
from ..utils import utils, errors, database
from discord.commands import SlashCommandGroup
from discord.ext import commands


class Fun(commands.Cog):
    """Fun commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    @commands.guild_only()
    @commands.slash_command(guild_ids=[710436465938530307])
    async def snipe(self, ctx):
        """Snipe the last deleted message."""
        snipe = await self.db.get_snipe(
            server_id=ctx.guild.id, channel_id=ctx.channel.id
        )

        if snipe:
            embed = discord.Embed(
                title="Snipe",
                colour=self.emb_colour,
            )

            embed.add_field(
                name="Author",
                value=f"<@{snipe.member_id}> ({snipe.member_id})",
                inline=False,
            )
            embed.add_field(
                name="Message",
                value=f"```{snipe.content}```"
                if not snipe.content.startswith("`") and not snipe.content.endswith("`")
                else snipe.content,
                inline=False,
            )

            if snipe.attachments:
                embed.add_field(
                    name="Attachments",
                    value="\n".join(snipe.attachments),
                    inline=False,
                )
        else:
            embed = discord.Embed(
                title="Snipe",
                description="No deleted messages for this channel could be found.",
                colour=self.emb_colour,
            )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Fun(bot))
