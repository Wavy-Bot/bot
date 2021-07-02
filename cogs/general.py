import os

import discord

from core import utils
from discord.ext import commands
from core import database

EMB_COLOUR = int(os.getenv("COLOUR"), 16)


class General(commands.Cog):
    """Cog that contains all general commands."""
    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database()

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot."""
        embed = discord.Embed(
            title="Pong :ping_pong:",
            description=f"Heartbeat: {round(self.bot.latency * 1000)}ms",
            colour=EMB_COLOUR)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['stats'])
    async def botinfo(self, ctx):
        """Sends info about the bot."""
        server_stats = await utils.server_stats()
        uptime = await utils.uptime()

        embed = discord.Embed(title="Wavy", colour=EMB_COLOUR)

        # Add all fields with the stats

        embed.add_field(name='General Stats',
                        value=f'• Guilds: {len(self.bot.guilds)}\n'
                        f'• Users: {len(list(self.bot.get_all_members()))} \n'
                        f'• Shards: {self.bot.shard_count}\n'
                        f'• Cogs: {len(self.bot.cogs)}\n'
                        f'• Commands: {len(self.bot.commands)}\n'
                        f'• Emojis: {len(self.bot.emojis)}\n'
                        f'• Voice Instances: {len(self.bot.voice_clients)}',
                        inline=True)

        embed.add_field(
            name="Server Stats",
            value=f"• CPU: {server_stats.cpu_usage}/100%\n"
            f"• RAM: {server_stats.ram_usage}/{server_stats.total_ram}MB\n"
            f"• Disk: {server_stats.disk_usage}/{server_stats.total_disk}GB\n"
            f"• OS: {server_stats.distro_name} {server_stats.distro_version}\n"
            f"• Kernel: {server_stats.kernel_version}\n"
            f"• Python: {server_stats.python_version}",
            inline=True)

        embed.add_field(
            name="Miscellaneous",
            value=f"[Website](https://wavybot.com)\n"
            f"[Discord Server](https://discord.gg/uDwQGyW)\n\n"
            f"**Uptime**:\n"
            f"{uptime.weeks} week(s), "
            f"{uptime.days} day(s), "
            f"{uptime.hours} hour(s), "
            f"{uptime.minutes} minute(s), {uptime.seconds} second(s)",
            inline=True)

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['guildinfo'])
    async def serverinfo(self, ctx):
        """Sends info about the current server."""
        guild = ctx.message.guild
        prefix = await self.db.fetch_config_prefix(guild.id)

        embed = discord.Embed(title=f"Info on {guild.name}", colour=EMB_COLOUR)

        embed.add_field(name="Owner", value=guild.owner.name, inline=True)

        embed.add_field(name="Members", value=guild.member_count, inline=True)

        embed.add_field(name="ID", value=guild.id, inline=True)

        embed.add_field(name="Verification level",
                        value=guild.verification_level,
                        inline=True)

        embed.add_field(name="Region", value=guild.region, inline=True)

        embed.add_field(name="Channels",
                        value=str(len(guild.channels)),
                        inline=True)

        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)

        embed.add_field(name="Boosts",
                        value=str(len(guild.premium_subscribers)),
                        inline=True)

        embed.add_field(name="Prefix", value=prefix, inline=True)

        embed.add_field(name="Created", value=guild.created_at, inline=True)

        # Add 1 to the guild shard ID since otherwise the integer starts at 0.

        embed.add_field(name="Shard", value=guild.shard_id + 1, inline=True)

        embed.set_thumbnail(url=guild.icon_url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['userinfo', 'memberinfo'])
    async def info(self, ctx, member: discord.Member = None):
        """Sends info about a member."""
        member = ctx.author if not member else member

        # Make a list of roles and remove the @everyone role

        roles = list(member.roles)
        roles.pop(0)

        # Create the embed and add all fields

        embed = discord.Embed(title=f"Info on {member}", colour=EMB_COLOUR)

        embed.add_field(name="Display name:",
                        value=member.display_name,
                        inline=False)

        embed.add_field(
            name="Account created at:",
            value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
            inline=False)

        embed.add_field(
            name="User joined at:",
            value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
            inline=False)

        embed.add_field(name="Bot?", value=member.bot)

        embed.add_field(name="Roles:",
                        value=" ".join([role.mention for role in roles]),
                        inline=False)

        embed.set_thumbnail(url=member.avatar_url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['pfp', 'av'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Sends a member's avatar."""
        member = ctx.author if not member else member

        # Image types (it's a bit messy, but for now it's fine)

        png = member.avatar_url_as(format='png')
        jpg = member.avatar_url_as(format='jpg')
        webp = member.avatar_url_as(format='webp')
        try:
            gif = member.avatar_url_as(format='gif')
        except discord.errors.InvalidArgument:
            gif = None

        embed = discord.Embed(title=f"{member.name}'s avatar",
                              description=f"[PNG]({png})"
                              f" | [JPG]({jpg})"
                              f" | [WEBP]({webp})"
                              f" | [GIF]({gif})" if gif else f"[PNG]({png})"
                              f" | [JPG]({jpg})"
                              f" | [WEBP]({webp})",
                              colour=EMB_COLOUR)

        embed.set_image(url=member.avatar_url)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Sends URLs to invite the bot, join the support server, etc."""
        embed = discord.Embed(title="Useful links", colour=EMB_COLOUR)

        embed.add_field(name="Invite",
                        value="[Click Here](https://invite.wavybot.com)",
                        inline=True)

        embed.add_field(name="Support Server",
                        value="[Click Here](https://discord.wavybot.com)",
                        inline=True)

        embed.add_field(name="Website",
                        value="[Click Here](https://wavybot.com)",
                        inline=True)

        embed.add_field(name="Documentation",
                        value="[Click Here](https://docs.wavybot.com)",
                        inline=True)

        embed.add_field(name="Web Dashboard",
                        value="[Click Here](https://dash.wavybot.com)",
                        inline=True)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(General(bot))
