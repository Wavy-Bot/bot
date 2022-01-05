import os
import time

import discord

import wavy
from ..utils import utils, errors
from discord.ext import commands
from discord.errors import InvalidArgument


class General(commands.Cog):
    """General commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)

    @commands.guild_only()
    @commands.slash_command()
    async def ping(self, ctx):
        """Ping pong"""
        embed = discord.Embed(
            title="Pong :ping_pong:",
            description=f"Heartbeat: {round(self.bot.latency * 1000)}ms",
            colour=self.emb_colour,
        )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def help(
        self,
        ctx,
        category: discord.Option(
            str,
            "category",
            choices=["General", "Moderation", "Music"],
            required=False,
        ),
    ):
        """Send help"""
        # if category:
        #     category = category.capitalize()

        categories = list(self.bot.cogs)

        if category:
            if category in categories:
                cog = self.bot.get_cog(category)

                embed = discord.Embed(
                    title=f"Help for category: {cog.qualified_name}",
                    colour=self.emb_colour,
                )

                for command in cog.get_commands():
                    embed.add_field(
                        name=command.name,
                        value=f"`{command.description}`",
                    )

                embed.set_footer(
                    text="Wavy • https://wavybot.com",
                    icon_url=self.bot.user.display_avatar.url,
                )

            else:
                raise errors.NonExistantCategory(category)

        else:
            embed = discord.Embed(title="Help Menu: Categories", colour=self.emb_colour)

            for item in categories:
                cog = self.bot.get_cog(item)
                cog_commands = cog.get_commands()

                human_commands = ", ".join(
                    [f"`{command.name}`" for command in cog_commands]
                )

                if human_commands:
                    embed.add_field(name=item, value=human_commands, inline=False)

                embed.set_footer(
                    text=f"To get more in-depth help you can run /help <category> • Wavy",
                    icon_url=self.bot.user.display_avatar.url,
                )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def stats(self, ctx):
        """The boring stuff"""
        server_stats = await utils.server_stats()
        uptime = await utils.uptime()

        uptime_text = (
            f"{uptime.weeks} week(s),"
            if uptime.weeks
            else "" f"{uptime.days} day(s),"
            if uptime.days
            else "" f"{uptime.hours} hour(s), "
            if uptime.hours
            else "" f"{uptime.minutes} minute(s) and "
            if uptime.minutes
            else ""
        )

        embed = discord.Embed(
            title="Bot stats",
            description=f"Bot version: {wavy.__VERSION__}\n"
            f"Pycord version: {server_stats.pycord_version}\n"
            f"Python version: {server_stats.python_version}\n"
            f"Bot uptime: {uptime_text}"
            f"{uptime.seconds} second(s)\n"
            f"Guilds: {len(self.bot.guilds)}\n"
            f"Users: {len(list(self.bot.get_all_members()))}\n"
            f"Shards: {self.bot.shard_count}\n"
            f"Cogs: {len(self.bot.cogs)}\n"
            "\n**--- System information ---**\n"
            f"CPU: {server_stats.cpu_usage}/100%\n"
            f"RAM: {server_stats.ram_usage}/{server_stats.total_ram}GB\n"
            f"Disk: {server_stats.disk_usage}/{server_stats.total_disk}GB",
            colour=self.emb_colour,
        )

        view = discord.ui.View()

        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                url="https://wavybot.com",
                label="Website",
            )
        )
        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                url="https://discord.gg/Nbcf36Fge5",
                label="Discord Server",
            )
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed, view=view)

    @commands.guild_only()
    @commands.slash_command()
    async def serverinfo(self, ctx):
        """Cool stats nobody's going to look at"""
        guild = ctx.guild

        embed = discord.Embed(title=f"Info on {guild.name}", colour=self.emb_colour)

        embed.add_field(name="ID", value=guild.id, inline=True)

        embed.add_field(
            name="Created",
            value=f"<t:{round(time.mktime(guild.created_at.utctimetuple()))}:F>",
            inline=True,
        )

        embed.add_field(name="Owner", value=guild.owner.name, inline=False)

        embed.add_field(name="Members", value=guild.member_count, inline=True)

        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)

        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)

        embed.add_field(
            name="Boosts", value=str(len(guild.premium_subscribers)), inline=True
        )

        embed.add_field(
            name="Verification level", value=guild.verification_level, inline=True
        )

        # Add 1 to the guild shard ID since otherwise the integer starts at 0.

        embed.add_field(name="Shard", value=guild.shard_id + 1, inline=True)

        embed.set_thumbnail(url=guild.icon.url)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Nobody cares"""
        member = ctx.author if not member else member

        # Make a list of roles and remove the @everyone role

        roles = list(member.roles)
        roles.pop(0)

        # Create the embed and add all fields

        embed = discord.Embed(title=f"Info on {member}", colour=self.emb_colour)

        embed.add_field(name="Display name:", value=member.display_name, inline=False)

        embed.add_field(
            name="Account created at:",
            value=f"<t:{round(time.mktime(member.created_at.utctimetuple()))}:F>",
            inline=False,
        )

        embed.add_field(
            name="User joined at:",
            value=f"<t:{round(time.mktime(member.joined_at.utctimetuple()))}:F>",
            inline=False,
        )

        embed.add_field(name="Bot?", value=member.bot)

        embed.add_field(
            name="Roles:",
            value=" ".join([role.mention for role in roles]),
            inline=False,
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Here's a cool avatar that you may steal now"""
        member = ctx.author if not member else member

        # Image types (it's a bit messy, but for now it's fine)

        png = member.avatar.with_format("png").url
        jpg = member.avatar.with_format("jpg").url
        webp = member.avatar.with_format("webp").url

        try:
            gif = member.avatar.with_format("gif").url
        except InvalidArgument:
            gif = None

        embed = discord.Embed(
            title=f"{member.name}'s avatar",
            description=f"[PNG]({png})"
            f" | [JPG]({jpg})"
            f" | [WEBP]({webp})"
            f" | [GIF]({gif})"
            if gif
            else f"[PNG]({png})" f" | [JPG]({jpg})" f" | [WEBP]({webp})",
            colour=self.emb_colour,
        )

        embed.set_image(url=member.avatar.url)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def displayavatar(self, ctx, member: discord.Member = None):
        """The cooler avatar"""
        member = ctx.author if not member else member

        # Image types (it's a bit messy, but for now it's fine)

        png = member.display_avatar.with_format("png").url
        jpg = member.display_avatar.with_format("jpg").url
        webp = member.display_avatar.with_format("webp").url

        try:
            gif = member.display_avatar.with_format("gif").url
        except InvalidArgument:
            gif = None

        embed = discord.Embed(
            title=f"{member.name}'s display avatar",
            description=f"[PNG]({png})"
            f" | [JPG]({jpg})"
            f" | [WEBP]({webp})"
            f" | [GIF]({gif})"
            if gif
            else f"[PNG]({png})" f" | [JPG]({jpg})" f" | [WEBP]({webp})",
            colour=self.emb_colour,
        )

        embed.set_image(url=member.display_avatar.url)

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(General(bot))
