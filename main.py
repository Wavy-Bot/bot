import os

import discord
import asyncio
import uvloop

from dotenv import load_dotenv

# Only set this to True if this is a production environment.
production = False

load_dotenv(".env.production" if production else ".env.development")


async def run(event_loop: uvloop.Loop) -> None:
    """Runs the bot."""
    bot = Wavy(event_loop)

    try:
        await bot.start(os.environ["TOKEN"])
    except KeyboardInterrupt:
        await bot.logout()


class Wavy(discord.Client):
    """The blazing-fast Discord bot."""

    def __init__(self, event_loop):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix="%",
            case_insensitive=True,
            intents=intents,
            status=discord.Status.online,
            activity=discord.Game("https://wavybot.com"),
            help_command=None,
            loop=event_loop,
        )

    async def on_ready(self) -> print:
        print(f"Logged in as\n{self.user.name}\n{self.user.id}")


if __name__ == "__main__":
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(loop))
