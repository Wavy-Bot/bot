import os

import discord
import asyncio

from core import database, request
from discord.ext import commands


async def run():
    """Starts the bot."""
    token = os.getenv("TOKEN")
    db = database.Database()
    bot = Wavy(db=db)
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
        if isinstance(message.channel,
                      discord.DMChannel) and not message.author.bot:
            async with message.channel.typing():
                res = await request.cleverbot(message.content,
                                              message.author.id)

                embed = discord.Embed(title="Cleverbot",
                                      description=res,
                                      colour=emb_colour)

                embed.set_footer(text="Wavy • https://wavybot.com",
                                 icon_url=bot.user.avatar_url)

                await message.channel.send(embed=embed)
        await bot.process_commands(message)

    try:
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
