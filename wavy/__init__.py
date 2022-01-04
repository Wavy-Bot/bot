import os

import discord
import uvloop

from wavy.utils import database
from discord.ext import commands
from discord.commands import permissions
from dotenv import load_dotenv

__VERSION__ = "0.0.1"

load_dotenv()


async def run(event_loop: uvloop.Loop) -> None:
    """Runs the bot."""
    admin_guild = int(os.environ["ADMIN_GUILD"])
    db = database.Database()
    bot = Wavy(event_loop=event_loop, db=db)

    @bot.slash_command(guild_ids=[admin_guild])
    @permissions.is_owner()
    async def load(ctx, extension: str):
        """Loads a cog."""
        bot.load_extension(f"wavy.cogs.{extension}")
        await ctx.respond(f"Loaded `{extension}`.")

    @bot.slash_command(guild_ids=[admin_guild])
    @permissions.is_owner()
    async def unload(ctx, extension: str):
        """Unloads a cog."""
        bot.unload_extension(f"wavy.cogs.{extension}")
        await ctx.respond(f"Unloaded `{extension}`.")

    @bot.slash_command(guild_ids=[admin_guild])
    @permissions.is_owner()
    async def reload(ctx, extension: str):
        """Reloads a cog."""
        bot.reload_extension(f"wavy.cogs.{extension}")
        await ctx.respond(f"Reloaded `{extension}`.")

    try:
        await bot.start(os.environ["TOKEN"])
    except KeyboardInterrupt:
        await bot.logout()


class Wavy(commands.AutoShardedBot):
    """The blazing-fast Discord bot."""

    def __init__(self, event_loop, db):
        self.db = db

        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("%"),
            case_insensitive=True,
            intents=intents,
            status=discord.Status.online,
            activity=discord.Game("https://wavybot.com"),
            help_command=None,
            loop=event_loop,
        )

        for cog in os.listdir("wavy/cogs"):
            if cog.endswith(".py") and not cog.startswith("_"):
                try:
                    cog = f"wavy.cogs.{cog.replace('.py', '')}"
                    self.load_extension(cog)
                except Exception as e:
                    print(f"{cog} cannot be loaded.")
                    raise e