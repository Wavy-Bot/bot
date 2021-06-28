"""FROM https://github.com/PythonistaGuild/Wavelink/blob/master/examples/advanced.py
The MIT License (MIT)

Copyright (c) 2019-2020 PythonistaGuild

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import datetime
import math
import random
import re
import json

import discord
import wavelink
import asyncio
import async_timeout

from core import exceptions
from discord.ext import commands, menus

# URL matching REGEX...
URL_REG = re.compile(r'https?://(?:www\.)?.+')

embcolor = 0x0c0f27  # Set embed color


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')


class Player(wavelink.Player):
    """Custom wavelink Player class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context: commands.Context = kwargs.get('context', None)
        if self.context:
            self.dj: discord.Member = self.context.author

        self.queue = asyncio.Queue()

        self.waiting = False
        self.updating = False

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.stop_votes = set()

    async def do_next(self) -> None:
        if self.is_playing or self.waiting:
            return

        # Clear the votes for a new song...
        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.stop_votes.clear()

        try:
            self.waiting = True
            with async_timeout.timeout(300):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            # No music has been played for 5 minutes, cleanup and disconnect...
            return await self.teardown()

        await self.play(track)
        self.waiting = False

    async def teardown(self):
        """Clear internal states, and disconnects."""
        try:
            await self.destroy()
        except KeyError:
            pass


class PaginatorSource(menus.ListPageSource):
    """Player queue paginator class."""
    def __init__(self, entries, *, per_page=8):
        super().__init__(entries, per_page=per_page)

    async def format_page(self, menu: menus.Menu, page):
        embed = discord.Embed(title='Coming Up...', colour=embcolor)
        embed.description = '\n'.join(f'`{index}. {title}`'
                                      for index, title in enumerate(page, 1))

        return embed

    def is_paginating(self):
        # We always want to embed even on 1 page of results...
        return True


