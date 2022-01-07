import os

import discord

from ..utils import utils, errors, database, requests
from discord.ext import commands, tasks


class Events(commands.Cog):
    """Events"""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.db = database.Database()
        self.change_status.start()
        self.update_memes.start()

    def cog_unload(self):
        """Runs when the cog gets unloaded."""
        self.change_status.cancel()
        self.update_memes.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the client is done preparing the data received from Discord."""
        print(f"Logged in as\n{self.bot.user.name}\n{self.bot.user.id}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild."""
        guild_channel = guild.text_channels[0]
        message_channel = self.bot.get_channel(guild_channel.id)

        message = (
            "**Hi there, I'm Wavy** - The blazing-fast Discord bot.\n"
            "- You can see a list of commands by typing `/help`\n"
            "- You can set me up by going to <https://wavybot.com>\n"
            "- If you need help, feel free to join my support server over at https://discord.wavybot.com"
        )

        try:
            await message_channel.send(message)
        except discord.Forbidden:
            return

    @tasks.loop(hours=1)
    async def change_status(self):
        """Changes the bot's status every hour."""
        status_message = await utils.status_message()

        await self.bot.change_presence(
            activity=discord.Game(status_message),
            status=discord.Status.online,
        )

    @tasks.loop(minutes=15)
    async def update_memes(self):
        """Updates the memes every 15 minutes."""
        await requests.update_memes()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Called when a message is deleted."""
        if (
            not isinstance(message.channel, discord.DMChannel)
            and not message.author.bot
        ):
            await self.db.set_snipe(
                server_id=message.guild.id,
                channel_id=message.channel.id,
                member_id=message.author.id,
                content=message.content,
                attachments=[i.url for i in message.attachments],
            )

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        """Called when a command raises an error."""
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.NoPrivateMessage):
            return

        if isinstance(error, commands.CommandOnCooldown):
            description = (
                f"You can use this command again in {error.retry_after} seconds."
            )
        elif isinstance(
            error,
            (
                errors.IncorrectChannel,
                errors.NoChannelProvided,
                errors.NonExistantCategory,
                errors.PlayerNotConnected,
            ),
        ):
            description = error
        elif hasattr(error, "original"):
            if isinstance(error.original, commands.MissingPermissions):
                permission_string = ""

                for i in error.original.missing_permissions:
                    permission_string += f"• `{i}`\n"

                description = (
                    f"You don't have permission to execute `{ctx.command.name}`. "
                    f"You need the following permissions:\n{permission_string}"
                )
            elif isinstance(error.original, commands.BotMissingPermissions):
                permission_string = ""

                for i in error.original.missing_permissions:
                    permission_string += f"• `{i}`\n"

                description = (
                    f"I don't have permission to execute `{ctx.command.name}`. "
                    f"I need the following permissions:\n{permission_string}"
                )
            elif isinstance(error.original, commands.NSFWChannelRequired):
                description = "This post can only be viewed in an NSFW channel."
            else:
                description = error.original
        else:
            description = f"`{error}`"

        embed = discord.Embed(
            title="Error", description=f"**:x: {description}**", colour=0xE73C24
        )

        embed.set_footer(
            text="Wavy • https://wavybot.com", icon_url=self.bot.user.display_avatar.url
        )

        await ctx.respond(embed=embed)

        raise error


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Events(bot))
