import os

import discord

from core import exceptions, database, request
from discord.ext import commands
from string import Formatter


class Events(commands.Cog):
    """Class that contains all the bot events."""
    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database()
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.err_colour = int(os.getenv("ERR_COLOUR"), 16)

    @staticmethod
    async def __parse_message(message: str, member):
        """Parses a message and changes values where needed."""
        parsed_msg = [
            fn for _, fn, _, _ in Formatter().parse(message) if fn is not None
        ]

        if parsed_msg:
            # Note(Robert): This is for security reasons since I don't want people to be able to access
            #               anything else than just these variables.
            server_name = member.guild.name
            member_mention = member.mention
            member_full = member.name + member.discriminator
            member_nickname = member.display_name
            member_count = len(member.guild.members)

            usable_vars = {
                "server_name": server_name,
                "member_mention": member_mention,
                "member_full": member_full,
                "member_nickname": member_nickname,
                "member_count": member_count
            }

            for i in parsed_msg:
                if i not in usable_vars:
                    message = message.replace("{" + i + "}", "")

            message = message.format(**usable_vars)

        return message

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is done preparing the data received from Discord."""
        print(f'Logged in as\n{self.bot.user.name}\n{self.bot.user.id}')

    @commands.Cog.listener()
    async def on_connect(self):
        """Called when the client has successfully connected to Discord."""
        guilds = self.bot.guilds

        await self.db.remove_old_guilds(guilds)

        for i in guilds:
            await self.db.add_guild(i.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild."""
        await self.db.add_guild(guild.id)

        guild_channel = guild.text_channels[0]
        message_channel = self.bot.get_channel(guild_channel.id)

        message = "**Hi there, I'm Wavy** - The blazing-fast Discord bot.\n" \
                  "- My prefix is `%`\n" \
                  "- You can see a list of commands by typing `%help`\n" \
                  "- You can set me up by going to <https://dash.wavybot.com>\n" \
                  "- If you need help, feel free to join my support server over at https://discord.wavybot.com"

        try:
            await message_channel.send(message)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Called when the bot leaves a guild."""
        await self.db.remove_guild(guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Called when a new member joins a guild."""
        channel_id = await self.db.fetch_channels_welcome(member.guild.id)
        if await self.db.fetch_config_welcome(member.guild.id) and channel_id:
            channel = self.bot.get_channel(channel_id)
            # Fetch welcome config from the database, check if it needs to be an embed and send the message.
            config = await self.db.fetch_welcome(member.guild.id)
            message = config.message

            if message:
                message = await self.__parse_message(message, member)

            else:
                message = f"Welcome to {member.guild.name}, {member.mention}! We now have {len(member.guild.members)} members."

            if config.embed:
                colour = self.emb_colour
                if config.embed_colour:
                    colour = int(config.embed_colour, 16)

                embed = discord.Embed(title=":tada: Welcome!",
                                      description=message,
                                      colour=colour)

                embed.set_thumbnail(url=member.avatar_url)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                try:
                    await channel.send(embed=embed)
                except AttributeError:
                    raise exceptions.NonExistantChannelError(
                        message=
                        f"The channel with ID {channel_id} does not exist.")

            else:
                try:
                    await channel.send(message)
                except AttributeError:
                    raise exceptions.NonExistantChannelError(
                        message=
                        f"The channel with ID {channel_id} does not exist.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Called when a member leaves a guild."""
        channel_id = await self.db.fetch_channels_leave(member.guild.id)
        if await self.db.fetch_config_leave(member.guild.id) and channel_id:
            channel = self.bot.get_channel(channel_id)
            # Fetch leave config from the database, check if it needs to be an embed and send the message.
            config = await self.db.fetch_leave(member.guild.id)
            message = config.message

            if message:
                message = await self.__parse_message(message, member)

            else:
                message = f"{member.mention} left the server, there are now {len(member.guild.members)} members in this server."

            if config.embed:
                colour = self.emb_colour
                if config.embed_colour:
                    colour = int(config.embed_colour, 16)

                embed = discord.Embed(title=":wave: Cya!",
                                      description=message,
                                      colour=colour)

                embed.set_thumbnail(url=member.avatar_url)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                try:
                    await channel.send(embed=embed)
                except AttributeError:
                    raise exceptions.NonExistantChannelError(
                        message=
                        f"The channel with ID {channel_id} does not exist.")

            else:
                try:
                    await channel.send(message)
                except AttributeError:
                    raise exceptions.NonExistantChannelError(
                        message=
                        f"The channel with ID {channel_id} does not exist.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Called when a member sends a message."""
        member = message.author

        # skipcq: PTC-W0048
        if not member.bot:
            if await self.db.fetch_config_cleverbot(message.guild.id):
                channel_id = await self.db.fetch_channels_cleverbot(
                    message.guild.id)
                if channel_id:
                    channel = self.bot.get_channel(channel_id)

                    if message.channel == channel:
                        async with message.channel.typing():
                            res = await request.cleverbot(
                                message.content, member.id)
                            embed = discord.Embed(title="Cleverbot",
                                                  description=res,
                                                  colour=self.emb_colour)

                            embed.set_footer(text="Wavy • https://wavybot.com",
                                             icon_url=self.bot.user.avatar_url)

                            try:
                                await channel.send(embed=embed)
                            except AttributeError:
                                raise exceptions.NonExistantChannelError(
                                    message=
                                    f"The channel with ID {channel_id} does not exist."
                                )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Called when an exception was called."""
        # TODO(Robert): Set the correct documentation URLs
        #               and declutter this. For now I'll add this:
        # skipcq: PYL-R1705
        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingRole):
            description = f"You don't have permission to execute `{ctx.invoked_with}`." \
                          f"You need the `{error.missing_role}` role. "

        elif isinstance(error, commands.MissingPermissions):
            # NOTE(Robert): I am aware that this is far
            #               from the best way to do this.
            permission_string = ""

            for i in error.missing_perms:
                permission_string += f"• `{i}`\n"

            description = f"You don't have permission to execute `{ctx.invoked_with}`." \
                          f"You need the following permissions:\n{permission_string}"

        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, ValueError):
                description = "Please mention or put in a valid channel ID. Not sure how to do this? Click [here](" \
                              "#)."

            elif isinstance(error.original, discord.Forbidden):
                description = "Wavy does not have the required permissions to do that. Please also make sure that you" \
                              " have put Wavy's role above all other roles. Not sure how to do this? Click [here](" \
                              "https://docs.wavybot.com). "

            else:
                description = f"`{error}`"

        elif isinstance(error, commands.NSFWChannelRequired):
            description = "Please set the channel to be NSFW, or move to an NSFW channel. Not sure how to do this? " \
                          "Click [here](https://docs.wavybot.com)."

        elif isinstance(error, exceptions.APIError):
            description = error

        else:
            description = f"`{error}`"

        embed = discord.Embed(title="Error",
                              description=description,
                              colour=self.err_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Events(bot))
