import random

import aiohttp

from core import classes
from core import exceptions
from discord.ext import commands


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

                raise commands.NSFWChannelRequired(channel=channel)

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


async def sra_image(animal: str):
    """Fetches a random image of the specified animal from Some Random API."""
    async with aiohttp.ClientSession() as cs, cs.get(
            f'https://some-random-api.ml/img/{animal}') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data['link']

            return url

        raise exceptions.APIError


async def sad_cat():
    """Fetches a random image of a sat cat from Wavy's API."""
    async with aiohttp.ClientSession() as cs, cs.get(
            'https://api.wavybot.com/sad_cat') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data['url']

            return url

        raise exceptions.APIError


async def duck():
    """Fetches a random image of a duck from random-d.uk."""
    async with aiohttp.ClientSession() as cs, cs.get(
            'https://random-d.uk/api/v2/random') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data['url']

            return url

        raise exceptions.APIError


async def bunny():
    """Fetches a random image of a bunny from bunnies.io."""
    async with aiohttp.ClientSession() as cs, cs.get(
            'https://api.bunnies.io/v2/loop/random/?media=gif,png') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data['media']['gif']

            return url

        raise exceptions.APIError


async def shiba():
    """Fetches a random image of a shiba from shibe.online."""
    async with aiohttp.ClientSession() as cs, cs.get(
            'https://shibe.online/api/shibes') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data[0]

            return url

        raise exceptions.APIError


async def sloth():
    """Fetches a random image of a sloth from sloth.pics."""
    async with aiohttp.ClientSession() as cs, cs.get(
            'https://sloth.pics/api') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data['url']

            return url

        raise exceptions.APIError


async def lizard():
    """Fetches a random image of a lizard from nekos.life."""
    async with aiohttp.ClientSession() as cs, cs.get(
            'https://nekos.life/api/v2/img/lizard') as resp:
        if resp.status == 200:
            data = await resp.json()

            url = data['url']

            return url

        raise exceptions.APIError


async def http_cat(code: int):
    """Fetches an HTTP cat from http.cat."""
    async with aiohttp.ClientSession() as cs, cs.get(
            f'https://http.cat/{code}') as resp:
        url = "https://http.cat/404"

        if resp.status == 200:
            url = f"https://http.cat/{code}"

        return url


async def http_dog(code: int):
    """Fetches an HTTP dog from httpstatusdogs.com."""
    async with aiohttp.ClientSession() as cs, cs.get(
            f'https://httpstatusdogs.com/img/{code}.jpg') as resp:
        url = "https://httpstatusdogs.com/img/404.jpg"

        if resp.status == 200:
            url = f"https://httpstatusdogs.com/img/{code}.jpg"

        return url


async def http_duck(code: int):
    """Fetches an HTTP duck from random-d.uk."""
    async with aiohttp.ClientSession() as cs, cs.get(
            f'https://random-d.uk/api/v2/http/{code}') as resp:
        url = "https://random-d.uk/api/v2/http/404"

        if resp.status == 200:
            url = f"https://random-d.uk/api/v2/http/{code}"

        return url
