from discord.ext import commands
from discord import Member, VoiceChannel


class IncorrectChannel(commands.CommandError):
    """Error raised when commands are issued outside the players' session channel."""

    def __init__(self, message_author: Member, channel: VoiceChannel):
        self.message = f"{message_author.mention}, you must be in {channel.mention} for this session."
        super().__init__(self.message)


class NoChannelProvided(commands.CommandError):
    """Error raised when no suitable channel was supplied."""

    def __init__(self, channel_type: str):
        if channel_type == "voice":
            self.message = (
                "You must be in a voice channel or provide one to connect to."
            )
        else:
            self.message = "You must provide a valid text channel."
        super().__init__(self.message)


class NonExistantCommand(commands.CommandError):
    """Error raised when the requested command doesn't exist."""

    def __init__(self, command: str):
        self.message = f"The command `{command}` does not exist."
        super().__init__(self.message)


class PlayerNotConnected(commands.CommandError):
    """Error raised when a player is not connected."""

    def __init__(self):
        self.message = "The bot is not currently playing anything."
        super().__init__(self.message)


class SongNotFound(commands.CommandError):
    """Error raised when a song could not be connected."""

    def __init__(self):
        self.message = "No songs were found with that query. Please try again."
        super().__init__(self.message)


class Timeout(commands.CommandError):
    """Error raised when a user is(n't) already timed out."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Bot(commands.CommandError):
    """Error raised when a member is a bot."""

    def __init__(self, message: str = "Member is a bot."):
        self.message = message
        super().__init__(self.message)


class WarnNotFound(commands.CommandError):
    """Error raised when a member is a bot."""

    def __init__(self, warn_id: str):
        self.message = f"No warning with ID `{warn_id}` found."
        super().__init__(self.message)
