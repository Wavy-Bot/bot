import os

import discord

from discord.ext import commands
from core import exceptions

ERR_COLOUR = int(os.getenv("ERR_COLOUR"), 16)


class Events(commands.Cog):
    """Class that contains all the bot events."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is done preparing the data received from Discord."""
        print(f'Logged in as\n{self.bot.user.name}\n{self.bot.user.id}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild."""
        guild_channel = guild.text_channels[0]
        message_channel = self.bot.get_channel(guild_channel.id)

        message = "**Hi there, I'm Wavy** - The blazingly fast Discord bot.\n" \
                  "- My prefix is `%`\n" \
                  "- You can see a list of commands by typing `%help`\n" \
                  "- You can set me up by going to <https://dash.wavybot.com>\n" \
                  "- If you need help, feel free to join my support server over at https://discord.wavybot.com"

        try:
            await message_channel.send(message)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Called when an exception was called."""
        # TODO(Robert): Set the correct documentation URLs.
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
                              colour=ERR_COLOUR)

        embed.set_footer(text="Wavy • https://wavybot.com",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    """Add cog to bot"""
    bot.add_cog(Events(bot))
