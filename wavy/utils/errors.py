from discord.ext import commands


class IncorrectChannel(commands.CommandError):
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


class NonExistantCategory(commands.CommandError):
    """Error raised when a category doesn't exist."""

    def __init__(self, category: str):
        self.message = f"The category `{category}` does not exist."
        super().__init__(self.message)


class PlayerNotConnected(commands.CommandError):
    """Error raised when a player is not connected."""

    def __init__(self):
        self.message = "**:x: The bot is not currently playing anything.**"
        super().__init__(self.message)


class SongNotFound(commands.CommandError):
    """Error raised when a song could not be connected."""

    def __init__(self):
        self.message = "**:x: No songs were found with that query. Please try again.**"
        super().__init__(self.message)


class NoVoiceChannel(commands.CommandError):
    """Error raised when a player is not connected."""

    def __init__(self):
        self.message = "**:x: You must be in a voice channel to play music.**"
        super().__init__(self.message)
