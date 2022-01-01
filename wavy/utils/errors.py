from discord.ext import commands


class IncorrectChannelError(commands.CommandError):
    """Error raised when commands are issued outside the players' session channel."""

    def __init__(self, message_author, channel):
        self.message = f"{message_author}, you must be in {channel} for this session."
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


class NonExistantCategoryError(commands.CommandError):
    """Error raised when a category doesn't exist."""

    def __init__(self, category: str):
        self.message = f"The category `{category}` does not exist."
        super().__init__(self.message)
