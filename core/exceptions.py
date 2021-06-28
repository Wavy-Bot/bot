from discord.ext import commands


class NSFWChannelRequired(commands.CommandError):
    """Error raised when channel isn't an NSFW channel."""


class APIError(commands.CommandError):
    """Error raised when an API returns an error."""
    def __init__(self,
                 message="The API returned an error. Please try again later."):
        self.message = message
        super().__init__(self.message)


class NoChannelProvided(commands.CommandError):
    """Error raised when no suitable voice channel was supplied."""


class IncorrectChannelError(commands.CommandError):
    """Error raised when commands are issued outside of the players session channel."""
