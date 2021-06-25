from discord.ext import commands


class NSFWChannelRequired(commands.CommandError):
    """Error raised when channel isn't an NSFW channel."""


class APIError(commands.CommandError):
    """Error raised when an API returns an error."""
    def __init__(self,
                 message="The API returned an error. Please try again later."):
        self.message = message
        super().__init__(self.message)
