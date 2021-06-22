import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("%"),
                              case_insensitive=True,
                              intents=intents,
                              status=discord.Status.online,
                              activity=discord.Game('https://wavybot.com'))


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


for cog in os.listdir("./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded.")
            raise e

bot.run(TOKEN)
