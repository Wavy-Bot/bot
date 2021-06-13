import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="%",
                   case_insensitive=True,
                   intents=intents,
                   status=discord.Status.online,
                   activity=discord.Game('https://wavybot.com'))


@bot.event
async def on_ready():
    """Called when the bot is done preparing the data received from Discord."""
    print(f'Logged in as\n{bot.user.name}\n{bot.user.id}')


for cog in os.listdir("./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded.")
            raise e

bot.run(TOKEN)
