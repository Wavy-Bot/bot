class Stats:
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


class Uptime:
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


class Minecraft:
    """
    Class that represents a Minecraft user.

    Takes the following arguments:
        name => The user's name.
        uuid => The user's UUID.
    """
    def __init__(self, name: str, uuid: str):
        self.name = name
        self.uuid = uuid


class Crafatar:
    """
    Class that represents a Crafatar API response.

    Takes the following arguments:
        url => The url of the render.
        uuid_class => The UUID class that was used to fetch said render.
    """
    def __init__(self, url: str, uuid_class: object):
        self.url = url
        self.uuid_class = uuid_class


class Reddit:
    """
    Class that represents a post in a subreddit.

    Takes the following arguments:
        subreddit => Subreddit the post is from.
        title => Post's title.
        link => Post's permalink.
        image_url => Post's image url.
        upvotes => Post's upvotes.
        comments => Post's comments.
    """
    def __init__(self, subreddit: str, title: str, link: str, image_url: str,
                 upvotes: int, comments: int):
        self.subreddit = subreddit
        self.title = title
        self.link = "https://reddit.com" + link
        self.image_url = image_url
        self.upvotes = upvotes
        self.comments = comments
