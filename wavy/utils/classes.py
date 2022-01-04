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
class SpotifyTrack:
    """
    Class that represents a Spotify track.

    Takes the following arguments:
        name => Track name.
        artist => Artist.
        image => Image URL.
        url => Spotify URL.
    """

    artist: str
    name: str
    image: str
    url: str


@dataclass
class ParsedSpotifyURL:
    """
    Class that represents a Spotify URL.

    Takes the following arguments:
        id => Spotify ID.
        type => Spotify type.
    """

    id: str
    type: str