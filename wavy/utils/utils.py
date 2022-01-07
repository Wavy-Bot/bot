import platform
import random
import json
import re

import discord
import psutil

from . import classes
from datetime import datetime, timedelta

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


async def interaction(interaction_type: str):
    """Picks a random interaction from the list."""
    with open("wavy/interactions.json", "r") as f:
        data = json.load(f)
        interaction_list = data[interaction_type]

    image = random.choice(interaction_list)

    return image


async def fetch_thumbnail(identifier: str):
    """Fetches a thumbnail from a Youtube ID."""
    ytid = identifier if re.match(r"^[a-zA-Z0-9_-]{11}$", identifier) else None

    if ytid:
        thumb = f"https://img.youtube.com/vi/{ytid}/hqdefault.jpg"
    else:
        thumb = None

    return thumb


async def chop_microseconds(delta):
    """Removes microseconds from a timedelta."""
    return delta - timedelta(microseconds=delta.microseconds)


async def convert_time_into_timedelta(time: int, unit: str):
    """Converts time into a timedelta."""
    # Get first letter of unit.
    time_format = re.sub("[^a-zA-Z]*", "", unit)[0]

    # Convert to proper units.
    if time_format == "M":
        time = time * 60
    elif time_format == "H":
        time = time * 3600
    elif time_format == "D":
        time = time * 86400
    elif time_format == "W":
        time = time * 604800

    time_delta = timedelta(seconds=time)

    return time_delta


async def progress_bar(percentage: int):
    """Creates a progress bar."""

    bar = f"{int(round(percentage / 10, 0)) * '⬜'}{(10 - int(round(percentage / 10, 0))) * '⬛'}"

    return bar
