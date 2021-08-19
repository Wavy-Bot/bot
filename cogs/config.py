import os

import discord

from core import database, classes
from discord.ext import commands


class Config(commands.Cog):
    """Cog that contains all config commands."""
    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()

    async def __cancel_message(self, title: str, reason: str):
        """Creates a message as to why the welcome message setup got cancelled"""
        embed = discord.Embed(
            title=title,
            description=f"Setup cancelled. Reason: `{reason}`",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        return embed

    @commands.group(aliases=["settings", "con"])
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        """Config group."""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
                title="Config",
                description=
                "No valid subcommand provided. Please use one of the following subcommands:"
                "\n`prefix`, `welcome`, `leave`, `autorole`, `cleverbot`, `logs`",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=embed)

    @config.group(aliases=["a", "ar", "auto_role", "role", "r"])
    @commands.has_permissions(manage_guild=True)
    async def autorole(self, ctx):
        """Autorole group."""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
                title="Autorole",
                description=
                "No valid subcommand provided. Please use one of the following subcommands:"
                "\n`add`, `remove`, `list`",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=embed)

    @config.command(aliases=["p", "pre"])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix: str = None):
        """Sets the bot's prefix in the current server. If no prefix provided it will return the current prefix."""
        if not prefix:
            prefix = await self.db.fetch_config_prefix(ctx.message.guild.id)

            embed = discord.Embed(
                title="Prefix",
                description=f"The current prefix is `{prefix}`.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=embed)

            return

        if len(prefix) > 2000:
            embed = discord.Embed(
                title="Prefix",
                description=
                "Unable to set prefix: prefix length is over 2000 characters.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=embed)

            return

        await self.db.set_config_prefix(ctx.message.guild.id, prefix)

        embed = discord.Embed(
            title="Prefix",
            description=f"Successfully set the prefix to `{prefix}`.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @config.command(aliases=["w", "join", "welcome_messages"])
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx):
        """Sets the bot's welcome message settings."""
        enable_list = ["yes", "enable", "true"]
        disable_list = ["no", "nope", "disable", "false"]

        def check(m):
            """Checks if the message channel is the same as it was and if the message author is also the same author."""
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        embed = discord.Embed(
            title="Welcome messages",
            description="Alright! Let's set up welcome messages.\n"
            "First, do you want welcome messages to be enabled or disabled?\n"
            "Reply with `yes` to enable them or with `no` to disable them.\n"
            "You can type `cancel` at any time to cancel the setup.\n"
            "\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        message = await ctx.send(embed=embed)

        enabled_input = await self.bot.wait_for('message',
                                                timeout=30,
                                                check=check)

        await enabled_input.delete()

        if enabled_input.content == "CANCEL".lower():
            embed = await self.__cancel_message(
                "Welcome messages", "User cancelled welcome message setup.")

            await message.edit(embed=embed)

            return

        if enabled_input.content.lower() in enable_list:
            enabled = True
        elif enabled_input.content.lower() in disable_list:
            enabled = False
        else:
            embed = embed = await self.__cancel_message(
                "Welcome messages", "User provided invalid option.")

            await message.edit(embed=embed)

            return

        await self.db.set_config_welcome(ctx.message.guild.id, enabled)

        if enabled:
            embed = discord.Embed(
                title="Welcome messages",
                description=
                "Second, what channel do you want the welcome messages to be sent in?\n"
                "(for example `#welcome`) or use its ID (for example `731143785769074780`)"
                "Also, please make sure that the bot has send message permissions in the desired channel.\n"
                "\nThis message will time out within 30 seconds.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            chann_input = await self.bot.wait_for('message',
                                                  timeout=30,
                                                  check=check)

            await chann_input.delete()

            if chann_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Welcome messages",
                    "User cancelled welcome message setup.")

                await message.edit(embed=embed)

                return

            try:
                channel = int(
                    chann_input.content.replace('<', '').replace('>',
                                                                 '').replace(
                                                                     '#', ''))
            except ValueError:
                embed = await self.__cancel_message(
                    "Welcome messages", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            channel = self.bot.get_channel(channel)

            if not channel:
                embed = await self.__cancel_message(
                    "Welcome messages", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            await self.db.set_channels_welcome(ctx.message.guild.id,
                                               channel.id)

            embed = discord.Embed(
                title="Welcome messages",
                description=
                "Third, What do you want the welcome message to be?\n"
                "Reply with `default` to use the default welcome message.\n"
                "\nThis message will time out within 4 minutes.",
                colour=self.emb_colour)

            embed.add_field(
                name="Tip",
                value=
                "Click [here](https://docs.wavybot.com/configuration/variables) to view all usable variables."
            )

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            message_input = await self.bot.wait_for('message',
                                                    timeout=240,
                                                    check=check)

            await message_input.delete()

            if message_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Welcome messages",
                    "User cancelled welcome message setup.")

                await message.edit(embed=embed)

                return

            if message_input.content == "DEFAULT".lower():
                w_message = None
            else:
                w_message = message_input.content

            await self.db.set_welcome_message(ctx.message.guild.id, w_message)

            embed = discord.Embed(
                title="Welcome messages",
                description=
                "Gotcha, Do you want the welcome message to be displayed as an embed?\n"
                "Reply with `yes` to enable embeds or with `no` to disable them.\n"
                "\nThis message will time out within 30 seconds.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            embed_input = await self.bot.wait_for('message',
                                                  timeout=30,
                                                  check=check)

            await embed_input.delete()

            if embed_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Welcome messages",
                    "User cancelled welcome message setup.")

                await message.edit(embed=embed)

                return

            if embed_input.content.lower() in enable_list:
                w_embed = True
            elif embed_input.content.lower() in disable_list:
                w_embed = False
            else:
                embed = await self.__cancel_message(
                    "Welcome messages", "User provided invalid option.")

                await message.edit(embed=embed)

                return

            await self.db.set_welcome_embed(ctx.message.guild.id, w_embed)

            if w_embed:
                embed = discord.Embed(
                    title="Welcome messages",
                    description=
                    "Now, onto the last part. What do you want the embed colour to be?\n"
                    "Please send an HTML colour code (e.g `#0c0f27`)"
                    "or reply with `default` to use the default colour.\n"
                    "\nThis message will time out within 1 minute.",
                    colour=self.emb_colour)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                await message.edit(embed=embed)

                colour_input = await self.bot.wait_for('message',
                                                       timeout=60,
                                                       check=check)

                await colour_input.delete()

                if colour_input.content == "CANCEL".lower():
                    embed = await self.__cancel_message(
                        "Welcome messages",
                        "User cancelled welcome message setup.")

                    await message.edit(embed=embed)

                    return

                if colour_input.content == "DEFAULT".lower():
                    colour = None
                else:
                    colour = colour_input.content.replace('#', '')

                    try:
                        int(colour, 16)
                    except ValueError:
                        embed = await self.__cancel_message(
                            "Welcome messages",
                            "Invalid colour code provided.")

                        await message.edit(embed=embed)

                        return

                await self.db.set_welcome_embed_colour(ctx.message.guild.id,
                                                       colour)

        embed = discord.Embed(
            title="Welcome messages",
            description="Here is a rundown of the information you provided.",
            colour=self.emb_colour)

        embed.add_field(name="Enabled", value=str(enabled))

        if enabled:
            embed.add_field(name="Channel", value=channel.mention)
            embed.add_field(name="Welcome message",
                            value=w_message if w_message else "default")
            embed.add_field(name="Embed", value=str(w_embed))
            if w_embed:
                embed.add_field(name="Embed colour",
                                value=colour_input.content)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

    @config.command(aliases=["l", "remove", "leave_messages", "fuckoff"])
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx):
        """Sets the bot's leave message settings."""
        enable_list = ["yes", "enable", "true"]
        disable_list = ["no", "nope", "disable", "false"]

        def check(m):
            """Checks if the message channel is the same as it was and if the message author is also the same author."""
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        embed = discord.Embed(
            title="Leave messages",
            description="Alright! Let's set up leave messages.\n"
            "First, do you want leave messages to be enabled or disabled?\n"
            "Reply with `yes` to enable them or with `no` to disable them.\n"
            "You can type `cancel` at any time to cancel the setup.\n"
            "\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        message = await ctx.send(embed=embed)

        enabled_input = await self.bot.wait_for('message',
                                                timeout=30,
                                                check=check)

        await enabled_input.delete()

        if enabled_input.content == "CANCEL".lower():
            embed = await self.__cancel_message(
                "Leave messages", "User cancelled leave message setup.")

            await message.edit(embed=embed)

            return

        if enabled_input.content.lower() in enable_list:
            enabled = True
        elif enabled_input.content.lower() in disable_list:
            enabled = False
        else:
            embed = await self.__cancel_message(
                "Leave messages", "User provided invalid option.")

            await message.edit(embed=embed)

            return

        await self.db.set_config_leave(ctx.message.guild.id, enabled)

        if enabled:
            embed = discord.Embed(
                title="Leave messages",
                description=
                "Second, what channel do you want the leave messages to be sent in?\n"
                "(for example `#leave`) or use its ID (for example `731143785769074780`)"
                "Also, please make sure that the bot has send message permissions in the desired channel.\n"
                "\nThis message will time out within 30 seconds.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            chann_input = await self.bot.wait_for('message',
                                                  timeout=30,
                                                  check=check)

            await chann_input.delete()

            if chann_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Leave messages", "User cancelled leave message setup.")

                await message.edit(embed=embed)

                return

            try:
                channel = int(
                    chann_input.content.replace('<', '').replace('>',
                                                                 '').replace(
                                                                     '#', ''))
            except ValueError:
                embed = await self.__cancel_message(
                    "Leave messages", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            channel = self.bot.get_channel(channel)

            if not channel:
                embed = await self.__cancel_message(
                    "Leave messages", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            await self.db.set_channels_leave(ctx.message.guild.id, channel.id)

            embed = discord.Embed(
                title="Leave messages",
                description="Third, What do you want the leave message to be?\n"
                "Reply with `default` to use the default leave message.\n"
                "\nThis message will time out within 4 minutes.",
                colour=self.emb_colour)

            embed.add_field(
                name="Tip",
                value=
                "Click [here](https://docs.wavybot.com/configuration/variables) to view all usable variables."
            )

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            message_input = await self.bot.wait_for('message',
                                                    timeout=240,
                                                    check=check)

            await message_input.delete()

            if message_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Leave messages", "User cancelled leave message setup.")

                await message.edit(embed=embed)

                return

            if message_input.content == "DEFAULT".lower():
                l_message = None
            else:
                l_message = message_input.content

            await self.db.set_leave_message(ctx.message.guild.id, l_message)

            embed = discord.Embed(
                title="Leave messages",
                description=
                "Gotcha, Do you want the leave message to be displayed as an embed?\n"
                "Reply with `yes` to enable embeds or with `no` to disable them.\n"
                "\nThis message will time out within 30 seconds.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            embed_input = await self.bot.wait_for('message',
                                                  timeout=30,
                                                  check=check)

            await embed_input.delete()

            if embed_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Leave messages", "User cancelled leave message setup.")

                await message.edit(embed=embed)

                return

            if embed_input.content.lower() in enable_list:
                l_embed = True
            elif embed_input.content.lower() in disable_list:
                l_embed = False
            else:
                embed = await self.__cancel_message(
                    "Leave messages", "User provided invalid option.")

                await message.edit(embed=embed)

                return

            await self.db.set_leave_embed(ctx.message.guild.id, l_embed)

            if l_embed:
                embed = discord.Embed(
                    title="Leave messages",
                    description=
                    "Now, onto the last part. What do you want the embed colour to be?\n"
                    "Please send an HTML colour code (e.g `#0c0f27`)"
                    "or reply with `default` to use the default colour.\n"
                    "\nThis message will time out within 1 minute.",
                    colour=self.emb_colour)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=self.bot.user.avatar_url)

                await message.edit(embed=embed)

                colour_input = await self.bot.wait_for('message',
                                                       timeout=60,
                                                       check=check)

                await colour_input.delete()

                if colour_input.content == "CANCEL".lower():
                    embed = await self.__cancel_message(
                        "Leave messages",
                        "User cancelled leave message setup.")

                    await message.edit(embed=embed)

                    return

                if colour_input.content == "DEFAULT".lower():
                    colour = None
                else:
                    colour = colour_input.content.replace('#', '')

                    try:
                        int(colour, 16)
                    except ValueError:
                        embed = await self.__cancel_message(
                            "Leave messages", "Invalid colour code provided.")

                        await message.edit(embed=embed)

                        return

                await self.db.set_leave_embed_colour(ctx.message.guild.id,
                                                     colour)

        embed = discord.Embed(
            title="Leave messages",
            description="Here is a rundown of the information you provided.",
            colour=self.emb_colour)

        embed.add_field(name="Enabled", value=str(enabled))

        if enabled:
            embed.add_field(name="Channel", value=channel.mention)

            embed.add_field(name="Leave message",
                            value=l_message if l_message else "default")
            embed.add_field(name="Embed", value=str(l_embed))
            if l_embed:
                embed.add_field(name="Embed colour",
                                value=colour_input.content)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

    @config.command(aliases=["c", "cl", "bot", "clever"])
    @commands.has_permissions(manage_guild=True)
    async def cleverbot(self, ctx):
        """Sets the bot's cleverbot settings."""
        enable_list = ["yes", "enable", "true"]
        disable_list = ["no", "nope", "disable", "false"]

        def check(m):
            """Checks if the message channel is the same as it was and if the message author is also the same author."""
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        embed = discord.Embed(
            title="Cleverbot",
            description="Alright! Let's set up Cleverbot.\n"
            "First, do you want Cleverbot to be enabled or disabled?\n"
            "Reply with `yes` to enable it or with `no` to disable it.\n"
            "You can type `cancel` at any time to cancel the setup.\n"
            "\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        message = await ctx.send(embed=embed)

        enabled_input = await self.bot.wait_for('message',
                                                timeout=30,
                                                check=check)

        await enabled_input.delete()

        if enabled_input.content == "CANCEL".lower():
            embed = await self.__cancel_message(
                "Cleverbot", "User cancelled Cleverbot setup.")

            await message.edit(embed=embed)

            return

        if enabled_input.content.lower() in enable_list:
            enabled = True
        elif enabled_input.content.lower() in disable_list:
            enabled = False
        else:
            embed = await self.__cancel_message(
                "Cleverbot", "User provided invalid option.")

            await message.edit(embed=embed)

            return

        await self.db.set_config_cleverbot(ctx.message.guild.id, enabled)

        if enabled:
            embed = discord.Embed(
                title="Cleverbot",
                description=
                "Second, what channel do you want the Cleverbot messages to be sent in?\n"
                "(for example `#cleverbot`) or use its ID (for example `731143785769074780`)"
                "Also, please make sure that the bot has send message permissions in the desired channel.\n"
                "\nThis message will time out within 30 seconds.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            chann_input = await self.bot.wait_for('message',
                                                  timeout=30,
                                                  check=check)

            await chann_input.delete()

            if chann_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Cleverbot", "User cancelled Cleverbot setup.")

                await message.edit(embed=embed)

                return

            try:
                channel = int(
                    chann_input.content.replace('<', '').replace('>',
                                                                 '').replace(
                                                                     '#', ''))
            except ValueError:
                embed = await self.__cancel_message(
                    "Cleverbot", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            channel = self.bot.get_channel(channel)

            if not channel:
                embed = await self.__cancel_message(
                    "Cleverbot", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            await self.db.set_channels_cleverbot(ctx.message.guild.id,
                                                 channel.id)

        embed = discord.Embed(
            title="Cleverbot",
            description="Here is a rundown of the information you provided.",
            colour=self.emb_colour)

        embed.add_field(name="Enabled", value=str(enabled))

        if enabled:
            embed.add_field(name="Channel", value=channel.mention)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

    @config.command(aliases=["lo", "log", "logging"])
    @commands.has_permissions(manage_guild=True)
    async def logs(self, ctx):
        """Sets the bot's logging settings."""
        enable_list = ["yes", "enable", "true"]
        disable_list = ["no", "nope", "disable", "false"]

        def check(m):
            """Checks if the message channel is the same as it was and if the message author is also the same author."""
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        embed = discord.Embed(
            title="Logs",
            description="Alright! Let's set up logging.\n"
            "First, do you want logs to be enabled or disabled?\n"
            "Reply with `yes` to enable it or with `no` to disable it.\n"
            "You can type `cancel` at any time to cancel the setup.\n"
            "\nThis message will time out within 30 seconds.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        message = await ctx.send(embed=embed)

        enabled_input = await self.bot.wait_for('message',
                                                timeout=30,
                                                check=check)

        await enabled_input.delete()

        if enabled_input.content == "CANCEL".lower():
            embed = await self.__cancel_message(
                "Logs", "User cancelled logging setup.")

            await message.edit(embed=embed)

            return

        if enabled_input.content.lower() in enable_list:
            enabled = True
        elif enabled_input.content.lower() in disable_list:
            enabled = False
        else:
            embed = await self.__cancel_message(
                "Logs", "User provided invalid option.")

            await message.edit(embed=embed)

            return

        await self.db.set_config_logs(ctx.message.guild.id, enabled)

        if enabled:
            embed = discord.Embed(
                title="Logs",
                description=
                "Second, what channel do you want the log messages to be sent in?\n"
                "(for example `#logs`) or use its ID (for example `731143785769074780`)"
                "Also, please make sure that the bot has send message permissions in the desired channel.\n"
                "\nThis message will time out within 30 seconds.",
                colour=self.emb_colour)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            chann_input = await self.bot.wait_for('message',
                                                  timeout=30,
                                                  check=check)

            await chann_input.delete()

            if chann_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Logs", "User cancelled logging setup.")

                await message.edit(embed=embed)

                return

            try:
                channel = int(
                    chann_input.content.replace('<', '').replace('>',
                                                                 '').replace(
                                                                     '#', ''))
            except ValueError:
                embed = await self.__cancel_message(
                    "Logs", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            channel = self.bot.get_channel(channel)

            if not channel:
                embed = await self.__cancel_message(
                    "Logs", "User provided invalid channel.")

                await message.edit(embed=embed)

                return

            await self.db.set_channels_log(ctx.message.guild.id, channel.id)

            options_dict = {
                "msg_delete":
                classes.LogOptions(description="Called on message deletion.",
                                   value=False),
                "msg_bulk_delete":
                classes.LogOptions(
                    description="Called on bulk message deletion.",
                    value=False),
                "msg_edit":
                classes.LogOptions(description="Called on message edit.",
                                   value=False),
                "ch_create":
                classes.LogOptions(description="Called on channel creation.",
                                   value=False),
                "ch_delete":
                classes.LogOptions(description="Called on channel deletion.",
                                   value=False),
                "member_ban":
                classes.LogOptions(description="Called on member ban.",
                                   value=False),
                "member_unban":
                classes.LogOptions(description="Called on member unban.",
                                   value=False),
                "voicestate_update":
                classes.LogOptions(description="Called on voicestate update.",
                                   value=False),
                "guild_update":
                classes.LogOptions(description="Called on guild update.",
                                   value=False),
                "role_create":
                classes.LogOptions(description="Called on role creation.",
                                   value=False),
                "role_update":
                classes.LogOptions(description="Called on channel update.",
                                   value=False),
                "role_delete":
                classes.LogOptions(description="Called on channel deletion.",
                                   value=False),
                "emoji_update":
                classes.LogOptions(description="Called on emoji update.",
                                   value=False),
                "invite_create":
                classes.LogOptions(description="Called on invite creation.",
                                   value=False),
                "invite_delete":
                classes.LogOptions(description="Called on invite deletion.",
                                   value=False)
            }

            embed = discord.Embed(
                title="Logs",
                description="Finally, what features do you want to be enabled?\n"
                "(example usage: `message_delete, member_ban, msg_edit`)\n"
                "\nThis message will time out within 5 minutes.",
                colour=self.emb_colour)

            for name, values in options_dict.items():
                embed.add_field(name=name, value=values.description)

            embed.set_footer(text="Wavy • https://wavybot.com",
                             icon_url=self.bot.user.avatar_url)

            await message.edit(embed=embed)

            feature_input = await self.bot.wait_for('message',
                                                    timeout=300,
                                                    check=check)

            await feature_input.delete()

            if feature_input.content == "CANCEL".lower():
                embed = await self.__cancel_message(
                    "Logs", "User cancelled logging setup.")

                await message.edit(embed=embed)

                return

            config_list = []

            for name, values in options_dict.items():
                if name in feature_input.content:
                    values.value = True
                config_list.append(values.value)

            await self.db.set_logs(ctx.message.guild.id, *config_list)

        embed = discord.Embed(
            title="Logs",
            description="Here is a rundown of the information you provided.",
            colour=self.emb_colour)

        embed.add_field(name="Enabled", value=str(enabled))

        if enabled:
            embed.add_field(name="Channel", value=channel.mention)

            for name, values in options_dict.items():
                if values.value:
                    embed.add_field(name=name, value=str(values.value))

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await message.edit(embed=embed)

    @autorole.command(aliases=["a"])
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, *, role: discord.Role):
        """Adds a role to the autorole list."""
        await self.db.set_role(ctx.message.guild.id, role.id, "auto")

        embed = discord.Embed(
            title="Autorole",
            description=f"Successfully added {role.mention} to the list.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @autorole.command(aliases=["r", "rm", "del", "delete", "yeet"])
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, *, role: discord.Role):
        """Removes a role from the autorole list."""
        db_role = await self.db.remove_role(ctx.message.guild.id, role.id,
                                            "auto")

        embed = discord.Embed(
            title="Autorole",
            description=f"Successfully removed {role.mention} from the list."
            if db_role else f"Could not find {role.mention} in the list.",
            colour=self.emb_colour)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @autorole.command(aliases=["l", "li", "dir", "ls"])
    async def list(self, ctx, member: discord.Member = None):
        """Sends the configured autoroles."""
        member = ctx.author if not member else member

        roles = await self.db.fetch_roles(ctx.message.guild.id, "auto")

        embed = discord.Embed(title="Showing autoroles" if roles else
                              "No autoroles have been set for this server.",
                              colour=self.emb_colour)

        # TODO(Robert): Add pagination.

        for i in roles:
            role = discord.utils.get(member.guild.roles, id=i.role_id)

            if role:
                embed.add_field(name=role.name,
                                value=role.mention,
                                inline=False)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Config(bot))
