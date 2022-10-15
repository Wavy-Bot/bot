import os
import asyncio

import wavy
import aiohttp

from . import database

db = database.Database()


async def fetch_subreddit(
    subreddit: str, category: str = "hot", limit: int = 100
) -> list:
    """Fetches posts from a subreddit."""
    client_id = os.environ["REDDIT_CLIENT_ID"]
    client_secret = os.environ["REDDIT_CLIENT_SECRET"]
    user_agent = os.environ["REDDIT_USER_AGENT"].format(wavy.__VERSION__)

    auth = aiohttp.BasicAuth(client_id, client_secret)
    headers = {"User-Agent": user_agent}

    # Just a quick note: 100 is the maximum limit for the JSON API. (index 0-99).
    # Use + to combine subreddits, e.g "memes+meme+dankmemes+memes_of_the_dank".
    async with aiohttp.ClientSession(
        auth=auth, headers=headers
    ) as session, session.get(
        f"https://reddit.com/r/{subreddit}/{category}.json?limit={limit}"
    ) as response:
        data = await response.json()

        # Announcement posts.
        announcements = data["data"]["dist"] - 100

        posts = data["data"]["children"]

        if announcements > 0:
            posts = posts[announcements:]

        post_list = []

        for post in posts:
            post = post["data"]

            post_list.append(
                {
                    "subreddit": post["subreddit"],
                    "title": post["title"],
                    "over_18": post["over_18"],
                    "url": "https://reddit.com" + post["permalink"],
                    "image": post["url"],
                    "ups": post["ups"],
                    "comments": post["num_comments"],
                }
            )

        return post_list


async def update_memes() -> list:
    """Fetches memes from Reddit and adds them to the database."""
    # We don't want to combine subreddits in this case so we can get the most amount of memes. (400)
    r_memes = await fetch_subreddit(subreddit="memes", limit=100)
    r_meme = await fetch_subreddit(subreddit="meme", limit=100)
    r_dankmemes = await fetch_subreddit(subreddit="dankmemes", limit=100)
    r_memes_of_the_dank = await fetch_subreddit(
        subreddit="memes_of_the_dank", limit=100
    )

    memes = r_memes + r_meme + r_dankmemes + r_memes_of_the_dank

    await db.set_memes(memes)

    return memes


async def post_botlist_data(bot_id: int, server_count: int, shards: int) -> None:
    """Makes a request to all the bot lists Wavy is listed on."""
    botlists = [
        {
            "url": f"https://top.gg/api/bots/{bot_id}/stats",
            "headers": {
                "Authorization": os.environ["TOPGG_API_KEY"],
                "Content-Type": "application/json",
            },
            "data": {"server_count": server_count, "shard_count": shards},
        }
        if os.getenv("TOPGG_API_KEY")
        else None,
        {
            "url": f"https://discord.bots.gg/api/v1/bots/{bot_id}/stats",
            "headers": {
                "Authorization": os.environ["BOTSGG_API_KEY"],
                "Content-Type": "application/json",
            },
            "data": {"guildCount": server_count, "shardCount": shards},
        }
        if os.getenv("BOTSGG_API_KEY")
        else None,
        {
            "url": f"https://discordbotlist.com/api/v1/bots/{bot_id}/stats",
            "headers": {
                "Authorization": os.environ["DISCORDBOTLIST_API_KEY"],
                "Content-Type": "application/json",
            },
            "data": {"guilds": server_count},
        }
        if os.getenv("DISCORDBOTLIST_API_KEY")
        else None,
        {
            "url": f"https://discords.com/bots/api/bot/{bot_id}",
            "headers": {
                "Authorization": os.environ["DISCORDS_API_KEY"],
                "Content-Type": "application/json",
            },
            "data": {"server_count": server_count},
        }
        if os.getenv("DISCORDS_API_KEY")
        else None,
    ]

    # See if there are any None values in the list and remove them.
    botlists = [i for i in botlists if i is not None]

    # If there are no items left in the list, return.
    if not botlists:
        return

    async with aiohttp.ClientSession() as cs:
        await asyncio.gather(
            *[
                cs.post(
                    url=botlist["url"],
                    headers=botlist["headers"],
                    json=botlist["data"],
                )
                for botlist in botlists
            ],
            return_exceptions=False,
        )
