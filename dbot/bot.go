package dbot

import (
	"context"
	"fmt"
	"github.com/disgoorg/disgo"
	"github.com/disgoorg/disgo/bot"
	"github.com/disgoorg/disgo/cache"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/gateway"
	"github.com/disgoorg/disgo/sharding"
	"github.com/disgoorg/disgolink/v2/disgolink"
	"github.com/disgoorg/json"
	"github.com/disgoorg/paginator"
	log "github.com/sirupsen/logrus"
	"github.com/wavy-bot/bot/models"
	"io"
	"os"
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
	// Lavalink is the Lavalink struct for the bot.
	Lavalink models.Lavalink
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
func (b *Bot) GetStats() (version string, goVersion string, disGoVersion string, disGoLinkVersion string, uptime time.Duration, shards int, guilds int, channels int) {
	version = b.Version
	goVersion = b.GoVersion
	disGoVersion = disgo.Version
	disGoLinkVersion = disgolink.Version
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

// addLavalinkNode adds a Lavalink node to the Lavalink client.
func (b *Bot) addLavalinkNode(ctx context.Context, nodeConfig disgolink.NodeConfig) (node disgolink.Node, err error) {
	// Add the node to the Lavalink client
	node, err = b.Lavalink.Client.AddNode(ctx, nodeConfig)
	if err != nil {
		b.Logger.Fatal("[DisGoLink] Error while adding node: ", err)
		return
	}

	// Get the node's version
	version, err := node.Version(ctx)
	if err != nil {
		b.Logger.Fatal("[DisGoLink] Error while getting node version: ", err)
		return
	}
	b.Logger.Infof("[DisGoLink] Node: <%s> is ready! Running version <%s>.", node.Config().Name, version)
	return
}

// AddLavalinkNodes adds all the Lavalink nodes from the lavalink.json file to the Lavalink client.
func (b *Bot) AddLavalinkNodes(ctx context.Context) (nodes []disgolink.Node, err error) {
	// Create a slice of node configurations
	var configs models.LavalinkNodes

	// Load the Lavalink configuration from the JSON file
	b.Logger.Info("[DisGoLink] Loading nodes from config...")
	jsonFile, err := os.Open("lavalink.json")
	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()

	// Read and unmarshal the JSON file
	byteValue, err := io.ReadAll(jsonFile)
	if err != nil {
		return nil, err
	}
	err = json.Unmarshal(byteValue, &configs)
	if err != nil {
		return nil, err
	}

	// Add the nodes to the Lavalink client
	b.Logger.Info("[DisGoLink] Adding nodes...")
	for _, nodeConfig := range configs.Nodes {
		node, err := b.addLavalinkNode(ctx, nodeConfig)
		if err == nil {
			// Add the node to the slice of nodes
			nodes = append(nodes, node)
		}
	}
	return
}
