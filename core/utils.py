import platform

import psutil
import distro

from core import classes
from datetime import datetime

launch_time = datetime.utcnow()


async def fetch_server_stats():
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


async def fetch_uptime():
    """Gets the bot's uptime."""
    # TODO(Robert): This really isn't the best way to do this,
    #               so I will have to improve this later.

    delta_uptime = datetime.utcnow() - launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    uptime = classes.Uptime(weeks=weeks,
                            days=days,
                            hours=hours,
                            minutes=minutes,
                            seconds=seconds)

    # Return class

    return uptime
