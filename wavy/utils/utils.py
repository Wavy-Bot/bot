import platform
import random
import json

import discord
import psutil

from . import classes
from datetime import datetime

LAUNCH_TIME = datetime.utcnow()


async def server_stats():
    """Gets the current server stats."""
    cpu_usage = psutil.cpu_percent()
    ram_usage = round(psutil.virtual_memory().used / (1024.0 ** 3), 1)
    total_ram = round(psutil.virtual_memory().total / (1024.0 ** 3), 1)
    disk_usage = round(psutil.disk_usage("/").used / (1024.0 ** 3), 1)
    total_disk = round(psutil.disk_usage("/").total / (1024.0 ** 3), 1)
    python_version = platform.python_version()
    pycord_version = discord.__version__

    stats = classes.Stats(
        cpu_usage=cpu_usage,
        ram_usage=ram_usage,
        total_ram=total_ram,
        disk_usage=disk_usage,
        total_disk=total_disk,
        python_version=python_version,
        pycord_version=pycord_version,
    )

    return stats


async def uptime():
    """Gets the bot's uptime."""
    # TODO(Robert): This really isn't the best way to do this,
    #               so I will have to improve this later.

    delta_uptime = datetime.utcnow() - LAUNCH_TIME
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    uptime_class = classes.Uptime(
        weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
    )

    # Return class

    return uptime_class


async def status_message():
    """Picks a status message from the list."""
    with open("wavy/messages.json", "r") as f:
        data = json.load(f)
        status_list = data["status"]

    message = random.choice(status_list)

    return message


async def loading_message():
    """Picks a random loading message from the list."""
    with open("wavy/messages.json", "r") as f:
        data = json.load(f)
        loading_list = data["loading"]

    message = random.choice(loading_list)

    return message
