import os
import asyncio

import aiohttp
import aiohttp_cors

from discord.ext import commands, tasks
from datetime import datetime, timedelta
from aiohttp import web

app = web.Application()


class Api(commands.Cog):
    """API cog."""

    def __init__(self, bot):
        self.bot = bot
        self.guilds = {}

        self.runner = web.AppRunner(app)
        self.api_host = os.environ.get("API_HOST", "127.0.0.1")
        self.api_port = os.environ.get("API_PORT", 8080)
        app.add_routes(
            [
                web.get("/", self.root),
                web.get("/auth/login", self.auth_login),
                web.get("/auth/callback", self.auth_callback),
                web.get("/user/guilds", self.user_guilds),
                web.get("/user/guild/{guild_id}", self.user_guild),
            ]
        )
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "https://wavybot.com"
                if not os.environ["DISCORD_CLIENT_ID"]
                else "http://localhost:3000": aiohttp_cors.ResourceOptions(
                    allow_credentials=True
                )
            },
        )
        for route in list(app.router.routes()):
            cors.add(route)
        self.server = self.bot.loop.create_task(self.run_server())
        self.remove_expired_guilds.start()

    def cog_unload(self):
        """Runs when the cog is unloaded."""
        # Stop the API
        self.server.cancel()
        self.remove_expired_guilds.cancel()

    @tasks.loop(seconds=5.0)
    async def remove_expired_guilds(self):
        """Removes guilds that have expired."""
        for token, guild in self.guilds.copy().items():
            if guild["expires"] <= datetime.utcnow():
                del self.guilds[token]

    async def run_server(self):
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

    async def get_guilds(
        self, token: str, permission_level: int = 32
    ) -> list or web.Response:
        async with aiohttp.ClientSession() as cs:
            # Get the user's guilds
            user_guilds = self.guilds.get(token, None)
            if not user_guilds:
                resp = await cs.get(
                    "https://discord.com/api/users/@me/guilds",
                    headers={"Authorization": f"Bearer {token}"},
                )

                data = await resp.json()

                if type(data) is dict:
                    return web.json_response(
                        {
                            "status": 400,
                            "data": "We have been rate limited by Discord. Please try again later.",
                            "loggedIn": False,
                        },
                        status=400,
                    )

                self.guilds[token] = {
                    "guilds": data,
                    "expires": datetime.utcnow() + timedelta(minutes=2),
                }
                user_guilds = self.guilds[token]

            # Get the bot's guilds
            bot_guilds = [str(guild.id) for guild in self.bot.guilds]

            guilds = []

            # Go through the user's guilds
            # and if the user has manage_server permissions in said guild,
            # add whether or not the bot is in the guild
            # and then it to the list of guilds.
            for guild in user_guilds["guilds"]:
                if (guild["permissions"] & 0x20) == permission_level:
                    if guild["id"] in bot_guilds:
                        guild["has_bot"] = True
                    else:
                        guild["has_bot"] = False
                    guilds.append(guild)

            def sort_key(guild):
                return guild["has_bot"]

            guilds.sort(reverse=True, key=sort_key)

            return guilds

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

    async def auth_login(self, request: web.Request):
        """Redirects to Discord's login page."""
        client_id = (
            self.bot.application_id
            if not os.environ["DISCORD_CLIENT_ID"]
            else os.environ["DISCORD_CLIENT_ID"]
        )
        redirect_uri = os.environ["DISCORD_REDIRECT_URI"]
        scopes = "identify guilds"

        raise web.HTTPFound(
            f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code"
        )

    async def auth_callback(self, request: web.Request) -> web.Response:
        """Authentication callback."""
        code = request.query.get("code")

        if code:
            async with aiohttp.ClientSession() as cs:
                client_id = (
                    self.bot.application_id
                    if not os.environ["DISCORD_CLIENT_ID"]
                    else os.environ["DISCORD_CLIENT_ID"]
                )
                client_secret = os.environ["DISCORD_CLIENT_SECRET"]
                redirect_uri = os.environ["DISCORD_REDIRECT_URI"]

                payload = {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                }

                # Get the access token
                resp = await cs.post(
                    "https://discord.com/api/oauth2/token", data=payload
                )

                data = await resp.json()

                if data.get("error"):
                    return web.json_response(
                        {"status": 400, "data": data, "loggedIn": False}, status=400
                    )

                # Get the user's info
                u_resp = await cs.get(
                    "https://discord.com/api/oauth2/@me",
                    headers={"Authorization": f"Bearer {data['access_token']}"},
                )

                u_data = await u_resp.json()

                if u_data.get("error"):
                    return web.json_response(
                        {"status": 400, "data": data, "loggedIn": False}, status=400
                    )

                # Put the user's info in the same dict as the token
                data["user"] = u_data["user"]

                return web.json_response(
                    {"status": 200, "data": data, "loggedIn": True}
                )
        return web.json_response(
            {"status": 401, "data": {"error": "No code provided."}, "loggedIn": False},
            status=401,
        )

    async def user_guilds(self, request: web.Request) -> web.Response:
        """Gets the guilds where the current user has manage_server permissions in."""
        token = request.query.get("token")

        if token:
            guilds = await self.get_guilds(token=token)

            # If error, return the error
            if type(guilds) is web.Response:
                return guilds

            return web.json_response(
                {"status": 200, "data": {"guilds": guilds}, "loggedIn": True}
            )
        return web.json_response(
            {"status": 401, "data": {"error": "No token provided."}, "loggedIn": False},
            status=401,
        )

    async def user_guild(self, request: web.Request) -> web.Response:
        """Gets the guilds where the current user has manage_server permissions in."""
        token = request.query.get("token")
        guild_id = request.match_info["guild_id"]

        if token and guild_id:
            guilds = await self.get_guilds(token=token)

            # If error, return the error
            if type(guilds) is web.Response:
                return guilds

            if guild_id not in [guild["id"] for guild in guilds]:
                return web.json_response(
                    {
                        "status": 400,
                        "data": {
                            "error": "You do not have permission to manage this guild."
                        },
                        "loggedIn": True,
                    },
                    status=400,
                )

            guild = [i for i in guilds if i["id"] == guild_id][0]

            if not guild["has_bot"]:
                raise web.HTTPFound(f"https://invite.wavybot.com")

            bot_guild = self.bot.get_guild(int(guild["id"]))

            guild["members"] = bot_guild.member_count
            guild["channels"] = len(bot_guild.channels)
            guild["roles"] = len(bot_guild.roles)
            guild["boosts"] = len(bot_guild.premium_subscribers)
            guild["verification_level"] = bot_guild.verification_level

            return web.json_response(
                {"status": 200, "data": {"guild": guild}, "loggedIn": True}
            )
        return web.json_response(
            {
                "status": 401,
                "data": {"error": "No token or guild id provided."},
                "loggedIn": False,
            },
            status=401,
        )


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Api(bot))
