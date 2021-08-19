import platform
import random
import re

import psutil
import distro

from core import classes
from datetime import datetime, timedelta

LAUNCH_TIME = datetime.utcnow()


async def server_stats():
    """Gets the current server stats."""
    cpu_usage = psutil.cpu_percent()
    ram_usage = round(psutil.virtual_memory().used / (1024.0**2))
    total_ram = round(psutil.virtual_memory().total / (1024.0**2))
    disk_usage = round(psutil.disk_usage('/').used / (1024.0**3))
    total_disk = round(psutil.disk_usage('/').total / (1024.0**3))
    distro_name = distro.name()
    distro_version = distro.version()
    python_version = platform.python_version()
    kernel_version = platform.release()

    stats = classes.Stats(cpu_usage=cpu_usage,
                          ram_usage=ram_usage,
                          total_ram=total_ram,
                          disk_usage=disk_usage,
                          total_disk=total_disk,
                          distro_name=distro_name,
                          distro_version=distro_version,
                          python_version=python_version,
                          kernel_version=kernel_version)

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

    uptime_class = classes.Uptime(weeks=weeks,
                                  days=days,
                                  hours=hours,
                                  minutes=minutes,
                                  seconds=seconds)

    # Return class

    return uptime_class


async def loading_text():
    """Picks a random loading text from a list."""
    loading_list = [
        "Writing poem...", "Creating masterpiece...", "Generating image...",
        "Getting coffee...", "Procrastinating...", "Burning servers...",
        "Getting dem memes...", "[put something funny here]",
        "Dabbing on dem haters...", "Added printing request to the queue...",
        "Am I supposed to do something?", "Failing life...",
        "Convincing AI not to turn evil..", "How did you get here?",
        "Computing the secret to life, the universe, and everything.",
        "When nothing is going right, go left!!...",
        "Never steal. The government hates competition....",
        "Dividing by zero...",
        "If I’m not back in five minutes, just wait longer.",
        "Proving P=NP...", "Laughing at your pictures-i mean, loading...",
        "Let's hope it's worth the wait",
        "Whatever you do, don't look behind you...",
        "Please wait... Consulting the manual...",
        "Deleting the System32 folder...",
        "When was the last time you dusted around here?",
        "Optimizing the optimizer...", "Building a wall...",
        "Updating Updater...", "Downloading Downloader...",
        "Debugging Debugger...", "Patience! This is difficult, you know...",
        "Grabbing extra minions...", "Waking up the minions...",
        "We're working very Hard .... Really",
        "You are number 2843684714 in the queue",
        "TODO: Insert elevator music", "Still faster than Windows update",
        "Reading Terms and Conditions for you.",
        "Shovelling coal into the server", "Alt-F4 speeds things up.",
        "Downloading more RAM..", "Updating to Windows Vista...",
        "Mining some bitcoins...", "Feel free to spin in your chair",
        "Loading funny message...", "BRB, working on my side project",
        "@todo Insert witty loading message", "Winter is coming...",
        "Please wait while the intern refills his coffee.",
        "Looking for sense of humour, please hold on.",
        "Cracking military-grade encryption...",
        "We’re going to need a bigger boat.", "I'm going to walk the dog.",
        "Well, this is embarrassing.",
        "I think I am, therefore, I am. I think.", "Granting wishes...",
        "Where did all the internets go", "I swear it's almost done.",
        "Should have used a compiled language...",
        "What do you call 8 Hobbits? A Hobbyte.",
        "We're making you a cookie...", "Warning: Don't set yourself on fire.",
        "Do you come here often?", "Counting backwards from Infinity...",
        "Are we there yet?",
        "Testing on Timmy... We're going to need another Timmy.",
        "Why don't you order a sandwich?",
        "Don't worry - a few bits tried to escape, but we caught them",
        "Someone please teach Hypixel how to make an api..."
    ]

    text = random.choice(loading_list)

    return text


async def progress_bar():
    """Creates a progress bar."""
    percentage = (random.randint(0, 100))

    bar = f"{int(round(percentage / 10, 0)) * '⬜'}{(10 - int(round(percentage / 10, 0))) * '⬛'}"

    bar_class = classes.ProgressBar(bar=bar, percentage=percentage)

    return bar_class


async def convert_time_into_timedelta(time: str):
    """Converts time into a timedelta."""
    time_formats = ["s", "m", "h", "d", "w"]
    time_format = re.sub("[^a-zA-Z]*", "", time)[0]

    if time_format not in time_formats:
        return

    time = int(re.sub("[^0-9]", "", time))

    if time_format == "m":
        time = time * 60
    elif time_format == "h":
        time = time * 3600
    elif time_format == "d":
        time = time * 86400
    elif time_format == "w":
        time = time * 604800

    time_delta = datetime.utcnow() + timedelta(seconds=time)

    time_class = classes.Time(time=time, timedelta=time_delta)

    return time_class


async def convert_time_into_epoch(time: str):
    """Converts time into a unix epoch timestamp."""
    time = await convert_time_into_timedelta(time)

    if not time:
        return

    timestamp = int(time.timedelta.timestamp())

    time_class = classes.Time(time=time.time,
                              timedelta=time.timedelta,
                              epoch=timestamp)

    return time_class