import os
from abc import ABC

import discord
import asyncio
import uvloop
import sentry_sdk

from wavy.utils import database
from discord.ext import commands
from dotenv import load_dotenv

__VERSION__ = "1.2.0"

load_dotenv()

sentry_sdk.init(
    os.environ["SENTRY_URL"],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


async def run(event_loop: uvloop.Loop) -> None:
    """
    Runs the bot.

    Parameters:
        event_loop => The event loop to use.

    >>> import wavy
    >>> import asyncio
    >>> import uvloop
    >>> loop = uvloop.new_event_loop()
    >>> asyncio.set_event_loop(loop)
    >>> loop.run_until_complete(wavy.run(loop))
    """
    asyncio.set_event_loop(event_loop)

    admin_guild = int(os.environ["ADMIN_GUILD"])
    db = database.Database()
    bot = Wavy(event_loop=event_loop, db=db)

    @commands.guild_only()
    @bot.slash_command(guild_ids=[admin_guild])
    @commands.is_owner()
    async def load(ctx, extension: str):
        """Loads a cog."""
        bot.load_extension(f"wavy.cogs.{extension}")
        await ctx.respond(f"Loaded `{extension}`.")

    @commands.guild_only()
    @bot.slash_command(guild_ids=[admin_guild])
    @commands.is_owner()
    async def unload(ctx, extension: str):
        """Unloads a cog."""
        bot.unload_extension(f"wavy.cogs.{extension}")
        await ctx.respond(f"Unloaded `{extension}`.")

    @commands.guild_only()
    @bot.slash_command(guild_ids=[admin_guild])
    @commands.is_owner()
    async def reload(ctx, extension: str):
        """Reloads a cog."""
        bot.reload_extension(f"wavy.cogs.{extension}")
        await ctx.respond(f"Reloaded `{extension}`.")

    try:
        await bot.start(os.environ["TOKEN"])
    except KeyboardInterrupt:
        await bot.close()


class Wavy(discord.AutoShardedBot, ABC):
    """The blazing-fast Discord bot.

    Parameters:
        event_loop => The event loop to use.
        db => The database to use.
    """

    def __init__(self, event_loop, db):
        self.db = db

        # Although your linter will probably say something along the lines of
        # 'Intents' object attribute 'members' is read-only, this works.
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            intents=intents,
            status=discord.Status.dnd,
            activity=discord.Game("Starting..."),
            help_command=None,
            loop=event_loop,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=True, replied_user=True
            ),
            chunk_guilds_at_startup=False,
        )

        # Loop through the cogs and load them unless the file name starts with "_".
        for cog in os.listdir("wavy/cogs"):
            if cog.endswith(".py") and not cog.startswith("_"):
                try:
                    cog = f"wavy.cogs.{cog.replace('.py', '')}"
                    self.load_extension(cog)
                except Exception as e:
                    print(f"{cog} cannot be loaded.")
                    raise e
