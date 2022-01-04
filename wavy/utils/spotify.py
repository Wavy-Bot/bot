import os

from urllib.parse import urlparse
from . import classes, errors
from async_spotify import SpotifyApiClient
from async_spotify.authentification.authorization_flows import ClientCredentialsFlow
from dotenv import load_dotenv

load_dotenv()

auth_flow = ClientCredentialsFlow(
    application_id=os.environ["SPOTIFY_CLIENT_ID"],
    application_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
)
auth_flow.load_from_env()

client = SpotifyApiClient(auth_flow, hold_authentication=True)


async def fetch(url: str = None, name: str = None) -> [classes.SpotifyTrack]:
    """
    Fetches a track, album or playlist.

    Takes the following arguments:
        url => The URL of the track, album or playlist.
        name => The name of the track.
    """
    if url:
        parsed_url = await parse_url(url)
        if parsed_url.type == "track":
            track = await fetch_track(parsed_url.id)
            return [track]
        elif parsed_url.type == "album":
            album = await fetch_album(parsed_url.id)
            return album
        elif parsed_url.type == "playlist":
            playlist = await fetch_playlist(parsed_url.id)
            return playlist
        else:
            raise errors.SongNotFound
    else:
        track = await search_track(name)
        return [track]


async def parse_url(url: str) -> classes.ParsedSpotifyURL:
    """Parses a Spotify URL and returns the data."""
    url = urlparse(url)

    if url.scheme in ["http", "https"]:
        path = url.path.split("/")
    elif url.scheme == "spotify":
        path = url.path.split(":")
    else:
        raise errors.SongNotFound

    spotify_id = path[-1]
    id_type = path[-2]

    parsed_class = classes.ParsedSpotifyURL(id=spotify_id, type=id_type)

    return parsed_class


async def fetch_track(track_id: str) -> classes.SpotifyTrack:
    """
    Fetches a track and returns a SpotifyTrack class.

    Takes the following arguments:
        track_id => The ID of the track.
    """
    auth_token = await client.get_auth_token_with_client_credentials()
    await client.create_new_client()

    track = await client.track.get_one(track_id=track_id, auth_token=auth_token)
    await client.close_client()

    track_class = classes.SpotifyTrack(
        name=track["name"],
        artist=track["artists"][0]["name"],
        image=track["album"]["images"][0]["url"],
        url=track["external_urls"]["spotify"],
    )

    return track_class


async def search_track(track_name: str) -> classes.SpotifyTrack:
    """
    Searches for a track and returns a SpotifyTrack class.

    Takes the following arguments:
        track_name => The name of the track.
    """
    auth_token = await client.get_auth_token_with_client_credentials()
    await client.create_new_client()

    query = await client.search.start(
        query=track_name, query_type=["track"], auth_token=auth_token
    )
    await client.close_client()

    if not query["tracks"]["items"]:
        raise errors.SongNotFound

    track = query["tracks"]["items"][0]

    track_class = classes.SpotifyTrack(
        name=track["name"],
        artist=track["artists"][0]["name"],
        image=track["album"]["images"][0]["url"],
        url=track["external_urls"]["spotify"],
    )

    return track_class


async def fetch_album(album_id: str) -> [classes.SpotifyTrack]:
    """
    Fetches an album and returns a SpotifyTrack class.

    Takes the following arguments:
        album_id => The ID of the album.
    """
    auth_token = await client.get_auth_token_with_client_credentials()
    await client.create_new_client()

    # TODO(Robert): Fix that this function only returns 100 tracks.
    album = await client.albums.get_one(album_id=album_id, auth_token=auth_token)
    tracks = await client.albums.get_tracks(album_id=album_id, auth_token=auth_token)
    await client.close_client()

    track_list = []

    for track in tracks["items"]:
        track_class = classes.SpotifyTrack(
            name=track["name"],
            artist=track["artists"][0]["name"],
            image=album["images"][0]["url"],
            url=track["external_urls"]["spotify"],
        )

        track_list.append(track_class)

    return track_list


async def fetch_playlist(playlist_id: str) -> [classes.SpotifyTrack]:
    """
    Fetches a playlist and returns a SpotifyTrack class.

    Takes the following arguments:
        playlist_id => The ID of the playlist.
    """
    auth_token = await client.get_auth_token_with_client_credentials()
    await client.create_new_client()

    # TODO(Robert): Fix that this function only returns 100 tracks.
    playlist = await client.playlists.get_tracks(
        playlist_id=playlist_id, auth_token=auth_token
    )
    await client.close_client()

    track_list = []

    for data in playlist["items"]:
        track = data["track"]
        track_class = classes.SpotifyTrack(
            name=track["name"],
            artist=track["artists"][0]["name"],
            image=track["album"]["images"][0]["url"],
            url=track["external_urls"]["spotify"],
        )

        track_list.append(track_class)

    return track_list
