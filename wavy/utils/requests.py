import os

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

    # We don't want to combine subreddits in this case so we can get the most amount of memes.
    # We also don't want to append the memes to the database in case they already exist.

    r_memes = await fetch_subreddit(subreddit="memes", limit=100)
    r_meme = await fetch_subreddit(subreddit="meme", limit=100)
    r_dankmemes = await fetch_subreddit(subreddit="dankmemes", limit=100)
    r_memes_of_the_dank = await fetch_subreddit(
        subreddit="memes_of_the_dank", limit=100
    )

    memes = r_memes + r_meme + r_dankmemes + r_memes_of_the_dank

    await db.set_memes(memes)

    return memes
