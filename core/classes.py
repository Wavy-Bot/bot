class Stats(object):
    """
    Class that represents the stats of the bot and the server it's running on.

    Takes the following arguments:
        cpu_usage => Total CPU usage. (in %)
        ram_usage => Total ram usage. (in MB)
        total_ram => Total RAM capacity. (in MB)
        disk_usage => Disk usage. (in GB)
        total_disk => Total disk capacity. (in GB)
        distro_name => Name of the distro.
        distro_version => Version of the distro.
        python_version => Python version.
        kernel_version => Version of the Linux kernel.
    """
    def __init__(self, cpu_usage: float, ram_usage: int, total_ram: int,
                 disk_usage: int, total_disk: int, distro_name: str,
                 distro_version: str, python_version: str,
                 kernel_version: str):
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.total_ram = total_ram
        self.disk_usage = disk_usage
        self.total_disk = total_disk
        self.distro_name = distro_name
        self.distro_version = distro_version
        self.python_version = python_version
        self.kernel_version = kernel_version


class Uptime(object):
    """
    Class that represents the bot's uptime.

    Takes the following arguments:
        weeks => Weeks the bot has been up.
        days => Days the bot has been up.
        hours => Hours the bot has been up.
        minutes => Minutes the bot has been up.
        seconds => Seconds the bot has been up.
    """
    def __init__(self, weeks, days, hours, minutes, seconds):
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
