import os
import json

import discord

from core import exceptions, database, request
from discord.ext import commands, tasks
from string import Formatter
from datetime import datetime


class Events(commands.Cog):
    """Class that contains all the bot events."""
    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database()
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.err_colour = int(os.getenv("ERR_COLOUR"), 16)
        self.check_mute.start()
        self.check_giveaways.start()
        self.post_botlist_data.start()

    def cog_unload(self):
        """Runs when the cog gets unloaded."""
        self.check_mute.cancel()
        self.check_giveaways.cancel()
        self.post_botlist_data.cancel()

    @staticmethod
    async def __parse_message(message: str, member):
        """Parses a message and changes values where needed."""
        # TODO(Robert): Check if this does not introduce security issues.
        parsed_msg = [
            fn for _, fn, _, _ in Formatter().parse(message) if fn is not None
        ]

        if parsed_msg:
            # NOTE(Robert): This is for security reasons since I don't want people to be able to access
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

    @staticmethod
    async def __list_to_string(i_list: list):
        """Converts a list to a string."""
        string = ' '.join(list(i_list))

        return string

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

    @tasks.loop(seconds=1800)
    async def post_botlist_data(self):
        """POSTs data to botlists."""
        await self.bot.wait_until_ready()

        await request.botlists(len(self.bot.guilds),
                               len(list(self.bot.get_all_members())),
                               self.bot.shard_count)

    @tasks.loop(seconds=10)
    async def check_mute(self):
        """Checks the current mutes in the database."""
        await self.bot.wait_until_ready()

        mutes = await self.db.fetch_mutes()

        for i in mutes:
            if i.end_time and i.end_time <= datetime.utcnow():
                server = self.bot.get_guild(i.server_id)

                member = discord.utils.get(server.members, id=i.member_id)

                if member:

                    fetch_role = await self.db.fetch_single_role(
                        server.id, "mute")

                    role = discord.utils.get(server.roles,
                                             id=fetch_role.role_id)

                    if role:
                        await member.remove_roles(role)

                await self.db.remove_mute(server.id, member.id)

    @tasks.loop(seconds=10)
    async def check_giveaways(self):
        """Checks the current giveaways in the database."""
        await self.bot.wait_until_ready()

        giveaways = await self.db.fetch_giveaways()

        for giveaway in giveaways:
            if giveaway.end_time <= datetime.utcnow():
                channel = self.bot.get_channel(giveaway.channel_id)

                if channel:
                    try:
                        message = await channel.fetch_message(
                            giveaway.message_id)
                    except discord.errors.NotFound:
                        await self.db.remove_giveaway(giveaway.server_id,
                                                      giveaway.message_id)
                        continue

                    winners = []

                    for reaction in message.reactions:
                        async for user in reaction.users():
                            if not user.bot and len(
                                    winners) <= giveaway.winners:
                                winners.append(user)

                    if not winners:
                        await channel.send("no-one entered the giveaway.")

                        await self.db.remove_giveaway(giveaway.server_id,
                                                      giveaway.message_id)

                        continue

                    for winner in winners:
                        await channel.send(
                            f"{winner.mention} has won the giveaway!")

                    embed = discord.Embed(
                        title="🎉 **GIVEAWAY** 🎉",
                        description="This giveaway has ended.",
                        colour=self.emb_colour)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await message.edit(embed=embed)

                    await message.clear_reaction('🎉')

                await self.db.remove_giveaway(giveaway.server_id,
                                              giveaway.message_id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild."""
        await self.db.add_guild(guild.id)

        guild_channel = guild.text_channels[0]
        message_channel = self.bot.get_channel(guild_channel.id)

        message = "**Hi there, I'm Wavy** - The blazing-fast Discord bot.\n" \
                  "- My prefix is `%`\n" \
                  "- You can see a list of commands by typing `%help`\n" \
                  "- You can set me up by going to <https://wavybot.com>\n" \
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

            roles = await self.db.fetch_roles(member.guild.id, "auto")

            if roles:
                role_list = []

                for i in roles:
                    role = discord.utils.get(member.guild.roles, id=i.role_id)

                    if role:
                        role_list.append(role)
                await member.add_roles(*role_list, reason="Autorole")

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
        if not isinstance(message.channel,
                          discord.DMChannel) and not member.bot:
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
    async def on_message_delete(self, message):
        """Called when a message is deleted."""
        if not isinstance(message.channel,
                          discord.DMChannel) and not message.author.bot:

            with open("snipe.json", "r") as json_file:
                snipe_file = json.load(json_file)
                json_file.close()

            if str(message.guild.id) not in snipe_file:
                snipe_file[str(message.guild.id)] = {}

            snipe_file[str(message.guild.id)][str(message.channel.id)] = {
                "member_id": message.author.id,
                "content": message.content,
                "attachments": [i.url for i in message.attachments]
            }

            with open("snipe.json", "w") as json_file:
                json.dump(snipe_file, json_file, indent=4)

            json_file.close()

            enabled = await self.db.fetch_config_logs(message.guild.id)

            if enabled:
                config = await self.db.fetch_logs(message.guild.id)

                if config.msg_delete:
                    channel_id = await self.db.fetch_channels_log(
                        message.guild.id)
                    channel = self.bot.get_channel(channel_id)

                    if channel:
                        embed = discord.Embed(
                            title="Message deleted",
                            description="A message got deleted.",
                            colour=self.emb_colour)

                        embed.add_field(name="Message author",
                                        value=message.author.mention,
                                        inline=False)

                        if message.content:
                            embed.add_field(name="Message content",
                                            value=message.content,
                                            inline=False)

                        if message.attachments:
                            embed.add_field(
                                name="Message attachments",
                                value=str([i.url
                                           for i in message.attachments]),
                                inline=False)

                        embed.add_field(name="Message channel",
                                        value=message.channel.mention,
                                        inline=False)

                        embed.set_thumbnail(url=message.author.avatar_url)

                        embed.set_footer(text="Wavy • https://wavybot.com",
                                         icon_url=self.bot.user.avatar_url)

                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        """Called when messages are bulk deleted."""
        if not isinstance(messages[0].channel, discord.DMChannel):
            enabled = await self.db.fetch_config_logs(messages[0].guild.id)

            if enabled:
                config = await self.db.fetch_logs(messages[0].guild.id)

                if config.msg_bulk_delete:
                    channel_id = await self.db.fetch_channels_log(
                        messages[0].guild.id)
                    channel = self.bot.get_channel(channel_id)

                    if channel:
                        embed = discord.Embed(
                            title="Messages bulk deleted",
                            description="Messages got bulk deleted.",
                            colour=self.emb_colour)

                        embed.add_field(name="Message channel",
                                        value=messages[0].channel.mention,
                                        inline=False)

                        embed.add_field(name="Messages deleted",
                                        value=str(len(messages)),
                                        inline=False)

                        embed.set_footer(text="Wavy • https://wavybot.com",
                                         icon_url=self.bot.user.avatar_url)

                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Called when a message is edited."""
        if not isinstance(before.channel,
                          discord.DMChannel) and not before.author.bot:
            enabled = await self.db.fetch_config_logs(before.guild.id)

            if enabled:
                config = await self.db.fetch_logs(before.guild.id)

                if config.msg_edit:
                    channel_id = await self.db.fetch_channels_log(
                        before.guild.id)
                    channel = self.bot.get_channel(channel_id)

                    if channel:
                        embed = discord.Embed(title="Message edited",
                                              colour=self.emb_colour)

                        embed.add_field(name="Message author",
                                        value=before.author.mention,
                                        inline=False)

                        embed.add_field(name="Before",
                                        value=f"```{before.content}```",
                                        inline=False)

                        embed.add_field(name="After",
                                        value=f"```{after.content}```",
                                        inline=False)

                        embed.add_field(name="Message channel",
                                        value=before.channel.mention,
                                        inline=False)

                        embed.add_field(
                            name="Message link",
                            value=f"[Go to message]({before.jump_url})",
                            inline=False)

                        embed.set_thumbnail(url=before.author.avatar_url)

                        embed.set_footer(text="Wavy • https://wavybot.com",
                                         icon_url=self.bot.user.avatar_url)

                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        """Called when a member gets banned from a guild."""
        enabled = await self.db.fetch_config_logs(guild.id)

        if enabled:
            config = await self.db.fetch_logs(guild.id)

            if config.member_ban:
                channel_id = await self.db.fetch_channels_log(guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Member banned",
                                          colour=self.emb_colour)

                    embed.add_field(name="Member",
                                    value=member.mention,
                                    inline=False)

                    embed.set_thumbnail(url=member.avatar_url)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        """Called when a member gets unbanned from a guild."""
        enabled = await self.db.fetch_config_logs(guild.id)

        if enabled:
            config = await self.db.fetch_logs(guild.id)

            if config.member_unban:
                channel_id = await self.db.fetch_channels_log(guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Member unbanned",
                                          colour=self.emb_colour)

                    embed.add_field(name="Member",
                                    value=member.mention,
                                    inline=False)

                    embed.set_thumbnail(url=member.avatar_url)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Called when a guild channel is created."""
        enabled = await self.db.fetch_config_logs(channel.guild.id)

        if enabled:
            config = await self.db.fetch_logs(channel.guild.id)

            if config.ch_create:
                channel_id = await self.db.fetch_channels_log(channel.guild.id)
                guild_channel = self.bot.get_channel(channel_id)

                if guild_channel:
                    embed = discord.Embed(title="Channel created",
                                          colour=self.emb_colour)

                    embed.add_field(name="Channel",
                                    value=channel.mention,
                                    inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await guild_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Called when a guild channel is deleted."""
        enabled = await self.db.fetch_config_logs(channel.guild.id)

        if enabled:
            config = await self.db.fetch_logs(channel.guild.id)

            if config.ch_delete:
                channel_id = await self.db.fetch_channels_log(channel.guild.id)
                guild_channel = self.bot.get_channel(channel_id)

                if guild_channel:
                    embed = discord.Embed(title="Channel deleted",
                                          colour=self.emb_colour)

                    embed.add_field(name="Channel",
                                    value=channel.name,
                                    inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await guild_channel.send(embed=embed)

    @commands.Cog.listener()
    # skipcq: PYL-W0613
    async def on_voice_state_update(self, member, before, after):
        """Called when a member changes their voicestate."""
        enabled = await self.db.fetch_config_logs(member.guild.id)

        if enabled:
            config = await self.db.fetch_logs(member.guild.id)

            if config.voicestate_update:
                channel_id = await self.db.fetch_channels_log(member.guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Voice state updated",
                                          colour=self.emb_colour)

                    embed.add_field(name="Member",
                                    value=member.mention,
                                    inline=False)

                    if after.channel:
                        embed.add_field(name="Channel",
                                        value=after.channel.mention,
                                        inline=False)

                    embed.add_field(name="Disconnected",
                                    value="False" if after.channel else "True",
                                    inline=False)

                    embed.add_field(name="Muted",
                                    value=str(after.self_mute),
                                    inline=False)

                    embed.add_field(name="Deafened",
                                    value=str(after.self_deaf),
                                    inline=False)

                    embed.add_field(name="Server muted",
                                    value=str(after.mute),
                                    inline=False)

                    embed.add_field(name="Server deafened",
                                    value=str(after.deaf),
                                    inline=False)

                    embed.set_thumbnail(url=member.avatar_url)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """Called when a guild updates."""
        enabled = await self.db.fetch_config_logs(before.id)

        if enabled:
            config = await self.db.fetch_logs(before.id)

            if config.guild_update:
                channel_id = await self.db.fetch_channels_log(before.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Guild updated",
                                          colour=self.emb_colour)

                    embed.add_field(name="Name",
                                    value=after.name,
                                    inline=False)

                    embed.add_field(name="Owner",
                                    value=after.owner.mention,
                                    inline=False)

                    embed.add_field(name="Text channels",
                                    value=str(len(after.text_channels)),
                                    inline=False)

                    embed.add_field(name="Voice channels",
                                    value=str(len(after.voice_channels)),
                                    inline=False)

                    embed.add_field(name="Shard ID",
                                    value=str(after.shard_id + 1),
                                    inline=False)

                    embed.set_thumbnail(url=after.icon_url)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Called when a guild creates a new role."""
        enabled = await self.db.fetch_config_logs(role.guild.id)

        if enabled:
            config = await self.db.fetch_logs(role.guild.id)

            if config.role_create:
                channel_id = await self.db.fetch_channels_log(role.guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Role created",
                                          colour=self.emb_colour)

                    embed.add_field(name="Name",
                                    value=role.mention,
                                    inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Called when a guild deletes a role."""
        enabled = await self.db.fetch_config_logs(role.guild.id)

        if enabled:
            config = await self.db.fetch_logs(role.guild.id)

            if config.role_delete:
                channel_id = await self.db.fetch_channels_log(role.guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Role deleted",
                                          colour=self.emb_colour)

                    embed.add_field(name="Name", value=role.name, inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """
        Called when a guild updates a role.
        This causes a lot of spam, and I do not recommend using it.
        """
        enabled = await self.db.fetch_config_logs(before.guild.id)

        if enabled:
            config = await self.db.fetch_logs(before.guild.id)

            if config.role_update:
                channel_id = await self.db.fetch_channels_log(before.guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Role updated",
                                          colour=self.emb_colour)

                    embed.add_field(name="Name",
                                    value=after.name,
                                    inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        """Called when a guild adds or removes an emoji."""
        enabled = await self.db.fetch_config_logs(guild.id)

        if enabled:
            config = await self.db.fetch_logs(guild.id)

            if config.emoji_update:
                channel_id = await self.db.fetch_channels_log(guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    # NOTE(Robert): This is a mess.
                    old_emoji = [
                        f"<:{i.name}:{i.id}>" for i in before if i.is_usable()
                    ]
                    new_emoji = [
                        f"<:{i.name}:{i.id}>" for i in after if i.is_usable()
                    ]
                    old_emoji = await self.__list_to_string(old_emoji)
                    new_emoji = await self.__list_to_string(new_emoji)

                    embed = discord.Embed(title="Emojis updated",
                                          colour=self.emb_colour)

                    embed.add_field(name="Before",
                                    value=old_emoji,
                                    inline=False)

                    embed.add_field(name="After",
                                    value=new_emoji,
                                    inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        """Called when an invite is created."""
        enabled = await self.db.fetch_config_logs(invite.guild.id)

        if enabled:
            config = await self.db.fetch_logs(invite.guild.id)

            if config.invite_create:
                channel_id = await self.db.fetch_channels_log(invite.guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Invite created",
                                          colour=self.emb_colour)

                    embed.add_field(name="Link",
                                    value=f"[{invite.id}]({invite.url})",
                                    inline=False)

                    embed.add_field(name="Max uses",
                                    value=str(invite.max_uses)
                                    if invite.max_uses != 0 else "Unlimited",
                                    inline=False)

                    embed.add_field(
                        name="Temporary membership",
                        value="True" if invite.temporary else "False",
                        inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        """Called when an invite is deleted."""
        enabled = await self.db.fetch_config_logs(invite.guild.id)

        if enabled:
            config = await self.db.fetch_logs(invite.guild.id)

            if config.invite_delete:
                channel_id = await self.db.fetch_channels_log(invite.guild.id)
                channel = self.bot.get_channel(channel_id)

                if channel:
                    embed = discord.Embed(title="Invite deleted",
                                          colour=self.emb_colour)

                    embed.add_field(name="Link",
                                    value=f"[{invite.id}]({invite.url})",
                                    inline=False)

                    embed.add_field(
                        name="Uses",
                        value=
                        f"{invite.uses if invite.uses else 0}/{'Unlimited' if not invite.max_uses or invite.max_uses == 0 else invite.max_uses}",
                        inline=False)

                    embed.add_field(
                        name="Temporary membership",
                        value="True" if invite.temporary else "False",
                        inline=False)

                    embed.set_footer(text="Wavy • https://wavybot.com",
                                     icon_url=self.bot.user.avatar_url)

                    await channel.send(embed=embed)

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
                description = "Invalid value provided. Please mention or put in a valid channel ID if applicable." \
                              "Else, please make sure you have put every value in correctly." \
                              "Not sure how to do this? Click [here](#)."

            elif isinstance(error.original, discord.Forbidden):
                description = "Wavy does not have the required permissions to do that. Please also make sure that you" \
                              " have put Wavy's role above all other roles. Not sure how to do this? Click [here](" \
                              "https://docs.wavybot.com). "

            else:
                description = f"`{error}`"

        if isinstance(error, commands.ChannelNotFound):
            description = "Please mention or put in a valid channel ID. Not sure how to do this? Click [here](" \
                          "#)."

        elif isinstance(error, commands.NSFWChannelRequired):
            description = "Please set the channel to be NSFW, or move to an NSFW channel. Not sure how to do this? " \
                          "Click [here](https://docs.wavybot.com)."

        elif isinstance(
                error,
            (exceptions.APIError, exceptions.NoChannelProvided,
             exceptions.NonExistantChannelError,
             exceptions.IncorrectChannelError,
             exceptions.NonExistantCategoryError, exceptions.NonExistantWarnID,
             exceptions.NonExistantMessageID)):
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
