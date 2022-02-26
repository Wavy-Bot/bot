import os
from abc import ABC

import discord
import asyncio
import uvloop
import sentry_sdk

from wavy.utils import database, utils
from discord.ext import commands
from discord.commands import permissions
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from uvicorn import Config, Server

__VERSION__ = "0.0.1a"  # I keep forgetting to update this, whoops.

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
    Runs the bot and its API.

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

    # TODO(Robert): Finish this, the API and the website.

    # The (quite messy) API stuff starts here,
    # I did not really have a better place to put this due to the fact that FastAPI doesn't really work in a cog,
    # and I have no idea how to expose the bot variable to a different file.

    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    config = Config(app=app, loop=event_loop, access_log=False, port=31088)
    server = Server(config)

    @app.get("/")
    async def root() -> JSONResponse:
        """API root."""
        return JSONResponse(
            {
                "status": 200,
                "data": {
                    "name": "Wavy API",
                    "description": "Wavy's API.",
                    "author": "Robert S & Contributors",
                    "version": __VERSION__,
                },
            }
        )

    @app.get("/guilds")
    async def guilds(request: Request) -> JSONResponse:
        """Returns a list of guilds the bot is in."""
        await utils.validate_api_key(request=request)
        return JSONResponse(
            {"status": 200, "data": [str(guild.id) for guild in bot.guilds]}
        )

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

    bot.loop.create_task(server.serve())

    try:
        await bot.start(os.environ["TOKEN"])
    except KeyboardInterrupt:
        await bot.close()


class Wavy(commands.AutoShardedBot, ABC):
    """The blazing-fast Discord bot."""

    def __init__(self, event_loop, db):
        self.db = db

        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("%"),
            case_insensitive=True,
            intents=intents,
            status=discord.Status.dnd,
            activity=discord.Game("Starting..."),
            help_command=None,
            loop=event_loop,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=True, replied_user=True
            ),
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
