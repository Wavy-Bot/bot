import os
import re
import json
import math
import random

import wavelink
import discord

from ..utils import errors
from discord.ext import commands, pages
from wavelink.ext import spotify


class Player(wavelink.Player):
    """Custom wavelink Player class."""

    def __init__(self, ctx: commands.Context, dj: discord.Member = None):
        super().__init__()
        if not dj:
            dj = ctx.author
        self.dj = dj
        self.ctx = ctx

        self.queue = wavelink.Queue()

        self.waiting = False
        self.updating = False

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.seek_votes = set()
        self.forward_votes = set()
        self.rewind_votes = set()
        self.remove_votes = set()
        self.stop_votes = set()

    async def do_next(self) -> None:
        """Play the next track in the queue."""
        if self.is_playing() or self.is_paused():
            return

        # Clear the votes for a new song
        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.seek_votes.clear()
        self.forward_votes.clear()
        self.rewind_votes.clear()
        self.remove_votes.clear()
        self.stop_votes.clear()

        try:
            track = self.queue.get()
        except wavelink.QueueEmpty:
            # No music to play, stop the player and disconnect.
            await self.ctx.send(
                "**:white_check_mark: Disconnected from the voice channel since there are no more songs in the queue.**"
            )
            return await self.teardown()

        await self.play(track)

    async def teardown(self) -> None:
        """Clears the queue, stops the player and disconnects."""
        self.queue.clear()
        await self.stop()
        await self.disconnect()

    async def put_in_queue(self, track: wavelink.Track, position: str) -> None:
        """Put a track in the queue at a certain position."""
        if position == "start":
            self.queue.put_at_front(track)
        elif position == "end":
            self.queue.put(track)


