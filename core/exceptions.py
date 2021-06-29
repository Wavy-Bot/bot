from discord.ext import commands


class APIError(commands.CommandError):
    """Error raised when an API returns an error."""
    def __init__(self,
                 message="The API returned an error. Please try again later."):
        self.message = message
        super().__init__(self.message)


class NoChannelProvided(commands.CommandError):
    """Error raised when no suitable voice channel was supplied."""
    def __init__(
        self,
        message="You must be in a voice channel or provide one to connect to."
    ):
        self.message = message
        super().__init__(self.message)


class IncorrectChannelError(commands.CommandError):
    """Error raised when commands are issued outside of the players session channel."""
    def __init__(
            self,
            message="You must be in a different text channel for this session.."
    ):
        self.message = message
        super().__init__(self.message)
