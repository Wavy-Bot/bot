import random

import aiohttp

from core import classes
from core import exceptions


async def reddit(subreddit: str, category: str, channel):
    """Fetches a random post from the specified subreddit."""
    async with aiohttp.ClientSession() as cs, cs.get(
            f"https://www.reddit.com/r/{subreddit}/{category}.json") as resp:
        if resp.status == 200:

            data = await resp.json()

            children = len(data['data']['children'])

            if not children:

                raise exceptions.APIError(
                    message=
                    "The requested subreddit has no posts. Please make sure your spelling is correct, otherwise "
                    "try again later. ")

            post = data['data']['children'][random.randint(0,
                                                           children)]['data']

            if post['over_18'] and not channel.is_nsfw():

                raise exceptions.NSFWChannelRequired

            post_class = classes.Reddit(subreddit=post['subreddit'],
                                        title=post['title'],
                                        link=post['permalink'],
                                        image_url=post['url'],
                                        upvotes=post['ups'],
                                        comments=post['num_comments'])

            return post_class

        raise exceptions.APIError(
            message=
            "Reddit's API returned an error. Please make sure your spelling is correct, otherwise try again leter."
        )


async def minecraft_uuid(username: str):
    """Fetches the UUID of a Minecraft user."""
    async with aiohttp.ClientSession() as cs, cs.get(
            f'https://api.mojang.com/users/profiles/minecraft/{username}'
    ) as resp:
        data = await resp.json()

        if resp.status == 200:

            mc_class = classes.Minecraft(name=data['name'], uuid=data['id'])

            return mc_class

        raise exceptions.APIError(message=data['errorMessage'])


async def crafatar(username: str, endpoint: str):
    """Fetches a render from Crafatar."""
    data = await minecraft_uuid(username)

    url = f"https://crafatar.com/renders/{endpoint}/{data.uuid}?overlay=true"

    crafatar_class = classes.Crafatar(url=url, uuid_class=data)

    return crafatar_class