class Music(commands.Cog):
    """Music cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emb_colour = int(os.getenv("COLOUR"), 16)

        # Regex
        self.url_reg = re.compile(r"https?://(?:www\.)?.+")
        self.yt_url_reg = re.compile(
            r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        )
        self.yt_playlist_reg = re.compile(r"^.*(youtu\.be|youtube\.com)(?=.*list=).*")
        self.sc_url_reg = re.compile(
            r"^((?:https?:)?\/\/)?((?:www)\.)?((?:soundcloud?\.com))"
        )

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self) -> None:
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        with open("lavalink.json") as f:
            nodes = json.load(f)

        for node in nodes.values():
            await wavelink.NodePool.create_node(
                bot=self.bot,
                **node,
                spotify_client=spotify.SpotifyClient(
                    client_id=os.environ["SPOTIFY_CLIENT_ID"],
                    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                ),
            )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node) -> None:
        """Event fired when a node has finished connecting."""
        print(f"[Wavelink] Node: <{node.identifier}> is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: Player, track: wavelink.Track, reason: str
    ) -> None:
        """Event fired when a track ends."""
        await player.do_next()

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(
        self, player: Player, track: wavelink.Track, reason: str
    ) -> None:
        """Event fired when a track is stuck."""
        await player.ctx.send(
            "**:disappointed_relieved: Uh-oh! The track seems to have gotten stuck for some reason."
            + (
                " I'm going to attempt to play the next song.**"
                if not player.queue.is_empty
                else "**"
            )
        )

        await player.do_next()

    @commands.Cog.listener()
    async def on_wavelink_track_exception(
        self, player: Player, track: wavelink.Track, error: any
    ) -> None:
        """Event fired when a track exception occurs."""
        await player.ctx.send(
            "**:disappointed_relieved: Uh-oh! Something broke while playing the track."
            + (
                " I'm going to attempt to play the next song.**"
                if not player.queue.is_empty
                else "**"
            )
        )

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if member.bot:
            return

        # Go through the nodes, and get the player for the guild.
        for node in wavelink.NodePool().nodes.values():
            player = node.get_player(
                after.channel.guild if after.channel else before.channel
            )
            if player:
                # If everyone left the channel, stop the player and leave too.
                if len(player.channel.members) == 1:
                    await player.teardown()

                # If the DJ left the channel, assign a new DJ.
                if member.id == player.dj.id and after.channel is not player.channel:
                    for m in player.channel.members:
                        if m.bot:
                            continue
                        else:
                            player.dj = m
                            return

    @staticmethod
    def is_privileged(ctx: commands.Context):
        """Check whether the user is an Admin or DJ."""
        vc: Player = ctx.voice_client

        return (
            vc.dj == ctx.author
            or ctx.author.guild_permissions.mute_members
            or ctx.author.guild_permissions.move_members
        )

    @staticmethod
    def required(ctx: commands.Context):
        """Method which returns required votes based on amount of members in a channel."""
        vc: Player = ctx.voice_client
        channel = vc.channel
        required = (
            math.ceil((len(channel.members) - 1) / 2.5)
            if len(channel.members) != 3
            else 1
        )

        return required

    async def cog_before_invoke(self, ctx: commands.Context) -> None or discord.Message:
        """Coroutine called before command invocation."""
        if ctx.command.name in ["play", "connect"]:
            return

        if not ctx.voice_client:
            # If the bot isn't in a voice channel
            raise errors.PlayerNotConnected

        if not ctx.author.voice:
            raise errors.NoChannelProvided(channel_type="voice")

        if ctx.voice_client and ctx.author.voice.channel != ctx.voice_client.channel:
            raise errors.IncorrectChannel(
                message_author=ctx.author, channel=ctx.voice_client.channel
            )

    @commands.guild_only()
    @commands.slash_command()
    async def play(
        self,
        ctx,
        query: str,
        position: discord.Option(
            str, "position", choices=["start", "end"], required=False, default="end"
        ),
    ):
        """Searches and plays a song from a given query.

        See title. Supports YouTube, SoundCloud, and Spotify, streaming from custom urls and probably more.

        Options:
            query: The query to search for.
            position (optional): The position to put the song at in the queue. If not provided, defaults to the end.
        """
        query = query.strip("<>")

        await ctx.respond(f"**:mag_right: Searching for songs with query `{query}`.**")

        # If the voice client doesn't exist, create one.
        if not ctx.voice_client:
            player = Player(ctx=ctx)
            vc: Player = await ctx.author.voice.channel.connect(cls=player)
        else:
            vc: Player = ctx.voice_client

        track_title = None

        # If the query is not a URL, try to search for it on YouTube.
        if not self.url_reg.match(query):
            try:
                track = await wavelink.YouTubeTrack.search(
                    query=query, return_first=True
                )
                await vc.put_in_queue(track, position)
                track_title = track.title
            except IndexError:
                raise errors.SongNotFound
        else:
            try:
                # Try to determine if the query is a Spotify url.
                decoded = spotify.decode_url(query)
                if decoded:
                    # If it is, do the appropriate thing depending on the type.
                    if decoded["type"] == spotify.SpotifySearchType.track:
                        track = await spotify.SpotifyTrack.search(
                            query=decoded["id"], return_first=True
                        )
                        await vc.put_in_queue(track, position)
                        track_title = track.title
                    elif decoded["type"] == spotify.SpotifySearchType.playlist:
                        async for track in spotify.SpotifyTrack.iterator(
                            query=decoded["id"], partial_tracks=True
                        ):
                            await vc.put_in_queue(track, position)
                            track_title = query
                    elif decoded["type"] == spotify.SpotifySearchType.album:
                        async for track in spotify.SpotifyTrack.iterator(
                            query=decoded["id"],
                            type=spotify.SpotifySearchType.album,
                            partial_tracks=True,
                        ):
                            await vc.put_in_queue(track, position)
                            track_title = query
                    # If it's something like an artist, return an error.
                    elif decoded["type"] == spotify.SpotifySearchType.unusable:
                        return await ctx.send("**:x: Invalid Spotify URL type.**")
                else:
                    # If the query is a YouTube URL, take the appropriate action(s).
                    if self.yt_url_reg.match(query):
                        # If the query is a YouTube playlist, add all the songs.
                        if self.yt_playlist_reg.match(query):
                            playlist = await vc.node.get_playlist(
                                wavelink.YouTubePlaylist, query
                            )
                            for track in playlist.tracks:
                                await vc.put_in_queue(track, position)
                            track_title = playlist.name
                        # Else, it is a song. Just add it.
                        else:
                            # Just add the song.
                            track = await vc.node.get_tracks(
                                query=query, cls=wavelink.YouTubeTrack
                            )
                            track = track[0]
                            await vc.put_in_queue(track, position)
                            track_title = track.title
                    # If the query is a Soundcloud song, add it. Playlists are not supported.
                    elif self.sc_url_reg.match(query):
                        # Just add the song.
                        track = await vc.node.get_tracks(
                            query=query, cls=wavelink.SoundCloudTrack
                        )
                        track = track[0]
                        await vc.put_in_queue(track, position)
                        track_title = track.title
                    # The query is from a different website, load all the tracks and add them.
                    else:
                        # If it's not a playlist, just add the song(s).
                        tracks = await vc.node.get_tracks(
                            query=query, cls=wavelink.Track
                        )
                        for track in tracks:
                            await vc.put_in_queue(track, position)
                        track_title = query
            except (wavelink.LoadTrackError, wavelink.LavalinkException):
                raise errors.SongNotFound

        if not vc.is_playing():
            await vc.do_next()
            await ctx.send(f"**Now playing: `{track_title}`**")
        else:
            await ctx.send(f"**Added to queue: `{track_title}`**")

    @commands.guild_only()
    @commands.slash_command()
    async def pause(self, ctx):
        """Pause the currently playing song.

        Nothing more, nothing less.
        """
        vc: Player = ctx.voice_client

        if vc.is_paused():
            return await ctx.respond("**:x: The player is already paused.**")

        if self.is_privileged(ctx):
            vc.pause_votes.clear()
            await vc.pause()
            return await ctx.respond(
                "**:pause_button: An admin or DJ has paused the player.**"
            )

        required = self.required(ctx)

        vc.pause_votes.add(ctx.author)

        if len(vc.pause_votes) >= required:
            vc.pause_votes.clear()
            await vc.pause()
            return await ctx.respond(
                "**:white_check_mark: Vote to pause passed. Pausing player.**"
            )
        await ctx.respond(
            f"**:white_check_mark: {ctx.author.mention} has voted to pause the player.**"
        )

    @commands.guild_only()
    @commands.slash_command()
    async def resume(self, ctx):
        """Resume a currently paused player.

        I honestly have no idea what to put here.
        """
        vc: Player = ctx.voice_client

        if not vc.is_paused():
            return await ctx.respond("**:x: The player is not paused.**")

        if self.is_privileged(ctx):
            vc.resume_votes.clear()
            await vc.resume()
            return await ctx.respond(
                "**:arrow_forward: An admin or DJ has resumed the player.**"
            )

        required = self.required(ctx)

        vc.resume_votes.add(ctx.author)

        if len(vc.resume_votes) >= required:
            vc.resume_votes.clear()
            await vc.resume()
            return await ctx.respond(
                "**:white_check_mark: Vote to resume passed. Resuming player.**"
            )
        await ctx.respond(
            f"**:white_check_mark: {ctx.author.mention} has voted to resume the player.**"
        )

    @commands.guild_only()
    @commands.slash_command()
    async def skip(self, ctx):
        """Skip the currently playing song.

        This will not skip if there is no song playing.
        """
        vc: Player = ctx.voice_client

        if self.is_privileged(ctx):
            vc.skip_votes.clear()
            await vc.stop()
            return await ctx.respond(
                "**:track_next: An admin or DJ has skipped the song.**"
            )

        required = self.required(ctx)

        vc.skip_votes.add(ctx.author)

        if len(vc.skip_votes) >= required:
            vc.skip_votes.clear()
            await vc.stop()
            return await ctx.respond(
                "**:white_check_mark: Vote to skip passed. Skipping song.**"
            )
        await ctx.respond(
            f"**:white_check_mark: {ctx.author.mention} has voted to skip the song.**"
        )

    @commands.guild_only()
    @commands.slash_command()
    async def disconnect(self, ctx):
        """Disconnects the player from the voice channel and clears its queue.

        This will not disconnect if there is no player connected.
        """
        vc: Player = ctx.voice_client

        if self.is_privileged(ctx):
            vc.stop_votes.clear()
            await vc.teardown()
            return await ctx.respond("**:white_check_mark: Disconnected.**")

        required = self.required(ctx)
        vc.stop_votes.add(ctx.author)

        if len(vc.stop_votes) >= required:
            await ctx.send(
                "**:white_check_mark: Vote to stop passed. Stopping the player.**"
            )
            await vc.teardown()
        await ctx.send(
            f"**:white_check_mark: {ctx.author.mention} has voted to stop the player.**"
        )

    @commands.guild_only()
    @commands.slash_command()
    async def volume(self, ctx, vol: int = None):
        """Change the player's volume, between 1 and 100.

        If no volume is provided, the current volume will be displayed.

        Options:
            vol (option): The volume to set the player to.
        """
        vc: Player = ctx.voice_client

        if not self.is_privileged(ctx):
            return await ctx.send(
                "**:x: Only the DJ or admins may change the volume.**"
            )

        if not vol:
            return await ctx.respond(
                f"**:loud_sound: The volume is currently set to {vc.volume}%**"
            )

        if not 0 < vol <= 100:
            return await ctx.respond("**:x: Please enter a value between 1 and 100.**")

        # Set the volume and respond.
        await vc.set_volume(vol)
        await ctx.respond(f"**:level_slider: Set volume to {vol}%**")

    @commands.guild_only()
    @commands.slash_command()
    async def shuffle(self, ctx):
        """Shuffle the player's queue.

        *insert interesting text here.*
        """
        vc: Player = ctx.voice_client

        if vc.queue.count < 3:
            return await ctx.respond("**:x: The queue is too short to shuffle.**")

        if self.is_privileged(ctx):
            vc.shuffle_votes.clear()
            random.shuffle(vc.queue._queue)
            return await ctx.respond("**:white_check_mark: Shuffled the playlist.**")

        required = self.required(ctx)

        vc.shuffle_votes.add(ctx.author)

        if len(vc.shuffle_votes) >= required:
            vc.shuffle_votes.clear()
            random.shuffle(vc.queue._queue)
            return await ctx.respond("**:white_check_mark: Shuffled the playlist.**")
        await ctx.respond(
            f"**:white_check_mark: {ctx.author.mention} has voted to shuffle the playlist.**"
        )

    @commands.guild_only()
    @commands.slash_command()
    async def seek(self, ctx, time_in_seconds: int):
        """Seeks to a certain point in the currently playing song.

        Great if you want to listen to the good part of a song.

        Options:
            time_in_seconds: The time in seconds to seek to.
        """
        vc: Player = ctx.voice_client

        time = time_in_seconds * 1000

        if self.is_privileged(ctx):
            vc.seek_votes.clear()
            await vc.seek(time)
            return await ctx.respond(
                f"**:left_right_arrow: Set position to `{time_in_seconds}`**"
            )

        required = self.required(ctx)

        vc.seek_votes.add(ctx.author)

        if len(vc.seek_votes) >= required:
            vc.seek_votes.clear()
            await vc.seek(time)
            return await ctx.respond(
                f"**:left_right_arrow: Set position to `{time_in_seconds}`**"
            )
        await ctx.respond(
            f"**:left_right_arrow: {ctx.author.mention} has voted to set the player position to `{time_in_seconds}`**"
        )

    @commands.guild_only()
    @commands.slash_command()
    async def forward(self, ctx, time_in_seconds: int):
        """Forwards by a certain amount of time in the currently playing song.

        Quite simple, isn't it?

        Options:
            time_in_seconds: The time in seconds to forward by.
        """
        vc: Player = ctx.voice_client

        time = (round(vc.position) + time_in_seconds) * 1000

        if self.is_privileged(ctx):
            vc.forward_votes.clear()
            await vc.seek(time)
            return await ctx.respond(
                f"**:fast_forward: Set position to `{round(time/1000)}`**"
            )

        required = self.required(ctx)

        vc.forward_votes.add(ctx.author)

        if len(vc.forward_votes) >= required:
            vc.forward_votes.clear()
            await vc.seek(time)
            return await ctx.respond(
                f"**:fast_forward: Set position to `{round(time/1000)}`**"
            )
        await ctx.respond(f"**:fast_forward: Set position to `{round(time/1000)}`**")

    @commands.guild_only()
    @commands.slash_command()
    async def rewind(self, ctx, time_in_seconds: int):
        """Rewinds by a certain amount of time in the currently playing song.

        Same as forward, but backwards. Or was it forwards? Or backwards? I don't know.

        Options:
            time_in_seconds: The time in seconds to rewind by.
        """
        vc: Player = ctx.voice_client

        time = (round(vc.position) - time_in_seconds) * 1000

        if self.is_privileged(ctx):
            vc.rewind_votes.clear()
            await vc.seek(time)
            return await ctx.respond(
                f"**:rewind: Set position to `{round(time/1000)}`**"
            )

        required = self.required(ctx)

        vc.rewind_votes.add(ctx.author)

        if len(vc.rewind_votes) >= required:
            vc.rewind_votes.clear()
            await vc.seek(time)
            return await ctx.respond(
                f"**:rewind: Set position to `{round(time/1000)}`**"
            )
        await ctx.respond(f"**:rewind:Set position to `{round(time/1000)}`**")

    @commands.guild_only()
    @commands.slash_command()
    async def swap_dj(self, ctx: commands.Context, *, member: discord.Member = None):
        """Swap the current DJ to another member in the voice channel.

        Options:
            member (option): The member to swap the DJ to. If not provided, a random member will be chosen.
        """
        vc: Player = ctx.voice_client

        if not self.is_privileged(ctx):
            return await ctx.send(
                "**:x: Only admins and the DJ may use this command.**"
            )

        if member and member not in ctx.voice_client.channel.members:
            return await ctx.send(
                f"**:x: {member} is not currently in voice, so can not be a DJ.**"
            )

        if member and member == vc.dj:
            return await ctx.send("**:x: Cannot swap DJ to the current DJ :)**")

        if len(ctx.voice_client.channel.members) <= 2:
            return await ctx.send("**:x: No other members to swap to.**")

        if member:
            vc.dj = member
            return await ctx.send(
                f"**:control_knobs: {member.mention} is now the DJ.**"
            )

        while not member:
            member = random.choice(ctx.voice_client.channel.members)
            if member.bot:
                member = None
                continue
            return await ctx.send(
                f"**:control_knobs: {member.mention} is now the DJ.**"
            )

    @commands.guild_only()
    @commands.slash_command()
    async def queue(self, ctx):
        """Display the player's queued songs.

        Now you can show all the fantastic songs you have queued up to your mates.
        """
        vc: Player = ctx.voice_client

        if vc.queue.count == 0:
            return await ctx.respond("**:x: There are no more songs in the queue.**")

        entries = list(vc.queue._queue)
        queue = [entries[i : i + 8] for i in range(0, vc.queue.count, 8)]
        page_list = []
        count = 0

        for page_number, tracks in enumerate(queue):
            embed = discord.Embed(
                title="Coming up...",
                description="\n".join(
                    [
                        f"{idx + count}. **[`{track.title}`]({track.uri})**\n"
                        if hasattr(track, "uri")
                        else f"{idx + count}. **`{track.title}`**\n"
                        for idx, track in enumerate(tracks, start=1)
                    ]
                ),
                colour=self.emb_colour,
            )

            embed.set_footer(
                text=f"Page {page_number + 1}/{len(queue)}",
                icon_url=self.bot.user.display_avatar.url,
            )

            page_list.append(embed)

            count += 8

        paginator = pages.Paginator(
            pages=page_list, show_disabled=False, show_indicator=True
        )

        await paginator.respond(ctx.interaction, ephemeral=False)

    @commands.guild_only()
    @commands.slash_command()
    async def remove(self, ctx, track: int):
        """Removes the specified track from the queue.

        You can use this to remove a song from the queue if you don't like it.

        Options:
            track: The number of the track to remove.
        """
        vc: Player = ctx.voice_client

        # Due to how indexing works, we need to subtract 1 from the song number
        track_index = track - 1
        try:
            track = vc.queue[track_index]
        except IndexError:
            return await ctx.respond(
                f"**:x: Track number {track} could not be found in the queue.**"
            )

        if self.is_privileged(ctx):
            vc.remove_votes.clear()
            vc.queue.__delitem__(track_index)

            return await ctx.respond(
                f"**:outbox_tray: An admin or DJ has removed `{track.title}` from the queue.**"
            )

        required = self.required(ctx)

        vc.remove_votes.add(ctx.author)

        if len(vc.remove_votes) >= required:
            vc.queue.__delitem__(track_index)
            await ctx.respond(
                f"**:white_check_mark: Vote to remove passed. Removed `{track.title}` from the queue.**"
            )
        else:
            await ctx.respond(
                f"**:white_check_mark: {ctx.author.mention} has voted to remove `{track.title}` from the queue.**"
            )

    @commands.guild_only()
    @commands.slash_command()
    async def nowplaying(self, ctx):
        """Sends an embed with information about the currently playing song.

        Why did I decide to write very useful text here again?
        """
        vc: Player = ctx.voice_client

        if vc.is_playing:
            # Create embed
            embed = discord.Embed(title="Now playing", colour=self.emb_colour)
            embed.description = (
                f"**[`{vc.track.title}`]({vc.track.uri})**\n\n"
                if vc.track.uri
                else f"**`{vc.track.title}`**\n\n"
            )
            try:
                embed.set_thumbnail(url=vc.track.thumbnail)
            except AttributeError:
                pass

            embed.add_field(
                name="Playing for",
                value=f"{round(vc.position)}s/{round(vc.track.duration)}s",
            )
            embed.add_field(
                name="Author",
                value=f"`{vc.track.author if vc.track.author else 'Unknown'}`",
            )
            embed.add_field(name="Queue Length", value=str(vc.queue.count))
            embed.add_field(name="Volume", value=f"**`{vc.volume}%`**")
            embed.add_field(name="DJ", value=vc.dj.mention)
            embed.add_field(name="Channel", value=f"{vc.channel.mention}")

            return await ctx.respond(embed=embed)
        await ctx.respond("**:x: There is no song currently playing.**")

    @commands.guild_only()
    @commands.slash_command()
    async def connect(self, ctx):
        """Connect to a voice channel.

        See above, this command will only work if you are connected to a voice channel and the bot isn't connected to a voice channel.
        """
        if not ctx.voice_client:
            player = Player(ctx=ctx)
            vc: Player = await ctx.author.voice.channel.connect(cls=player)
            return await ctx.respond(f"**:robot: Joined {vc.channel.mention}.**")
        else:
            vc: Player = ctx.voice_client
            if vc.is_connected:
                return await ctx.respond(
                    "**:x: I'm already connected to a voice channel.**"
                )


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Music(bot))
