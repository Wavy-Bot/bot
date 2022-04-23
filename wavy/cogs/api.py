import os
import asyncio

from wavy.utils import utils

from discord.ext import commands
from aiohttp import web

app = web.Application()


class Api(commands.Cog):
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

        self.runner = web.AppRunner(app)
        self.api_host = os.environ.get("API_HOST", "0.0.0.0")
        self.api_port = os.environ.get("API_PORT", 8080)
        app.add_routes([web.get("/", self.root), web.get("/guilds", self.guilds)])
        self.api = self.bot.loop.create_task(self.run_api())

    def cog_unload(self):
        """Runs when the cog is unloaded."""
        # Stop the API
        self.api.cancel()

    async def run_api(self):
        """Runs the API."""
        try:
            # Wait until the bot is ready
            print("Waiting for bot to start before starting API...")
            await self.bot.wait_until_ready()

            # Start the API
            print("Starting API...")
            await self.runner.setup()
            site = web.TCPSite(self.runner, self.api_host, self.api_port)
            await site.start()
            print("API started.")
        except asyncio.CancelledError:
            # Clean up runner
            await self.runner.cleanup()
            print("API stopped.")

    @staticmethod
    async def root(request: web.Request) -> web.Response:
        """API root."""
        return web.json_response(
            {
                "status": 200,
                "data": {
                    "name": "Wavy API",
                    "description": "Wavy's API.",
                    "author": "Robert S & Contributors",
                },
            }
        )

    async def guilds(self, request: web.Request) -> web.Response:
        """Returns a list of guilds the bot is in."""
        if not await utils.validate_api_key(headers=request.headers):
            raise web.HTTPForbidden
        return web.json_response(
            {"status": 200, "data": [str(guild.id) for guild in self.bot.guilds]}
        )


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Api(bot))
