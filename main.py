import os

import discord
import asyncio
import sentry_sdk

from core import database
import core.request as core_request
from discord.ext import commands
from sanic import Sanic
from sanic.response import json

SENTRY_URL = os.getenv("SENTRY_URL")

sentry_sdk.init(SENTRY_URL, traces_sample_rate=1.0)


async def run():
    """Starts the bot."""
    token = os.getenv("TOKEN")
    secret = os.getenv("API_SECRET")
    db = database.Database()
    bot = Wavy(db=db)
    app = Sanic(__name__)
    emb_colour = int(os.getenv("COLOUR"), 16)

    # NOTE(Robert): A little explanation of all this crap, the commands are here because
    #               in the class the commands wouldn't load, but outside they would +
    #               I don't want these commands in a class/cog since I don't want them
    #               to be unloadable.

    @bot.command(hidden=True)
    @commands.is_owner()
    async def load(ctx, extension):
        """Loads a cog."""
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Loaded `{extension}`.")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def unload(ctx, extension):
        """Unloads a cog."""
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"Unloaded `{extension}`.")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def reload(ctx, extension):
        """Reloads a cog."""
        bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f"Reloaded `{extension}`.")

    # NOTE(Robert): This is here because if I were to put it in a cog it would only apply for said cog,
    #               not globally.

    @bot.event
    async def on_message(message):
        """Called when a message is created and sent."""
        if isinstance(message.channel,
                      discord.DMChannel) and not message.author.bot:
            async with message.channel.typing():
                res = await core_request.cleverbot(message.content,
                                                   message.author.id)

                embed = discord.Embed(title="Cleverbot",
                                      description=res,
                                      colour=emb_colour)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=bot.user.avatar_url)

                await message.channel.send(embed=embed)
        await bot.process_commands(message)

    @app.route("/")
    async def index(request):
        """Index page."""
        return json({"message": "Welcome to Wavy's API."})

    @app.route("/fetch/roles")
    async def fetch_roles(request):
        """Fetches all roles of the specified server."""
        try:
            guild_id = request.json['guild_id']
            guild_id = int(guild_id)
        except TypeError:
            return json({"message": "No guild ID was provided."}, status=400)

        if request.token != secret:
            return json(
                {
                    "message":
                    "The API key provided did not match the key that was set."
                },
                status=401)

        guild = bot.get_guild(guild_id)

        if not guild:
            return json({"message": "The guild ID provided was invalid."},
                        status=400)

        role_list = []
        roles = guild.roles
        roles.pop(0)  # Remove @everyone role

        for i in roles:
            role_list.append({"id": i.id, "name": i.name})

        return json(role_list)

    @app.route("/fetch/channels")
    async def fetch_channels(request):
        """Fetches all text channels of the specified server."""
        try:
            guild_id = request.json['guild_id']
            guild_id = int(guild_id)
        except TypeError:
            return json({"message": "No guild ID was provided."}, status=400)

        if request.token != secret:
            return json(
                {
                    "message":
                    "The API key provided did not match the key that was set."
                },
                status=401)

        guild = bot.get_guild(guild_id)

        if not guild:
            return json({"message": "The guild ID provided was invalid."},
                        status=400)

        channel_list = []
        channels = guild.text_channels

        for i in channels:
            channel_list.append({"id": i.id, "name": i.name})

        return json(channel_list)

    try:
        bot.loop.create_task(
            app.create_server(host="127.0.0.1",
                              port=31088,
                              debug=False,
                              return_asyncio_server=True))

        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()


class Wavy(commands.AutoShardedBot):
    """
    The blazing-fast Discord bot - now as a class for as little as $69420.99!
    (this is a joke if you haven't noticed already ^)
    """
    def __init__(self, db):
        self.db = db

        intents = discord.Intents.default()
        intents.members = True

        super().__init__(command_prefix=self.__fetch_prefix,
                         case_insensitive=True,
                         intents=intents,
                         status=discord.Status.online,
                         activity=discord.Game('https://wavybot.com'),
                         help_command=None)

        for cog in os.listdir("./cogs"):
            if cog.endswith(".py") and not cog.startswith("_"):
                try:
                    cog = f"cogs.{cog.replace('.py', '')}"
                    self.load_extension(cog)
                except Exception as e:
                    print(f"{cog} cannot be loaded.")
                    raise e

    async def __fetch_prefix(self, botobject, message):
        """Fetches the bot's prefix from the database."""
        if not message.guild:
            return commands.when_mentioned_or("%")(botobject, message)

        prefix = await self.db.fetch_config_prefix(message.guild.id)

        if not prefix:
            prefix = "%"

        return commands.when_mentioned_or(prefix)(botobject, message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
