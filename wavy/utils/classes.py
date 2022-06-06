from dataclasses import dataclass


@dataclass
class Stats:
    """
    Class that represents the stats of the bot and the server it's running on.

    Takes the following arguments:
        cpu_usage => Total CPU usage. (in %)
        ram_usage => Total ram usage. (in GB)
        total_ram => Total RAM capacity. (in GB)
        disk_usage => Disk usage. (in GB)
        total_disk => Total disk capacity. (in GB)
        python_version => Python version.
        pycord_version => Pycord version.
    """

    cpu_usage: float
    ram_usage: float
    total_ram: float
    disk_usage: float
    total_disk: float
    python_version: str
    pycord_version: str


@dataclass
class Uptime:
    """
    Class that represents the uptime of the bot.

    Takes the following arguments:
        weeks => Weeks the bot has been up.
        days => Days the bot has been up.
        hours => Hours the bot has been up.
        minutes => Minutes the bot has been up.
        seconds => Seconds the bot has been up.
    """

    weeks: int
    days: int
    hours: int
    minutes: int
    seconds: int


@dataclass
class Warn:
    """
    Class that represents a warn.

    Takes the following arguments:
        server_id => ID of the Discord server.
        member_id => ID of the server member.
        id => ID of the warn.
        reason => Reason for the warn.
    """

    server_id: int
    member_id: int
    id: str
    reason: str


@dataclass
class RedditPost:
    """
    Class that represents a reddit post.

    Takes the following arguments:
        subreddit => The subreddit the post came from.
        title => Title of the post.
        over_18 => Whether the post is NSFW.
        url => URL of the post.
        image => Image URL of the post.
        ups => Upvotes of the post.
        comments => Number of comments on the post.
    """

    subreddit: str
    title: str
    over_18: bool
    url: str
    image: str
    ups: int
    comments: int
