"""
A lot of the code here comes from the following sources (<3 to the people who made them):
- https://github.com/Devoxin/Lavalink.py/blob/master/examples/music.py
- https://github.com/PythonistaGuild/Wavelink/blob/master/examples/advanced.py

And thus this file falls under the MIT license:

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
import asyncio
import os
import json
import re
import math

import discord
import lavalink

from datetime import timedelta
from ..utils import utils, equalizers, spotify, errors
from discord.ext import commands, pages


class LavalinkVoiceClient(discord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://docs.pycord.dev/en/master/api.html#voiceprotocol
    """

    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        super().__init__(client, channel)
        self.client = client
        self.channel = channel
        # ensure there exists a client already
        if hasattr(self.client, "lavalink"):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                "localhost", 2333, "youshallnotpass", "us", "default-node"
            )
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        """Event called on voice server update."""
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        """Event called on voice state update."""
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that
        # would set channel_id to None doesn't get dispatched after the
        # disconnect
        player.channel_id = None
        self.cleanup()


class Music(commands.Cog):
    """Music related commands."""

    def __init__(self, bot):
        self.bot = bot

        self.emb_colour = int(os.getenv("COLOUR"), 16)
        self.url_reg = re.compile(r"https?://(?:www\.)?.+")

        self.bot.loop.create_task(self.start_nodes())
        lavalink.add_event_hook(self.track_hook)

    async def start_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        if not hasattr(self.bot, "lavalink"):
            self.bot.lavalink = lavalink.Client(self.bot.user.id)

        with open("lavalink.json") as f:
            nodes = json.load(f)

        for node in nodes.values():
            print(f"[NODE {node['name']}] Connecting to Lavalink instance")
            self.bot.lavalink.add_node(**node)
            print(f"[NODE {node['name']}] Node is ready!")

    def cog_unload(self):
        """Cog unload handler. This removes any event hooks that were registered."""
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """Command before-invoke handler."""
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check and ctx.command.name in ("play",):
            await self.ensure_voice(ctx)
        #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def ensure_voice(self, ctx):
        """This check ensures that the bot and command author are in the same voicechannel."""
        player = self.bot.lavalink.player_manager.create(
            ctx.guild.id, endpoint=str(ctx.guild.region)
        )
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ("play",)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise errors.NoChannelProvided(channel_type="voice")

        if not player.is_connected:
            if not should_connect:
                raise errors.PlayerNotConnected

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if (
                not permissions.connect or not permissions.speak
            ):  # Check user limit too?
                raise commands.BotMissingPermissions(["Connect", "Speak"])

            player.store("channel", ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                channel = self.bot.get_channel(int(player.channel_id))
                raise errors.IncorrectChannel(
                    message_author=ctx.author.mention, channel=channel.mention
                )

    async def track_hook(self, event):
        """Lavalink event hook for track end."""
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    def required(self, ctx: commands.Context):
        """Method which returns required votes based on amount of members in a channel."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        channel = self.bot.get_channel(int(player.channel_id))
        required = math.ceil((len(channel.members) - 1) / 2.5)

        if ctx.command.name == "stop" and len(channel.members) == 3:
            required = 2

        return required

    def is_privileged(self, ctx: commands.Context):
        """Check whether the user is an Admin or DJ."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        return (
            player.store(key="dj", value=ctx.author)
            or ctx.author.guild_permissions.kick_members
        )

    @staticmethod
    async def position(player_position: float):
        """Method which returns the player position."""
        player_position = timedelta(milliseconds=round(player_position))

        player_position = player_position - timedelta(
            microseconds=player_position.microseconds
        )

        return player_position

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Event listener for when a user changes voice state."""
        await self.bot.wait_until_ready()

        player = self.bot.lavalink.player_manager.get(member.guild.id)

        if player and before.channel:
            members = before.channel.members

            if player.is_connected and len(members) == 1:
                text_channel = player.fetch(key="channel", default=None)

                guild_id = int(player.guild_id)
                guild = self.bot.get_guild(guild_id)

                # Clear the queue to ensure old tracks don't start playing
                # when someone else queues something.
                player.queue.clear()
                # Stop the current track so Lavalink consumes less resources.
                await player.stop()
                # Disconnect from the voice channel.
                await guild.voice_client.disconnect(force=True)

                if text_channel:
                    channel = self.bot.get_channel(text_channel)
                    await channel.send(
                        "**:white_check_mark: Disconnected from voice channel due to all members leaving.**"
                    )

    @commands.guild_only()
    @commands.slash_command()
    async def connect(self, ctx):
        """Connect to a voice channel."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player and player.is_connected:
            await ctx.respond("**:x: I'm already connected to a voice channel.**")
            return

        channel = getattr(ctx.author.voice, "channel", None)
        if channel is None:
            raise errors.NoChannelProvided(channel_type="voice")

        await channel.connect(cls=LavalinkVoiceClient)

        await ctx.respond(f"**:robot: Joined `{channel.name}`.**")

    @commands.guild_only()
    @commands.slash_command()
    async def play(
        self,
        ctx,
        query: str,
        platform: discord.Option(
            str,
            "platform",
            choices=["YouTube", "Spotify", "SoundCloud"],
            required=False,
        ),
        position: discord.Option(
            str,
            "position",
            choices=["start", "end"],
            required=False,
        ),
    ):
        """Searches and plays a song from a given query."""
        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        query = query.strip("<>")
        spotify_query = None

        # Check if the user input might be a URL. If it isn't, we can make Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not self.url_reg.match(query):
            if platform == "SoundCloud":
                query = f"scsearch:{query}"
            elif platform == "Spotify":
                spotify_query = await spotify.fetch(name=query)
                query = f"ytsearch:{spotify_query[0].name} {spotify_query[0].artist}"
            else:
                query = f"ytsearch:{query}"

        # God this is ugly, but it works for now.
        if not spotify_query:
            # If the platform is Spotify, and the query is a URL, we can use the URL directly.
            if platform == "Spotify":
                spotify_query = await spotify.fetch(url=query)
                query = f"ytsearch:{spotify_query[0].name} {spotify_query[0].artist}"

            # If it turns out to be a Spotify URL, but the user did not specify a platform, we can use the URL directly.
            try:
                spotify_query = await spotify.fetch(url=query)
                query = f"ytsearch:{spotify_query[0].name} {spotify_query[0].artist}"
                platform = "Spotify"
            except errors.SongNotFound:
                pass

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # Alternatively, results['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results["tracks"]:
            raise errors.SongNotFound

        embed = discord.Embed(colour=self.emb_colour)

        channel = self.bot.get_channel(int(player.channel_id))
        dj = player.fetch(key="dj", default=None)

        if not dj:
            dj = ctx.author
            player.store(key="dj", value=ctx.author)

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results["loadType"] == "PLAYLIST_LOADED":
            tracks = results["tracks"]

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(
                    requester=ctx.author.id, track=track, index=0 if position else None
                )

            embed.title = "Added playlist to queue"
            embed.description = f'**[`{results["playlistInfo"]["name"]}`]({query})**'

            thumb = await utils.fetch_thumbnail(
                results["tracks"][0]["info"]["identifier"]
            )
            qsize = len(player.queue)

            embed.add_field(name="Tracks", value=str(len(tracks)))
            embed.add_field(name="Queue Length", value=str(qsize + 1))
            embed.add_field(name="Volume", value=f"**`{player.volume}%`**")
            embed.add_field(name="Requested By", value=ctx.author.mention)
            embed.add_field(name="DJ", value=dj.mention)
            embed.add_field(name="Channel", value=f"{channel.mention}")
        else:
            if platform == "Spotify":
                loading_message = await utils.loading_message()

                add_song_embed = discord.Embed(
                    title="Adding songs to queue...",
                    description=loading_message,
                    colour=self.emb_colour,
                )

                add_song_msg = await ctx.respond(embed=add_song_embed)

                tracks_added = 0

                # This will basically DoS your Lavalink if it is a remotely large playlist, so be careful.
                # I have not found a better way to do this, but it would be a livesafer if you could request
                # to add multiple songs at once.
                for track in spotify_query:
                    query = f"ytsearch:{track.name} {track.artist}"
                    results = await player.node.get_tracks(query)

                    track = results["tracks"][0]
                    track = lavalink.models.AudioTrack(
                        track, ctx.author.id, recommended=True
                    )

                    player.add(
                        requester=ctx.author.id,
                        track=track,
                        index=0 if position else None,
                    )

                    # If no song is currently playing, already play one of the songs since this could take a very
                    # long time.
                    if not player.is_connected and not player.channel_id:
                        break
                    if not player.is_playing:
                        await player.play()

                        await ctx.send(
                            "I will already start playing the requested songs whilst adding them to the queue."
                        )

                        temp_embed = discord.Embed(colour=self.emb_colour)

                        temp_embed.title = "Added track to queue"

                        # I am aware that this is duplicate code.

                        thumb = await utils.fetch_thumbnail(
                            results["tracks"][0]["info"]["identifier"]
                        )
                        qsize = len(player.queue)

                        temp_embed.add_field(
                            name="Tracks", value=str(len(spotify_query))
                        )
                        temp_embed.add_field(
                            name="Queue Length", value=str(qsize + len(spotify_query))
                        )
                        temp_embed.add_field(
                            name="Volume", value=f"**`{player.volume}%`**"
                        )
                        temp_embed.add_field(
                            name="Requested By", value=ctx.author.mention
                        )
                        temp_embed.add_field(name="DJ", value=dj.mention)
                        temp_embed.add_field(name="Channel", value=f"{channel.mention}")

                        if thumb:
                            temp_embed.set_thumbnail(url=thumb)

                        await ctx.send(embed=temp_embed)

                    tracks_added += 1

                await add_song_msg.delete_original_message()

                embed.title = f"Added {tracks_added} track(s) to queue"

                # I am aware that this is duplicate code.

                thumb = await utils.fetch_thumbnail(
                    results["tracks"][0]["info"]["identifier"]
                )
                qsize = len(player.queue)

                embed.add_field(name="Tracks", value=str(tracks_added))
                embed.add_field(name="Queue Length", value=str(qsize))
                embed.add_field(name="Volume", value=f"**`{player.volume}%`**")
                embed.add_field(name="Requested By", value=ctx.author.mention)
                embed.add_field(name="DJ", value=dj.mention)
                embed.add_field(name="Channel", value=f"{channel.mention}")

            else:
                track = results["tracks"][0]
                embed.title = "Added track to queue"
                embed.description = (
                    f'**[`{track["info"]["title"]}`]({track["info"]["uri"]})**'
                )

                thumb = await utils.fetch_thumbnail(track["info"]["identifier"])
                qsize = len(player.queue)

                embed.add_field(
                    name="Duration",
                    value=str(
                        await utils.chop_microseconds(
                            timedelta(milliseconds=int(track["info"]["length"]))
                        )
                    ),
                )
                embed.add_field(name="Queue Length", value=str(qsize + 1))
                embed.add_field(name="Volume", value=f"**`{player.volume}%`**")
                embed.add_field(name="Requested By", value=ctx.author.mention)
                embed.add_field(name="DJ", value=dj.mention)
                embed.add_field(name="Channel", value=f"{channel.mention}")

                # You can attach additional information to audiotracks through kwargs, however this involves
                # constructing the AudioTrack class yourself.
                track = lavalink.models.AudioTrack(
                    track, ctx.author.id, recommended=True
                )
                player.add(
                    requester=ctx.author.id, track=track, index=0 if position else None
                )

        if thumb:
            embed.set_thumbnail(url=thumb)

        await ctx.respond(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

    @commands.guild_only()
    @commands.slash_command()
    async def pause(self, ctx):
        """Pause the currently playing song."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.paused:
            await ctx.respond("**:x: The player is already paused.**")
            return

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if self.is_privileged(ctx):
            await ctx.respond(
                "**:pause_button: An admin or DJ has paused the player.**"
            )
            player.delete(key="pause_votes")

            await player.set_pause(True)
            return

        required = self.required(ctx)

        pause_votes = player.fetch(key="pause_votes", default=[])
        pause_votes.append(ctx.author)
        player.store(key="pause_votes", value=pause_votes)

        if len(pause_votes) >= required:
            await ctx.respond(
                "**:white_check_mark: Vote to pause passed. Pausing player.**"
            )
            player.delete(key="pause_votes")
            await player.set_pause(True)
        else:
            await ctx.respond(
                f"**:white_check_mark: {ctx.author.mention} has voted to pause the player.**"
            )

    @commands.guild_only()
    @commands.slash_command()
    async def resume(self, ctx):
        """Resume a currently paused player."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.paused:
            await ctx.respond("**:x: The player is not paused.**")
            return

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if self.is_privileged(ctx):
            await ctx.respond(
                "**:arrow_forward: An admin or DJ has resumed the player.**"
            )
            player.delete(key="resume_votes")

            await player.set_pause(False)
            return

        required = self.required(ctx)

        resume_votes = player.fetch(key="resume_votes", default=[])
        resume_votes.append(ctx.author)
        player.store(key="resume_votes", value=resume_votes)

        if len(resume_votes) >= required:
            await ctx.respond(
                "**:white_check_mark: Vote to resume passed. Resuming player.**"
            )
            player.delete(key="resume_votes")
            await player.set_pause(False)
        else:
            await ctx.respond(
                f"**:white_check_mark: {ctx.author.mention} has voted to resume the player.**"
            )

    @commands.guild_only()
    @commands.slash_command()
    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if self.is_privileged(ctx):
            await ctx.respond("**:track_next: An admin or DJ has skipped the song.**")
            player.delete(key="skip_votes")

            await player.skip()
            return

        if ctx.author == player.current.requester:
            await ctx.respond(
                "**:track_next: The song requester has skipped the song.**"
            )
            player.delete(key="skip_votes")

            await player.skip()
            return

        required = self.required(ctx)

        skip_votes = player.fetch(key="skip_votes", default=[])
        skip_votes.append(ctx.author)
        player.store(key="skip_votes", value=skip_votes)

        if len(skip_votes) >= required:
            await ctx.respond(
                "**:white_check_mark: Vote to skip passed. Skipping song.**"
            )
            player.delete(key="skip_votes")
            await player.skip()
        else:
            await ctx.respond(
                f"**:white_check_mark: {ctx.author.mention} has voted to skip the song.**"
            )

    @commands.guild_only()
    @commands.slash_command()
    async def disconnect(self, ctx):
        """Disconnects the player from the voice channel and clears its queue."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not ctx.author.voice or (
            player.is_connected
            and ctx.author.voice.channel.id != int(player.channel_id)
        ):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            await ctx.respond("You're not in my voicechannel!")
            return

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await ctx.voice_client.disconnect(force=True)
        await ctx.respond("**:white_check_mark: Disconnected.**")

    @commands.guild_only()
    @commands.slash_command()
    async def volume(self, ctx, vol: int = None):
        """Change the player's volume, between 1 and 100."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if not vol:
            await ctx.respond(
                f"**:loud_sound: The volume is currently set to {player.volume}%**"
            )
            return

        if not self.is_privileged(ctx):
            await ctx.respond("**:x: Only the DJ or admins may change the volume.**")
            return

        if not 0 < vol < 1001:
            await ctx.respond("**:x: Please enter a value between 1 and 1000.**")
            return

        await player.set_volume(vol)
        await ctx.respond(f"**:level_slider: Set volume to {vol}%**")

    @commands.guild_only()
    @commands.slash_command()
    async def shuffle(self, ctx):
        """Shuffle the player's queue."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        qsize = len(player.queue)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if qsize < 3:
            await ctx.respond("**:x: Add more songs to the queue before shuffling.**")
            return

        if self.is_privileged(ctx):
            if not player.shuffle:
                player.set_shuffle(True)
                await ctx.respond("**:twisted_rightwards_arrows: Shuffling enabled.**")
            else:
                player.set_shuffle(False)
                await ctx.respond("**:twisted_rightwards_arrows: Shuffling disabled.**")
            player.delete(key="shuffle_votes")
            return

        required = self.required(ctx)

        shuffle_votes = player.fetch(key="shuffle_votes", default=[])
        shuffle_votes.append(ctx.author)
        player.store(key="shuffle_votes", value=shuffle_votes)

        if len(player.shuffle_votes) >= required:
            player.delete(key="shuffle_votes")
            if not player.shuffle:
                player.set_shuffle(True)
                await ctx.respond(
                    "****:twisted_rightwards_arrows: Vote to shuffle passed. Shuffling enabled.**"
                )
            else:
                player.set_shuffle(False)
                await ctx.respond(
                    "**:twisted_rightwards_arrows: Vote to shuffle passed. Shuffling disabled.**"
                )
        else:
            await ctx.respond(
                f"**:white_check_mark: {ctx.author.mention} has voted to shuffle the playlist.**"
            )

    @commands.guild_only()
    @commands.slash_command()
    async def equalizer(
        self,
        ctx,
        equalizer: discord.Option(
            str, "profile", choices=["flat", "boost", "metal", "piano"]
        ),
    ):
        """Changes the player's equalizer."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if not self.is_privileged(ctx):
            await ctx.respond("**:x: Only the DJ or admins may change the equalizer.**")
            return

        eqs = {
            "flat": equalizers.Equalizer.flat(),
            "boost": equalizers.Equalizer.boost(),
            "metal": equalizers.Equalizer.metal(),
            "piano": equalizers.Equalizer.piano(),
        }

        eq = eqs.get(equalizer.lower())

        if not eq:
            joined = "\n• ".join(eqs.keys())
            await ctx.respond(f"**:x: Invalid EQ provided.** Valid EQs:\n\n• {joined}")
            return

        await ctx.respond(
            f"**:control_knobs: Successfully changed equalizer to {equalizer}.**"
        )
        await player.set_gains(*eq.raw)

    @commands.guild_only()
    @commands.slash_command()
    async def nowplaying(self, ctx):
        """Sends an embed with information about the currently playing song."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        dj = player.fetch(key="dj", default=ctx.author)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        channel = self.bot.get_channel(int(player.channel_id))
        qsize = len(player.queue)

        track = player.current

        thumb = await utils.fetch_thumbnail(track.identifier)

        player_position = await self.position(player.position)

        # Create embed

        embed = discord.Embed(title="Now playing", colour=self.emb_colour)
        embed.description = f"**[`{track.title}`]({track.uri})**\n\n"
        if thumb:
            embed.set_thumbnail(url=thumb)

        embed.add_field(
            name="Playing for",
            value=f"`{player_position}/{timedelta(milliseconds=int(track.duration))}`",
        )
        embed.add_field(name="Queue Length", value=str(qsize + 1))
        embed.add_field(name="Volume", value=f"**`{player.volume}%`**")
        embed.add_field(name="Requested By", value=f"<@{player.current.requester}>")
        embed.add_field(name="DJ", value=dj.mention)
        embed.add_field(name="Channel", value=f"{channel.mention}")

        await ctx.respond(embed=embed)

    @commands.guild_only()
    @commands.slash_command()
    async def seek(self, ctx, time_in_seconds: int):
        """Seeks to a certain point in the currently playing song."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        time = time_in_seconds * 1000

        await player.seek(position=time)

        player_position = timedelta(milliseconds=time)

        await ctx.respond(f"**:left_right_arrow: Set position to `{player_position}`**")

    @commands.guild_only()
    @commands.slash_command()
    async def forward(self, ctx, time_in_seconds: int):
        """Forwards by a certain amount of time in the currently playing song."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        player_position = await self.position(player.position)

        time = (player_position.seconds + time_in_seconds) * 1000

        await player.seek(position=time)

        player_position = timedelta(milliseconds=time)

        await ctx.respond(f"**:fast_forward: Set position to `{player_position}`**")

    @commands.guild_only()
    @commands.slash_command()
    async def rewind(self, ctx, time_in_seconds: int):
        """Rewinds by a certain amount of time in the currently playing song."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        player_position = await self.position(player.position)

        time = (player_position.seconds - time_in_seconds) * 1000

        await player.seek(position=time)

        player_position = timedelta(milliseconds=time)

        await ctx.respond(f"**:rewind: Set position to `{player_position}`**")

    @commands.guild_only()
    @commands.slash_command()
    async def swap_dj(self, ctx, member: discord.Member = None):
        """Swap the current DJ to another member in the voice channel."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if not self.is_privileged(ctx):
            await ctx.respond("**:x: Only admins and the DJ may use this command.**")
            return

        members = self.bot.get_channel(int(player.channel_id)).members
        dj = player.fetch(key="dj", default=ctx.author)

        if member and member not in members:
            await ctx.respond(
                f"**:x: {member} is not currently in voice, so can not be a DJ.**"
            )
            return

        if member and member == dj:
            await ctx.respond("**:x: Cannot swap DJ to the current DJ... :)**")
            return

        if len(members) <= 2:
            await ctx.respond("**:x: No more members to swap to.**")
            return

        if member:
            player.store(key="dj", value=member)
            await ctx.respond(f"**:control_knobs: {member.mention} is now the DJ.**")
            return

        for m in members:
            if m == dj or m.bot:
                continue
            player.store(key="dj", value=member)
            await ctx.respond(f"**:control_knobs: {member.mention} is now the DJ.**")
            return

    @commands.guild_only()
    @commands.slash_command()
    async def queue(self, ctx):
        """Display the player's queued songs."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        qsize = len(player.queue)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        if qsize == 0:
            await ctx.respond("**:x: There are no more songs in the queue.**")
            return

        queue = [player.queue[i : i + 8] for i in range(0, len(player.queue), 8)]
        page_list = []
        count = 0

        for page_number, tracks in enumerate(queue):
            embed = discord.Embed(
                title="Coming up...",
                description="\n".join(
                    [
                        f"{idx + count}. **[`{track.title}`]({track.uri})**\n"
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
        """Removes the specified track from the queue."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise errors.PlayerNotConnected

        # Due to how indexing works, we need to subtract 1 from the song number
        track_index = track - 1
        try:
            track = player.queue[track_index]
        except IndexError:
            await ctx.respond(
                f"**:x: Track number {track} could not be found in the queue.**"
            )
            return

        if self.is_privileged(ctx):
            player.queue.remove(track)

            await ctx.respond(
                f"**:outbox_tray: An admin or DJ has removed `{track.title}` from the queue.**"
            )
            return

        if ctx.author == track.requester:
            player.queue.remove(track)

            await ctx.respond(
                f"**:outbox_tray: The song requester has removed `{track.title}` from the queue.**"
            )
            return

        required = self.required(ctx)

        remove_votes = player.fetch(key="remove_votes", default=[])
        remove_votes.append(ctx.author)
        player.store(key="remove_votes", value=remove_votes)

        if len(remove_votes) >= required:
            player.queue.remove(track)
            await ctx.respond(
                f"**:white_check_mark: Vote to remove passed. Removed `{track.title}` from the queue.**"
            )
        else:
            await ctx.respond(
                f"**:white_check_mark: {ctx.author.mention} has voted to remove `{track.title} from the queue`.**"
            )


def setup(bot: commands.Bot):
    """Add cog to bot"""
    bot.add_cog(Music(bot))
