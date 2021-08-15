import os

import psycopg

from core import classes, exceptions
from psycopg import pool
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_DATABASE")
PORT = os.getenv("DB_PORT")


def init_db():
    """Performs DB initialization."""
    with psycopg.Connection.connect(
            f"user={USERNAME} password={PASSWORD} host={HOST} dbname={DATABASE} port={PORT}"
    ) as db, db.cursor() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS config(
            server_id BIGINT,
            prefix TEXT,
            welcome BOOL DEFAULT false,
            autorole BOOL DEFAULT false,
            leave BOOL DEFAULT false,
            level BOOL DEFAULT false,
            level_rewards BOOL DEFAULT false,
            stack_rewards BOOL DEFAULT false,
            cleverbot BOOL DEFAULT false,
            logs BOOL DEFAULT false,
            captcha BOOL DEFAULT false
        );
        CREATE TABLE IF NOT EXISTS channels(
            server_id BIGINT,
            welcome BIGINT,
            leave BIGINT,
            log BIGINT,
            level BIGINT,
            captcha BIGINT,
            cleverbot BIGINT
        );
        CREATE TABLE IF NOT EXISTS roles(
            server_id BIGINT,
            role_id BIGINT,
            type TEXT
        );
        CREATE TABLE IF NOT EXISTS welcome(
            server_id BIGINT,
            message TEXT,
            embed BOOL DEFAULT true,
            embed_colour TEXT
        );
        CREATE TABLE IF NOT EXISTS leave(
            server_id BIGINT,
            message TEXT,
            embed BOOL DEFAULT true,
            embed_colour TEXT
        );
        CREATE TABLE IF NOT EXISTS level(
            server_id BIGINT,
            member_id BIGINT,
            level BIGINT,
            xp BIGINT
        );
        CREATE TABLE IF NOT EXISTS level_rewards(
            server_id BIGINT,
            role_id BIGINT,
            level BIGINT
        );
        CREATE TABLE IF NOT EXISTS logs(
            server_id BIGINT,
            msg_delete BOOL DEFAULT true,
            msg_bulk_delete BOOL DEFAULT true,
            msg_edit BOOL DEFAULT true,
            ch_create BOOL DEFAULT true,
            ch_delete BOOL DEFAULT true,
            member_ban BOOL DEFAULT true,
            member_unban BOOL DEFAULT true,
            voicestate_update BOOL DEFAULT false,
            guild_update BOOL DEFAULT true,
            role_create BOOL DEFAULT true,
            role_update BOOL DEFAULT true,
            role_delete BOOL DEFAULT true,
            emoji_update BOOL DEFAULT false,
            invite_create BOOL DEFAULT false,
            invite_delete BOOL DEFAULT false
        );
        CREATE TABLE IF NOT EXISTS mutes(
            server_id BIGINT,
            member_id BIGINT,
            end_time TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS warns(
            server_id BIGINT,
            member_id BIGINT,
            warn_id TEXT,
            reason TEXT
        );
        CREATE TABLE IF NOT EXISTS giveaways(
            server_id BIGINT,
            channel_id BIGINT,
            message_id BIGINT,
            winners BIGINT,
            end_time TIMESTAMP
        )
        """)

        db.commit()

        c.close()
        db.close()


class Database:
    """Class that contains database-related functions."""
    def __init__(self):
        self.db = self.create_db_pool()

    @staticmethod
    def create_db_pool():
        """Creates an asyncronous database pool."""
        db_pool = pool.AsyncConnectionPool(
            f"user={USERNAME} password={PASSWORD} host={HOST} dbname={DATABASE} port={PORT}"
        )

        return db_pool

    async def add_guild(self, server_id: str):
        """Creates rows for a specific guild."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT server_id FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            if not r:
                # NOTE(Robert): This is like this due to
                #               psycopg.errors.SyntaxError: cannot insert multiple commands into a prepared statement
                await c.execute("INSERT INTO config (server_id) VALUES (%s);",
                                (server_id, ))
                await c.execute(
                    "INSERT INTO channels (server_id) VALUES (%s);",
                    (server_id, ))
                await c.execute("INSERT INTO welcome (server_id) VALUES (%s);",
                                (server_id, ))
                await c.execute("INSERT INTO leave (server_id) VALUES (%s);",
                                (server_id, ))
                await c.execute("INSERT INTO logs (server_id) VALUES (%s);",
                                (server_id, ))

                await db.commit()

    async def remove_guild(self, server_id: str):
        """Removes all rows that correspond to a specific guild."""
        async with self.db.connection() as db, db.cursor() as c:
            # NOTE(Robert): This is like this due to
            #               psycopg.errors.SyntaxError: cannot insert multiple commands into a prepared statement
            await c.execute("DELETE FROM config WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM channels WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM welcome WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM leave WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM level WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM level_rewards WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM logs WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM mutes WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM roles WHERE server_id=%s;",
                            (server_id, ))

            await db.commit()

    async def remove_old_guilds(self, servers: list):
        """Removes all rows that correspond to an old guild the bot isn't part of anymore."""
        # @NOTE(Robert): Oh boy, this is messy.
        server_list = [i.id for i in servers]

        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT server_id FROM config;")

            r = await c.fetchall()

            for i in r:
                if i[0] not in server_list:
                    await self.remove_guild(i[0])

    async def fetch_config_prefix(self, server_id: int):
        """Fetches a guild's prefix."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT prefix FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            if r:
                return r[0]

            return r

    async def fetch_config_welcome(self, server_id: int):
        """Fetches if a guild has welcome messages enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT welcome FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_autorole(self, server_id: int):
        """Fetches if a guild has autorole enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT autorole FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_leave(self, server_id: int):
        """Fetches if a guild has leave messages enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT leave FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_level(self, server_id: int):
        """Fetches if a guild has level messages enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT level FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_level_rewards(self, server_id: int):
        """Fetches if a guild has level rewards enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT level_rewards FROM config WHERE server_id=%s;",
                (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_stack_rewards(self, server_id: int):
        """Fetches if a guild has level reward stacking enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT stack_rewards FROM config WHERE server_id=%s;",
                (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_cleverbot(self, server_id: int):
        """Fetches if a guild has cleverbot enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT cleverbot FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_logs(self, server_id: int):
        """Fetches if a guild has logging enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT logs FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_config_captcha(self, server_id: int):
        """Fetches if a guild has captchas enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT captcha FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_channels_welcome(self, server_id: int):
        """Fetches a guild's welcome channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT welcome FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_channels_leave(self, server_id: int):
        """Fetches a guild's leave channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT leave FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_channels_log(self, server_id: int):
        """Fetches a guild's logging channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT log FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_channels_level(self, server_id: int):
        """Fetches a guild's level channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT level FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_channels_captcha(self, server_id: int):
        """Fetches a guild's captcha channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT captcha FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_channels_cleverbot(self, server_id: int):
        """Fetches a guild's cleverbot channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT cleverbot FROM channels WHERE server_id=%s;",
                (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def fetch_welcome(self, server_id: int):
        """Fetches a guild's welcome message settings."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT * FROM welcome WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            welcome_class = classes.Welcome(server_id=r[0],
                                            message=r[1],
                                            embed=r[2],
                                            embed_colour=r[3])

            return welcome_class

    async def fetch_leave(self, server_id: int):
        """Fetches a guild's leave message settings."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT * FROM leave WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            leave_class = classes.Leave(server_id=r[0],
                                        message=r[1],
                                        embed=r[2],
                                        embed_colour=r[3])

            return leave_class

    async def fetch_level(self, server_id: int, member_id: int):
        """Fetches a guild's level settings."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM level WHERE server_id=%s AND member_id=%s;",
                (server_id, member_id))

            r = await c.fetchone()

            if r:
                level_class = classes.Level(server_id=r[0],
                                            member_id=r[1],
                                            level=r[2],
                                            xp=r[3])

                return level_class

            return

    async def set_xp(self, xp: int, server_id: int, member_id: int):
        """Sets a member's XP."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT xp FROM level WHERE member_id=%s;",
                            (member_id, ))

            r = await c.fetchone()

            if not r:
                await c.execute(
                    "INSERT INTO level (xp, server_id, member_id, level) VALUES (%s, %s, %s, 0);",
                    (xp, server_id, member_id))

            else:
                await c.execute(
                    "UPDATE level SET xp=%s, server_id=%s, member_id=%s WHERE member_id=%s;",
                    (xp, server_id, member_id, member_id))

            await db.commit()

    async def set_level(self, level: int, server_id: int, member_id: int):
        """Sets a member's level."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE level SET level=%s, server_id=%s, member_id=%s WHERE member_id=%s;",
                (level, server_id, member_id, member_id))

            await db.commit()

    async def fetch_level_rewards(self, level: int, server_id: int):
        """Fetches level rewards for said level, returns None if no level reward for that level has been configured."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM level_rewards WHERE server_id=%s AND level=%s;",
                (server_id, level))

            r = await c.fetchall()

            if r:
                rewards_list = []

                for i in r:
                    rewards_class = classes.LevelRewards(server_id=i[0],
                                                         role_id=i[1],
                                                         level=i[2])

                    rewards_list.append(rewards_class)
                return rewards_list

            return

    async def fetch_lower_level_rewards(self, level: int, server_id: int):
        """
        Fetches level rewards for lower levels,
        returns None if no level reward for any lower level has been found.
        """
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM level_rewards WHERE server_id=%s AND level < %s;",
                (server_id, level))

            r = await c.fetchall()

            if r:
                rewards_list = []

                for i in r:
                    rewards_class = classes.LevelRewards(server_id=i[0],
                                                         role_id=i[1],
                                                         level=i[2])

                    rewards_list.append(rewards_class)
                return rewards_list

            return

    async def fetch_logs(self, server_id: int):
        """Fetches a guild's log settings."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT * FROM logs WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            logs_class = classes.Logs(server_id=r[0],
                                      msg_delete=r[1],
                                      msg_bulk_delete=r[2],
                                      msg_edit=r[3],
                                      ch_create=r[4],
                                      ch_delete=r[5],
                                      member_ban=r[6],
                                      member_unban=r[7],
                                      voicestate_update=r[8],
                                      guild_update=r[9],
                                      role_create=r[10],
                                      role_update=r[11],
                                      role_delete=r[12],
                                      emoji_update=r[13],
                                      invite_create=r[14],
                                      invite_delete=r[15])

            return logs_class

    async def fetch_mutes(self):
        """Fetches all mutes."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT * FROM mutes;")

            r = await c.fetchall()

            mute_list = []

            for i in r:
                mute_class = classes.Mutes(server_id=i[0],
                                           member_id=i[1],
                                           end_time=i[2])

                mute_list.append(mute_class)

            return mute_list

    async def fetch_mute(self, server_id: int, member_id: int):
        """Fetches if a member is muted in a specific guild."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM mutes WHERE server_id=%s AND member_id=%s;",
                (server_id, member_id))

            r = await c.fetchone()

            if r:
                mute_class = classes.Mutes(server_id=server_id,
                                           member_id=r[1],
                                           end_time=r[2])

                return mute_class

            return

    async def set_mute(self,
                       server_id: int,
                       member_id: int,
                       time: object = None):
        """Mutes a member."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "INSERT INTO mutes (server_id, member_id, end_time) VALUES (%s, %s, %s);",
                (server_id, member_id, time))

            await db.commit()

    async def remove_mute(self, server_id: int, member_id: int):
        """Unmutes a member."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "DELETE FROM mutes WHERE server_id=%s AND member_id=%s",
                (server_id, member_id))

            await db.commit()

    async def fetch_role(self, server_id: int, role_type: str):
        """Fetches a specific role."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM roles WHERE server_id=%s AND type=%s;",
                (server_id, role_type))

            r = await c.fetchone()

            if r:
                role_class = classes.Roles(server_id=server_id,
                                           role_id=r[1],
                                           role_type=r[2])

                return role_class

            return

    async def set_role(self, server_id: int, role_id: int, role_type: str):
        """Sets a role."""
        async with self.db.connection() as db, db.cursor() as c:
            role = await self.fetch_role(server_id, role_type)

            if not role:
                await c.execute(
                    "INSERT INTO roles (server_id, role_id, type) VALUES (%s, %s, %s);",
                    (server_id, role_id, role_type))

            else:

                await c.execute(
                    "UPDATE roles SET role_id=%s WHERE server_id=%s AND type=%s;",
                    (role_id, server_id, role_type))

            await db.commit()

    async def fetch_warns(self, server_id: int, member_id: int):
        """Fetches all warnings a member has."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM warns WHERE server_id=%s AND member_id=%s;",
                (server_id, member_id))

            r = await c.fetchall()

            warn_list = []

            for i in r:
                warn_class = classes.Warns(server_id=server_id,
                                           member_id=member_id,
                                           warn_id=i[2],
                                           reason=i[3])

                warn_list.append(warn_class)

            return warn_list

    async def fetch_warn(self, server_id: int, warn_id: str):
        """Fetches a warning by ID."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM warns WHERE server_id=%s AND warn_id=%s;",
                (server_id, warn_id))

            r = await c.fetchone()

            if r:
                warn_class = classes.Warns(server_id=server_id,
                                           member_id=r[1],
                                           warn_id=warn_id,
                                           reason=r[3])

                return warn_class

            return

    async def set_warn(self, server_id: int, member_id: int, warn_id: str,
                       reason: str):
        """Warns a member."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "INSERT INTO warns (server_id, member_id, warn_id, reason) VALUES (%s, %s, %s, %s);",
                (server_id, member_id, warn_id, reason))

            await db.commit()

    async def remove_warn(self, server_id: int, warn_id: str):
        """Unwarns a member."""
        async with self.db.connection() as db, db.cursor() as c:
            if await self.fetch_warn(server_id, warn_id):

                await c.execute(
                    "DELETE FROM warns WHERE server_id=%s AND warn_id=%s",
                    (server_id, warn_id))

                await db.commit()

                return

            raise exceptions.NonExistantWarnID(
                message=f"Could not find warning with ID `{warn_id}`.")

    async def set_giveaway(self, server_id: int, channel_id: int,
                           message_id: int, winners: int, end_time: object):
        """Sets a giveaway."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "INSERT INTO giveaways (server_id, channel_id, message_id, winners, end_time)"
                "VALUES (%s, %s, %s, %s, %s);",
                (server_id, channel_id, message_id, winners, end_time))

            await db.commit()

    async def fetch_giveaway(self, server_id: int, message_id: int):
        """Fetches a giveaway."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM giveaways WHERE server_id=%s AND message_id=%s;",
                (server_id, message_id))

            r = await c.fetchone()

            if r:
                giveaway_class = classes.Giveaways(server_id=server_id,
                                                   channel_id=r[1],
                                                   message_id=r[2],
                                                   winners=r[3],
                                                   end_time=r[4])

                return giveaway_class
            return

    async def remove_giveaway(self, server_id: int, message_id: int):
        """Deletes a giveaway."""
        async with self.db.connection() as db, db.cursor() as c:
            if await self.fetch_giveaway(server_id, message_id):
                await c.execute(
                    "DELETE FROM giveaways WHERE server_id=%s AND message_id=%s",
                    (server_id, message_id))

                await db.commit()

                return

            raise exceptions.NonExistantMessageID(
                message=f"Could not find giveaway with ID `{message_id}`.")

    async def fetch_giveaways(self):
        """Fetches all giveaways."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT * FROM giveaways;")

            r = await c.fetchall()

            giveaway_list = []

            for i in r:
                giveaway_class = classes.Giveaways(server_id=i[0],
                                                   channel_id=i[1],
                                                   message_id=i[2],
                                                   winners=i[3],
                                                   end_time=i[4])

                giveaway_list.append(giveaway_class)

            return giveaway_list

    async def fetch_giveaways_in_guild(self, server_id: int):
        """Fetches all giveaways in a guild."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT * FROM giveaways WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchall()

            giveaway_list = []

            for i in r:
                giveaway_class = classes.Giveaways(server_id=i[0],
                                                   channel_id=i[1],
                                                   message_id=i[2],
                                                   winners=i[3],
                                                   end_time=i[4])

                giveaway_list.append(giveaway_class)

            return giveaway_list
