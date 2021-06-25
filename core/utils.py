import platform
import random

import psutil
import distro

from core import classes
from datetime import datetime

launch_time = datetime.utcnow()


async def server_stats():
    """Gets the current server stats."""
    # TODO(Robert): This really isn't the best way to do this,
    #               so I will have to improve this later.

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

    delta_uptime = datetime.utcnow() - launch_time
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
    # NOTE(Robert) This is an absolute warcrime
    #              and I don't recommend doing
    #              it like this.
    percentage = (random.randint(0, 100))

    if percentage == 0:
        bar = bar = "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"
    elif percentage <= 10:
        bar = "⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛"
    elif percentage <= 20:
        bar = "⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛"
    elif percentage <= 30:
        bar = "⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛"
    elif percentage <= 40:
        bar = "⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛"
    elif percentage <= 50:
        bar = "⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛"
    elif percentage <= 60:
        bar = "⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛"
    elif percentage <= 70:
        bar = "⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛"
    elif percentage <= 80:
        bar = "⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛"
    elif percentage <= 90:
        bar = "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛"
    elif percentage <= 100:
        bar = "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜"

    bar_class = classes.ProgressBar(bar=bar, percentage=percentage)

    return bar_class