class Music(commands.Cog, wavelink.WavelinkMixin):
    """Music Cog."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.volume = 100

        if not hasattr(bot, 'wavelink'):
            bot.wavelink = wavelink.Client(bot=bot)

        bot.loop.create_task(self.start_nodes())

    async def start_nodes(self) -> None:
        """Connect and intiate nodes."""

        print("[Server] Connecting to Lavalink instance")

        await self.bot.wait_until_ready()

        if self.bot.wavelink.nodes:
            previous = self.bot.wavelink.nodes.copy()

            for node in previous.values():
                await node.destroy()

        with open('wavelink.json') as f:
            nodes = json.load(f)

        for n in nodes.values():
            await self.bot.wavelink.initiate_node(**n)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        print(f'[Server] Node {node.identifier} is ready.')

    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node: wavelink.Node, payload):
        await payload.player.do_next()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        if member.bot:
            return

        player: Player = self.bot.wavelink.get_player(member.guild.id,
                                                      cls=Player)

        if not player.channel_id or not player.context:
            player.node.players.pop(member.guild.id)
            return

        channel = self.bot.get_channel(int(player.channel_id))

        if member == player.dj and after.channel is None:
            for m in channel.members:
                if m.bot:
                    continue
                else:
                    player.dj = m
                    return

        elif after.channel == channel and player.dj not in channel.members:
            player.dj = member

    async def cog_before_invoke(self, ctx: commands.Context):
        """Coroutine called before command invocation.

        We mainly just want to check whether the user is in the players controller channel.
        """
        player: Player = self.bot.wavelink.get_player(ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if player.context:
            if player.context.channel != ctx.channel:
                raise exceptions.IncorrectChannelError(
                    f'{ctx.author.mention}, you must be in {player.context.channel.mention} for this session.'
                )

        if ctx.command.name == 'connect' and not player.context:
            return
        elif self.is_privileged(ctx):
            return

        if not player.channel_id:
            return

        channel = self.bot.get_channel(int(player.channel_id))
        if not channel:
            return

        if player.is_connected:
            if ctx.author not in channel.members:
                raise exceptions.IncorrectChannelError(
                    f'{ctx.author.mention}, you must be in {player.context.channel.mention} for this session.'
                )

    def required(self, ctx: commands.Context):
        """Method which returns required votes based on amount of members in a channel."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)
        channel = self.bot.get_channel(int(player.channel_id))
        required = math.ceil((len(channel.members) - 1) / 2.5)

        if ctx.command.name == 'stop':
            if len(channel.members) == 3:
                required = 2

        return required

    def is_privileged(self, ctx: commands.Context):
        """Check whether the user is an Admin or DJ."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        return player.dj == ctx.author or ctx.author.guild_permissions.kick_members

    @commands.command(aliases=['join', 'c', 'conn'])
    async def connect(self,
                      ctx: commands.Context,
                      *,
                      channel: discord.VoiceChannel = None):
        """Connect to a voice channel."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if player.is_connected:
            return

        channel = getattr(ctx.author.voice, 'channel', channel)
        if channel is None:
            raise exceptions.NoChannelProvided

        await ctx.send(f"**:robot: Joined `{channel.name}`.**")

        await player.connect(channel.id)

    @commands.command(aliases=['sing', 'p', 'pl'])
    async def play(self, ctx: commands.Context, *, query: str):
        """Play or queue a song with the given query."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            await ctx.invoke(self.connect)

        query = query.strip('<>')

        await ctx.send(f"**:mag_right: Searching for `{query}`.**")

        if not URL_REG.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(query)
        if not tracks:
            return await ctx.send(
                '**:x: No songs were found with that query. Please try again.**'
            )

        channel = self.bot.get_channel(int(player.channel_id))

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                track = Track(track.id, track.info, requester=ctx.author)
                await player.queue.put(track)

            qsize = player.queue.qsize()

            # Create embed

            embed = discord.Embed(title=f'Added to queue', colour=embcolor)
            embed.description = f'**[`{tracks.data["playlistInfo"]["name"]}`]({track.uri})**\n\n'
            embed.set_thumbnail(url=track.thumb)

            embed.add_field(
                name='Duration',
                value=str(datetime.timedelta(milliseconds=int(track.length))))
            embed.add_field(name='Queue Length', value=str(qsize))
            embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
            embed.add_field(name='Requested By', value=track.requester.mention)
            embed.add_field(name='DJ', value=player.dj.mention)
            embed.add_field(name='Channel', value=f'{channel.name}')

            await ctx.send(embed=embed)

        else:
            track = Track(tracks[0].id, tracks[0].info, requester=ctx.author)

            qsize = player.queue.qsize()

            # Create embed

            embed = discord.Embed(title=f'Added to queue', colour=embcolor)
            embed.description = f'**[`{track.title}`]({track.uri})**\n\n'
            embed.set_thumbnail(url=track.thumb)

            embed.add_field(
                name='Duration',
                value=str(datetime.timedelta(milliseconds=int(track.length))))
            embed.add_field(name='Queue Length', value=str(qsize + 1))
            embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
            embed.add_field(name='Requested By', value=track.requester.mention)
            embed.add_field(name='DJ', value=player.dj.mention)
            embed.add_field(name='Channel', value=f'{channel.name}')

            await ctx.send(embed=embed)

            await player.queue.put(track)

        if not player.is_playing:
            await player.do_next()

    @commands.command(aliases=['pa', 'stop'])
    async def pause(self, ctx: commands.Context):
        """Pause the currently playing song."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if player.is_paused or not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send(
                '**:pause_button: An admin or DJ has paused the player.**')
            player.pause_votes.clear()

            return await player.set_pause(True)

        required = self.required(ctx)
        player.pause_votes.add(ctx.author)

        if len(player.pause_votes) >= required:
            await ctx.send(
                '**:white_check_mark: Vote to pause passed. Pausing player.**')
            player.pause_votes.clear()
            await player.set_pause(True)
        else:
            await ctx.send(
                f'**:white_check_mark: {ctx.author.mention} has voted to pause the player.**'
            )

    @commands.command(aliases=['r'])
    async def resume(self, ctx: commands.Context):
        """Resume a currently paused player."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_paused or not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send(
                '**:arrow_forward: An admin or DJ has resumed the player.**')
            player.resume_votes.clear()

            return await player.set_pause(False)

        required = self.required(ctx)
        player.resume_votes.add(ctx.author)

        if len(player.resume_votes) >= required:
            await ctx.send(
                '**:white_check_mark: Vote to resume passed. Resuming player.**'
            )
            player.resume_votes.clear()
            await player.set_pause(False)
        else:
            await ctx.send(
                f'**:white_check_mark: {ctx.author.mention} has voted to resume the player.**'
            )

    @commands.command(aliases=['s', 'sk'])
    async def skip(self, ctx: commands.Context):
        """Skip the currently playing song."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send(
                '**:track_next: An admin or DJ has skipped the song.**')
            player.skip_votes.clear()

            return await player.stop()

        if ctx.author == player.current.requester:
            await ctx.send(
                '**:track_next: The song requester has skipped the song.**')
            player.skip_votes.clear()

            return await player.stop()

        required = self.required(ctx)
        player.skip_votes.add(ctx.author)

        if len(player.skip_votes) >= required:
            await ctx.send(
                '**:white_check_mark: Vote to skip passed. Skipping song.**')
            player.skip_votes.clear()
            await player.stop()
        else:
            await ctx.send(
                f'**:white_check_mark: {ctx.author.mention} has voted to skip the song.**'
            )

    @commands.command(aliases=['dis', 'fuckoff', 'fuck_off'])
    async def disconnect(self, ctx: commands.Context):
        """Stop the player and clear all internal states."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send('**:wave: Successfully disconnected.**')
            return await player.teardown()

        required = self.required(ctx)
        player.stop_votes.add(ctx.author)

        if len(player.stop_votes) >= required:
            await ctx.send(
                '**:white_check_mark: Vote to stop passed. Stopping the player.**'
            )
            await player.teardown()
        else:
            await ctx.send(
                f'**:white_check_mark: {ctx.author.mention} has voted to stop the player.**'
            )

    @commands.command(aliases=['v', 'vol'])
    async def volume(self, ctx: commands.Context, *, vol: str = None):
        """Change the player's volume, between 1 and 100."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if not vol:
            await ctx.send(
                f"**:loud_sound: The volume is currently set to {self.volume}%**"
            )
            return

        vol = int(vol.replace('%', ''))

        if not self.is_privileged(ctx):
            return await ctx.send(
                '**:x: Only the DJ or admins may change the volume.**')

        if not 0 < vol < 101:
            return await ctx.send(
                '**:x: Please enter a value between 1 and 100.**')

        await player.set_volume(vol)
        self.volume = vol
        await ctx.send(f"**:level_slider: Set volume to {vol}%**")

    @commands.command(aliases=['mix'])
    async def shuffle(self, ctx: commands.Context):
        """Shuffle the player's queue."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if player.queue.qsize() < 3:
            return await ctx.send(
                '**:x: Add more songs to the queue before shuffling.**')

        if self.is_privileged(ctx):
            await ctx.send(
                '**:twisted_rightwards_arrows: Shuffled the playlist.**')
            player.shuffle_votes.clear()
            return random.shuffle(player.queue._queue)

        required = self.required(ctx)
        player.shuffle_votes.add(ctx.author)

        if len(player.shuffle_votes) >= required:
            await ctx.send(
                '**:white_check_mark: Vote to shuffle passed. Shuffling the playlist.**'
            )
            player.shuffle_votes.clear()
            random.shuffle(player.queue._queue)
        else:
            await ctx.send(
                f'**:white_check_mark: {ctx.author.mention} has voted to shuffle the playlist.**'
            )

    @commands.command(aliases=['eq'])
    async def equalizer(self, ctx: commands.Context, *, equalizer: str = None):
        """Changes the player's equalizer."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                '**:x: Only the DJ or admins may change the equalizer.**')

        eqs = {
            'flat': wavelink.Equalizer.flat(),
            'boost': wavelink.Equalizer.boost(),
            'metal': wavelink.Equalizer.metal(),
            'piano': wavelink.Equalizer.piano()
        }

        if not equalizer:
            joined = "\n• ".join(eqs.keys())
            return await ctx.send(
                f'**:x: Invalid EQ provided.** Valid EQs:\n\n• {joined}')

        eq = eqs.get(equalizer.lower(), None)

        if not eq:
            joined = "\n• ".join(eqs.keys())
            return await ctx.send(
                f'**:x: Invalid EQ provided.** Valid EQs:\n\n• {joined}')

        await ctx.send(
            f'**:control_knobs: Successfully changed equalizer to {equalizer}.**'
        )
        await player.set_eq(eq)

    @commands.command(aliases=['q', 'que'])
    async def queue(self, ctx: commands.Context):
        """Display the player's queued songs."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if player.queue.qsize() == 0:
            return await ctx.send(
                '**:x: There are no more songs in the queue.**')

        entries = [track.title for track in player.queue._queue]
        pages = PaginatorSource(entries=entries)
        paginator = menus.MenuPages(source=pages,
                                    timeout=None,
                                    delete_message_after=True)

        await paginator.start(ctx)

    @commands.command(aliases=['np', 'now_playing', 'current'])
    async def nowplaying(self, ctx: commands.Context):
        """Sends an embed with information about the currently playing song."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        channel = self.bot.get_channel(int(player.channel_id))
        qsize = player.queue.qsize()

        track = player.current

        # Create embed

        embed = discord.Embed(title=f'Now playing', colour=embcolor)
        embed.description = f'**[`{track.title}`]({track.uri})**\n\n'
        embed.set_thumbnail(url=track.thumb)

        embed.add_field(
            name='Duration',
            value=str(datetime.timedelta(milliseconds=int(track.length))))
        embed.add_field(name='Queue Length', value=str(qsize))
        embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
        embed.add_field(name='Requested By', value=track.requester.mention)
        embed.add_field(name='DJ', value=player.dj.mention)
        embed.add_field(name='Channel', value=f'{channel.name}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['swap'])
    async def swap_dj(self,
                      ctx: commands.Context,
                      *,
                      member: discord.Member = None):
        """Swap the current DJ to another member in the voice channel."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                                      cls=Player,
                                                      context=ctx)

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                '**:x: Only admins and the DJ may use this command.**')

        members = self.bot.get_channel(int(player.channel_id)).members

        if member and member not in members:
            return await ctx.send(
                f'**:x: {member} is not currently in voice, so can not be a DJ.**'
            )

        if member and member == player.dj:
            return await ctx.send(
                '**:x: Cannot swap DJ to the current DJ... :)**')

        if len(members) <= 2:
            return await ctx.send('**:x: No more members to swap to.**')

        if member:
            player.dj = member
            return await ctx.send(
                f'**:control_knobs: {member.mention} is now the DJ.**')

        for m in members:
            if m == player.dj or m.bot:
                continue
            else:
                player.dj = m
                return await ctx.send(
                    f'**:control_knobs: {member.mention} is now the DJ.**')


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Music(bot))
