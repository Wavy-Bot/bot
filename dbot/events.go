package dbot

import (
	"context"
	"github.com/disgoorg/disgo/events"
	"github.com/disgoorg/disgolink/v2/disgolink"
	"github.com/disgoorg/disgolink/v2/lavalink"
	"github.com/wavy-bot/bot/models"
	"time"
)

// OnReady is called when the client is done preparing the data received from Discord.
func (b *Bot) OnReady(event *events.Ready) {
	// Set uptime
	b.StartedAt = time.Now()

	// Print wavy information
	b.Logger.Infof("Bot is ready!\nLogged in as:\n%s\n%s\nRunning with %d shard(s)\n\n", event.User.ID, event.User.Username, len(b.Client.ShardManager().Shards()))
}

// TODO(Robert): Application command error handling.

func (b *Bot) OnVoiceStateUpdate(event *events.GuildVoiceStateUpdate) {
	if event.VoiceState.UserID != b.Client.ApplicationID() {
		return
	}
	b.Lavalink.Client.OnVoiceStateUpdate(context.TODO(), event.VoiceState.GuildID, event.VoiceState.ChannelID, event.VoiceState.SessionID)
	if event.VoiceState.ChannelID == nil {
		b.Lavalink.Queues.Delete(event.VoiceState.GuildID)
	}
}

func (b *Bot) OnVoiceServerUpdate(event *events.VoiceServerUpdate) {
	b.Lavalink.Client.OnVoiceServerUpdate(context.TODO(), event.GuildID, event.Token, *event.Endpoint)
}

func (b *Bot) OnPlayerPause(player disgolink.Player, event lavalink.PlayerPauseEvent) {
	b.Logger.Infof("onPlayerPause: %s", event.GuildID())
}

func (b *Bot) OnPlayerResume(player disgolink.Player, event lavalink.PlayerResumeEvent) {
	b.Logger.Infof("onPlayerResume: %s", event.GuildID())
}

func (b *Bot) OnTrackStart(player disgolink.Player, event lavalink.TrackStartEvent) {
	b.Logger.Infof("Track started: %s", event.EncodedTrack)
}

func (b *Bot) OnTrackEnd(player disgolink.Player, event lavalink.TrackEndEvent) {
	if !event.Reason.MayStartNext() {
		return
	}

	queue := b.Lavalink.Queues.Get(event.GuildID())
	var (
		nextTrack lavalink.Track
		ok        bool
	)
	switch queue.Type {
	case models.LavalinkQueueTypeNormal:
		nextTrack, ok = queue.Next()

	case models.LavalinkQueueTypeRepeatTrack:
		nextTrack = *player.Track()

	case models.LavalinkQueueTypeRepeatQueue:
		lastTrack, _ := b.Lavalink.Client.BestNode().DecodeTrack(context.TODO(), event.EncodedTrack)
		queue.Add(*lastTrack)
		nextTrack, ok = queue.Next()
	}

	if !ok {
		return
	}
	if err := player.Update(context.TODO(), lavalink.WithTrack(nextTrack)); err != nil {
		b.Logger.Error("Failed to play next track: ", err)
	}

	b.Logger.Infof("Track ended: %s", event.Reason)
}

func (b *Bot) OnTrackException(player disgolink.Player, event lavalink.TrackExceptionEvent) {
	b.Logger.Errorf("Track exception: %s", event.Exception)
}

func (b *Bot) OnTrackStuck(player disgolink.Player, event lavalink.TrackStuckEvent) {
	b.Logger.Errorf("Track stuck: %s", event.EncodedTrack)
}

func (b *Bot) OnWebSocketClosed(player disgolink.Player, event lavalink.WebSocketClosedEvent) {
	b.Logger.Errorf("Websocket closed: %d %s", event.Code, event.Reason)
}
