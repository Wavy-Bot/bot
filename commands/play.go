package commands

import (
	"context"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/disgoorg/disgolink/v2/disgolink"
	"github.com/disgoorg/disgolink/v2/lavalink"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
	"time"
)

// PlayHandler is the handler for the play command.
// Music? In Wavy? No way! (<- Copilot thought of that)
func PlayHandler(e *handler.CommandEvent) error {
	// The track to play
	var song *lavalink.Track

	// Get the command interaction data
	var data = e.SlashCommandInteractionData()

	// Get the query from the interaction
	query := data.String("query")

	// TODO(Robert): Add support for position
	// Get the position from the interaction,
	// If the position is not provided, default to end
	//position, ok := data.OptString("position")
	//if !ok {
	//	position = "end"
	//}

	// Check if the user is in a voice channel
	// TODO(Robert): Check if the bot is in a voice channel and if the user is in the same voice channel
	voiceState, ok := dbot.B.Client.Caches().VoiceState(*e.GuildID(), e.User().ID)
	if !ok {
		return e.CreateMessage(discord.NewMessageCreateBuilder().
			SetContent("**❌ You are not in a voice channel.**").
			Build())
	}

	// Send a message saying that we are searching for songs
	if err := e.CreateMessage(discord.NewMessageCreateBuilder().
		SetContentf("**🔎 Searching for songs with query `%s`.**", query).
		Build()); err != nil {
		return err
	}

	// If the query is not a URL, add ytsearch: to the query
	if !utils.URLPattern.MatchString(query) {
		query = lavalink.SearchTypeYoutube.Apply(query)
	}

	// Set context to 10 seconds
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	dbot.B.Lavalink.Client.BestNode().LoadTracksHandler(ctx, query, disgolink.NewResultHandler(
		func(track lavalink.Track) {
			// Loaded a single track
			song = &track
		},
		func(playlist lavalink.Playlist) {
			// Loaded a playlist
			// TODO(Robert): Add playlist tracks to queue
			song = &playlist.Tracks[0]
		},
		func(tracks []lavalink.Track) {
			// Loaded a search result
			song = &tracks[0]
		},
		func() {
			// Nothing matching the query found
			// Send a message saying that nothing was found
			_, err := e.CreateFollowupMessage(discord.NewMessageCreateBuilder().
				SetContent("**❌ No songs were found with that query.**").
				Build())
			if err != nil {
				dbot.B.Logger.Error(err)
			}
		},
		func(err error) {
			// Something went wrong while loading the track
			// Log the error
			dbot.B.Logger.Error(err)
			// Send a message saying that something went wrong
			_, err = e.CreateFollowupMessage(discord.NewMessageCreateBuilder().
				SetContent("**❌ Something went wrong while loading the track.**").
				Build())
			if err != nil {
				dbot.B.Logger.Error(err)
			}
		},
	))

	// If the song is nil, return
	if song == nil {
		return nil
	}

	// Connect to the voice channel
	if err := dbot.B.Client.UpdateVoiceState(context.TODO(), *e.GuildID(), voiceState.ChannelID, false, false); err != nil {
		return err
	}

	// Send a message saying that we are playing the song
	_, err := e.CreateFollowupMessage(discord.NewMessageCreateBuilder().
		SetContentf("**🎵 Added [`%s`](<%s>) to the queue.**", song.Info.Title, *song.Info.URI).
		Build())
	if err != nil {
		return err
	}

	// Play the song
	return dbot.B.Lavalink.Client.Player(*e.GuildID()).Update(context.TODO(), lavalink.WithTrack(*song))
}
