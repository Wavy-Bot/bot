package dbot

import (
	"github.com/disgoorg/disgo/events"
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
