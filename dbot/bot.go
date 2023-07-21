package dbot

import (
	"fmt"
	"github.com/disgoorg/disgo"
	"github.com/disgoorg/disgo/bot"
	"github.com/disgoorg/disgo/cache"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/gateway"
	"github.com/disgoorg/disgo/sharding"
	"github.com/disgoorg/paginator"
	log "github.com/sirupsen/logrus"
	"time"
)

// B is the bot instance.
// It is called B to avoid interference with DisGo's wavy package.
var B = &Bot{}

// Bot contains all the variables that are used throughout the bot.
type Bot struct {
	// StartedAt is when the bot started.
	StartedAt time.Time
	// GoVersion is the version of Go the bot uses.
	GoVersion string
	// Client is the Discord client for the bot.
	Client bot.Client
	// Paginator is the paginator the bot uses.
	Paginator *paginator.Manager
	// Logger is the logger the bot uses.
	Logger *log.Logger
	// Version is the version of the bot.
	Version string
}

// Setup sets up the bot.
func (b *Bot) Setup(listeners ...bot.EventListener) (err error) {
	// Create a new DisGo client
	b.Client, err = disgo.New(Config.Token,
		bot.WithShardManagerConfigOpts(
			sharding.WithLogger(b.Logger),
			sharding.WithAutoScaling(true),
			sharding.WithGatewayConfigOpts(
				gateway.WithIntents(
					gateway.IntentsNonPrivileged,
					gateway.IntentGuildMembers,
				),
				gateway.WithCompress(true),
				gateway.WithPresenceOpts(gateway.WithWatchingActivity("/help | https://wavybot.com")),
			),
		),
		bot.WithEventListeners(listeners...),
		bot.WithCacheConfigOpts(cache.WithCaches(cache.FlagGuilds, cache.FlagMembers, cache.FlagVoiceStates, cache.FlagChannels, cache.FlagRoles, cache.FlagEmojis, cache.FlagStickers)),
	)
	if err != nil {
		b.Logger.Fatal("error while creating disgo client: ", err)
	}

	return
}

// GetAvatar returns the bot's avatar.
func (b *Bot) GetAvatar(opts ...discord.CDNOpt) string {
	// Get the bot's user from the cache
	user, _ := b.Client.Caches().SelfUser()

	return user.EffectiveAvatarURL(opts...)
}

// GetStats returns the bot's stats.
// TODO(Robert): Voice connections?
func (b *Bot) GetStats() (version string, goVersion string, disGoVersion string, uptime time.Duration, shards int, guilds int, channels int) {
	version = b.Version
	goVersion = b.GoVersion
	disGoVersion = disgo.Version
	uptime = time.Since(b.StartedAt).Round(time.Second)
	shards = len(b.Client.ShardManager().Shards())
	guilds = b.Client.Caches().GuildsLen()
	channels = b.Client.Caches().ChannelsLen()

	return
}

// GetInviteLink returns the bot's invite link.
func (b *Bot) GetInviteLink() string {
	return fmt.Sprintf("https://discord.com/oauth2/authorize?client_id=%d&scope=bot%%20applications.commands&permissions=%d", b.Client.ID(), Config.InvitePermissions)
}
