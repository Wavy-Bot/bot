# TODO(Robert): Move this to asyncpg or mongodb

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

    async def set_config_prefix(self, server_id: int, prefix: str):
        """Sets a guild's prefix."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE config SET prefix=%s WHERE server_id=%s;",
                            (prefix, server_id))

            await db.commit()

    async def fetch_config_welcome(self, server_id: int):
        """Fetches if a guild has welcome messages enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT welcome FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def set_config_welcome(self, server_id: int, enabled: bool):
        """Sets a guild's welcome message config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE config SET welcome=%s WHERE server_id=%s;",
                            (enabled, server_id))

            await db.commit()

    async def set_config_leave(self, server_id: int, enabled: bool):
        """Sets a guild's leave message config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE config SET leave=%s WHERE server_id=%s;",
                            (enabled, server_id))

            await db.commit()

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

    async def fetch_config_cleverbot(self, server_id: int):
        """Fetches if a guild has cleverbot enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT cleverbot FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def set_config_cleverbot(self, server_id: int, enabled: bool):
        """Sets a guild's Cleverbot config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE config SET cleverbot=%s WHERE server_id=%s;",
                (enabled, server_id))

            await db.commit()

    async def fetch_config_logs(self, server_id: int):
        """Fetches if a guild has logging enabled."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT logs FROM config WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def set_config_logs(self, server_id: int, enabled: bool):
        """Sets a guild's logging config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE config SET logs=%s WHERE server_id=%s;",
                            (enabled, server_id))

            await db.commit()

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

    async def set_channels_welcome(self, server_id: int, channel_id: int):
        """Sets a guild's welcome channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE channels SET welcome=%s WHERE server_id=%s;",
                (channel_id, server_id))

            await db.commit()

    async def fetch_channels_leave(self, server_id: int):
        """Fetches a guild's leave channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT leave FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def set_channels_leave(self, server_id: int, channel_id: int):
        """Sets a guild's leave channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE channels SET leave=%s WHERE server_id=%s;",
                            (channel_id, server_id))

            await db.commit()

    async def fetch_channels_log(self, server_id: int):
        """Fetches a guild's logging channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("SELECT log FROM channels WHERE server_id=%s;",
                            (server_id, ))

            r = await c.fetchone()

            return r[0]

    async def set_channels_log(self, server_id: int, channel_id: int):
        """Sets a guild's leave channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE channels SET log=%s WHERE server_id=%s;",
                            (channel_id, server_id))

            await db.commit()

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

    async def set_channels_cleverbot(self, server_id: int, channel_id: int):
        """Sets a guild's Cleverbot channel."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE channels SET cleverbot=%s WHERE server_id=%s;",
                (channel_id, server_id))

            await db.commit()

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

    async def set_welcome_message(self, server_id: int, message: str):
        """Sets a guild's welcome message."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE welcome SET message=%s WHERE server_id=%s;",
                (message, server_id))

            await db.commit()

    async def set_welcome_embed(self, server_id: int, enabled: bool):
        """Sets a guild's welcome message embed config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE welcome SET embed=%s WHERE server_id=%s;",
                            (enabled, server_id))

            await db.commit()

    async def set_welcome_embed_colour(self, server_id: int, colour: str):
        """Sets a guild's welcome message embed colour config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE welcome SET embed_colour=%s WHERE server_id=%s;",
                (colour, server_id))

            await db.commit()

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

    async def set_leave_message(self, server_id: int, message: str):
        """Sets a guild's leave message."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE leave SET message=%s WHERE server_id=%s;",
                            (message, server_id))

            await db.commit()

    async def set_leave_embed(self, server_id: int, enabled: bool):
        """Sets a guild's leave message embed config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute("UPDATE leave SET embed=%s WHERE server_id=%s;",
                            (enabled, server_id))

            await db.commit()

    async def set_leave_embed_colour(self, server_id: int, colour: str):
        """Sets a guild's leave message embed colour config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE leave SET embed_colour=%s WHERE server_id=%s;",
                (colour, server_id))

            await db.commit()

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

    async def set_logs(self, server_id: int, msg_delete: bool,
                       msg_bulk_delete: bool, msg_edit: bool, ch_create: bool,
                       ch_delete: bool, member_ban: bool, member_unban: bool,
                       voicestate_update: bool, guild_update: bool,
                       role_create: bool, role_update: bool, role_delete: bool,
                       emoji_update: bool, invite_create: bool,
                       invite_delete: bool):
        """Sets a guild's logging config."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "UPDATE logs SET msg_delete=%s, msg_bulk_delete=%s, msg_edit=%s, ch_create=%s, ch_delete=%s, member_ban=%s, member_unban=%s, voicestate_update=%s, guild_update=%s, role_create=%s, role_update=%s, role_delete=%s, emoji_update=%s, invite_create=%s, invite_delete=%s WHERE server_id=%s;",
                (msg_delete, msg_bulk_delete, msg_edit, ch_create, ch_delete,
                 member_ban, member_unban, voicestate_update, guild_update,
                 role_create, role_update, role_delete, emoji_update,
                 invite_create, invite_delete, server_id))

            await db.commit()

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

    async def fetch_single_role(self, server_id: int, role_type: str):
        """Fetches a single specific role."""
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

    async def fetch_role(self, server_id: int, role_id: int, role_type: str):
        """Fetches a specific role."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM roles WHERE server_id=%s AND role_id=%s AND type=%s;",
                (server_id, role_id, role_type))

            r = await c.fetchone()

            if r:
                role_class = classes.Roles(server_id=server_id,
                                           role_id=r[1],
                                           role_type=r[2])

                return role_class

            return

    async def fetch_roles(self, server_id: int, role_type: str):
        """Fetches multiple roles."""
        async with self.db.connection() as db, db.cursor() as c:
            await c.execute(
                "SELECT * FROM roles WHERE server_id=%s AND type=%s;",
                (server_id, role_type))

            r = await c.fetchall()

            role_list = []

            for i in r:
                role_class = classes.Roles(server_id=server_id,
                                           role_id=i[1],
                                           role_type=i[2])

                role_list.append(role_class)

            return role_list

    async def set_single_role(self, server_id: int, role_id: int,
                              role_type: str):
        """Sets a single role."""
        async with self.db.connection() as db, db.cursor() as c:
            role = await self.fetch_single_role(server_id, role_type)

            if not role:
                await c.execute(
                    "INSERT INTO roles (server_id, role_id, type) VALUES (%s, %s, %s);",
                    (server_id, role_id, role_type))

            else:
                await c.execute(
                    "UPDATE roles SET role_id=%s WHERE server_id=%s AND type=%s;",
                    (role_id, server_id, role_type))

            await db.commit()

    async def set_role(self, server_id: int, role_id: int, role_type: str):
        """Sets a role."""
        async with self.db.connection() as db, db.cursor() as c:
            role = await self.fetch_role(server_id, role_id, role_type)

            if not role:
                await c.execute(
                    "INSERT INTO roles (server_id, role_id, type) VALUES (%s, %s, %s);",
                    (server_id, role_id, role_type))

            else:
                await c.execute(
                    "UPDATE roles SET role_id=%s WHERE server_id=%s AND type=%s;",
                    (role_id, server_id, role_type))

            await db.commit()

    async def remove_role(self, server_id: int, role_id: int, role_type: str):
        """Removes a role."""
        async with self.db.connection() as db, db.cursor() as c:
            role = await self.fetch_role(server_id, role_id, role_type)

            if not role:
                return

            else:
                await c.execute(
                    "DELETE FROM roles WHERE server_id=%s AND role_id=%s AND type=%s;",
                    (server_id, role_id, role_type))

                await db.commit()

                return True

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
