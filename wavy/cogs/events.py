import os

import discord

from ..utils import utils
from discord.ext import commands, tasks


class Events(commands.Cog):
    """Events"""

    def __init__(self, bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.change_status.start()

    def cog_unload(self):
        """Runs when the cog gets unloaded."""
        self.change_status.cancel()

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

    # TODO(Robert): Error handler.


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Events(bot))
