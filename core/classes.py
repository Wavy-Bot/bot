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


class ProgressBar:
    """
    Class that represents a progress bar.

    Takes the following arguments:
        bar => The progress bar itself.
        percentage => The percentage used for the progress bar.
    """
    def __init__(self, bar: str, percentage: int):
        self.bar = bar
        self.percentage = percentage


class Welcome:
    """
    Class that represents the welcome table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        message => Welcome message.
        embed => Whether or not the welcome message is an embed.
        embed_colour => Colour of the embed.
    """
    def __init__(self, server_id: int, message: str, embed: bool,
                 embed_colour: int):
        self.server_id = server_id
        self.message = message
        self.embed = embed
        self.embed_colour = embed_colour


class Leave:
    """
    Class that represents the leave table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        message => Leave message.
        embed => Whether or not the leave message is an embed.
        embed_colour => Colour of the embed.
    """
    def __init__(self, server_id: int, message: str, embed: bool,
                 embed_colour: int):
        self.server_id = server_id
        self.message = message
        self.embed = embed
        self.embed_colour = embed_colour


class Level:
    """
    Class that represents the level table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        member_id => Discord member ID.
        level => Member's level.
        xp => Member's xp.
    """
    def __init__(self, server_id: int, member_id: int, level: int, xp: int):
        self.server_id = server_id
        self.member_id = member_id
        self.level = level
        self.xp = xp


class LevelRewards:
    """
    Class that represents the level rewards table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        role_id => Discord role ID.
        level => Level at which a member gets said role.
    """
    def __init__(self, server_id: int, role_id: int, level: int):
        self.server_id = server_id
        self.role_id = role_id
        self.level = level


class Logs:
    """
    Class that represents the logs table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        msg_delete => Message delete bool.
        msg_edit => Message edit bool.
        ch_create => Create channel bool.
        ch_delete => Channel delete bool.
        member_ban => Member ban bool.
        member_unban => Member unban bool.
        voicestate_update => Voicestate update bool.
        guild_update => Guild update bool.
        integration_update => Integration update bool.
        webhook_update => Webhook update bool.
        role_create => Role create bool.
        role_update => Role update bool.
        role_delete => Role delete bool.
        emoji_update => Emoji update bool.
        invite_create => Invite create bool.
        invite_delete => Invite delete bool.
    """
    def __init__(self, server_id: int, msg_delete: bool, msg_bulk_delete: bool,
                 msg_edit: bool, ch_create: bool, ch_delete: bool,
                 member_ban: bool, member_unban: bool, voicestate_update: bool,
                 guild_update: bool, role_create: bool, role_update: bool,
                 role_delete: bool, emoji_update: bool, invite_create: bool,
                 invite_delete: bool):
        self.server_id = server_id
        self.msg_delete = msg_delete
        self.msg_bulk_delete = msg_bulk_delete
        self.msg_edit = msg_edit
        self.ch_create = ch_create
        self.ch_delete = ch_delete
        self.member_ban = member_ban
        self.member_unban = member_unban
        self.voicestate_update = voicestate_update
        self.guild_update = guild_update
        self.role_create = role_create
        self.role_update = role_update
        self.role_delete = role_delete
        self.emoji_update = emoji_update
        self.invite_create = invite_create
        self.invite_delete = invite_delete


class Mutes:
    """
    Class that represents the mutes table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        member_id => Discord member ID.
        end_time => Timestamp the mute will end at, will be None if no time specified.
    """
    def __init__(self,
                 server_id: int = None,
                 member_id: int = None,
                 end_time: object = None):
        self.server_id = server_id
        self.member_id = member_id
        self.end_time = end_time


class Roles:
    """
    Class that represents the roles table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        role_id => Discord role ID.
        role_type => Role type.
    """
    def __init__(self, server_id: int, role_id: int, role_type: str):
        self.server_id = server_id
        self.role_id = role_id
        self.role_type = role_type


class Time:
    """
    Class that represents the time in seconds and in a datetime object.

    Takes the following arguments:
        time => Time in seconds.
        timedelta => datetime object.
    """
    def __init__(self, time: int, timedelta: object):
        self.time = time
        self.timedelta = timedelta


class Warns:
    """
    Class that represents the warns table in the database.

    Takes the following arguments:
        server_id => Discord server ID.
        member_id => Discord member ID.
        warn_id => ID assigned to the warning.
        reason => Reason the member got a warning.
    """
    def __init__(self, server_id: int, member_id: int, warn_id: str,
                 reason: str):
        self.server_id = server_id
        self.member_id = member_id
        self.warn_id = warn_id
        self.reason = reason
