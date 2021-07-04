import os

import psycopg3

from core import classes
from psycopg3 import pool
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_DATABASE")
PORT = os.getenv("DB_PORT")


def init_db():
    """Performs DB initialization."""
    with psycopg3.Connection.connect(
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
                #               psycopg3.errors.SyntaxError: cannot insert multiple commands into a prepared statement
                await c.execute("INSERT INTO config (server_id) VALUES (%s);",
                                (server_id, ))
                await c.execute(
                    "INSERT INTO channels (server_id) VALUES (%s);",
                    (server_id, ))
                await c.execute("INSERT INTO welcome (server_id) VALUES (%s);",
                                (server_id, ))
                await c.execute("INSERT INTO leave (server_id) VALUES (%s);",
                                (server_id, ))

                await db.commit()

    async def remove_guild(self, server_id: str):
        """Removes all rows that correspond to a specific guild."""
        async with self.db.connection() as db, db.cursor() as c:
            # NOTE(Robert): This is like this due to
            #               psycopg3.errors.SyntaxError: cannot insert multiple commands into a prepared statement
            await c.execute("DELETE FROM config WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM channels WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM welcome WHERE server_id=%s;",
                            (server_id, ))
            await c.execute("DELETE FROM leave WHERE server_id=%s;",
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

            welcome_class = classes.Leave(server_id=r[0],
                                          message=r[1],
                                          embed=r[2],
                                          embed_colour=r[3])

            return welcome_class
