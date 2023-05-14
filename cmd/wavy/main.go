package main

import (
	"context"
	"github.com/disgoorg/disgo/bot"
	"github.com/disgoorg/disgolink/v2/disgolink"
	"github.com/disgoorg/paginator"
	"github.com/disgoorg/snowflake/v2"
	"github.com/getsentry/sentry-go"
	"github.com/makasim/sentryhook"
	log "github.com/sirupsen/logrus"
	"github.com/wavy-bot/bot/commands"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/models"
	"os"
	"os/signal"
	"runtime"
	"strings"
	"syscall"
	"time"
)

// Version of the bot.
const Version = "2.0.0-alpha.1"

func init() {
	// Set the logger
	dbot.B.Logger = log.StandardLogger()

	// Load the config
	dbot.LoadConfig()

	// Set up logging
	dbot.B.Logger.SetFormatter(&log.TextFormatter{
		EnvironmentOverrideColors: true,
		DisableTimestamp:          false,
		FullTimestamp:             true,
		TimestampFormat:           time.StampMilli,
		PadLevelText:              true,
	})
	if dbot.Config.Debug {
		dbot.B.Logger.SetLevel(log.DebugLevel)
	} else {
		dbot.B.Logger.SetLevel(log.InfoLevel)
	}

	if dbot.Config.SentryURL != "" {
		// Initialize Sentry
		if err := sentry.Init(sentry.ClientOptions{
			Dsn: dbot.Config.SentryURL,
			// Enable printing of SDK debug messages if debug is enabled.
			Debug:            dbot.Config.Debug,
			AttachStacktrace: true,
			SampleRate:       1,
			ServerName:       os.Getenv("HOSTNAME"),
			// @TODO(Robert): Set this to the version of the bot.
			//Release:          wavy.Version,
		}); err != nil {
			dbot.B.Logger.Fatalf("sentry.Init: %s", err)
		}

		// Set up Sentry hook
		dbot.B.Logger.AddHook(sentryhook.New([]log.Level{log.PanicLevel, log.FatalLevel, log.ErrorLevel}))
	}

	// Set the application and Go version
	dbot.B.Version = Version
	dbot.B.GoVersion = strings.Replace(runtime.Version(), "go", "", 1)
}

func main() {
	var err error

	// wowie cool ascii art
	dbot.B.Logger.Info("\n _       __                        \n| |     / /  ____ _ _   __   __  __\n| | /| / /  / __ `/| | / /  / / / /\n| |/ |/ /  / /_/ / | |/ /  / /_/ / \n|__/|__/   \\__,_/  |___/   \\__, /  \n                          /____/   ")

	// Create command handler
	h := commands.CreateHandler()
	// Create paginator
	p := paginator.New()
	dbot.B.Paginator = p

	// Set up the bot
	if err := dbot.B.Setup(h, dbot.B.Paginator, bot.NewListenerFunc(dbot.B.OnReady), bot.NewListenerFunc(dbot.B.OnVoiceStateUpdate), bot.NewListenerFunc(dbot.B.OnVoiceServerUpdate)); err != nil {
		dbot.B.Logger.Fatal("error while setting up wavy: ", err)
	}

	// Create Lavalink client
	dbot.B.Lavalink.Client = disgolink.New(dbot.B.Client.ID(),
		disgolink.WithListenerFunc(dbot.B.OnPlayerPause),
		disgolink.WithListenerFunc(dbot.B.OnPlayerResume),
		disgolink.WithListenerFunc(dbot.B.OnTrackStart),
		disgolink.WithListenerFunc(dbot.B.OnTrackEnd),
		disgolink.WithListenerFunc(dbot.B.OnTrackException),
		disgolink.WithListenerFunc(dbot.B.OnTrackStuck),
		disgolink.WithListenerFunc(dbot.B.OnWebSocketClosed),
	)

	// Create Lavalink queues map
	dbot.B.Lavalink.Queues = &models.LavalinkQueueManager{
		Queues: make(map[snowflake.ID]*models.LavalinkQueue),
	}

	// Sync commands
	dbot.B.Logger.Info("Syncing commands...")
	if dbot.Config.Debug {
		_, err = dbot.B.Client.Rest().SetGuildCommands(dbot.B.Client.ApplicationID(), dbot.Config.AdminGuild, commands.Commands)
	} else {
		_, err = dbot.B.Client.Rest().SetGlobalCommands(dbot.B.Client.ApplicationID(), commands.Commands)
	}
	if err != nil {
		dbot.B.Logger.Fatal("error while syncing commands: ", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Open the gateway
	if err := dbot.B.Client.OpenShardManager(ctx); err != nil {
		dbot.B.Logger.Fatal("error while connecting to gateway: ", err)
	}
	// Defer closing the client
	defer dbot.B.Client.Close(context.TODO())

	// Connect to Lavalink
	_, err = dbot.B.AddLavalinkNodes(ctx)
	if err != nil {
		dbot.B.Logger.Fatal("[DisGoLink] Error while adding Lavalink nodes: ", err)
	}

	// Wait for CTRL-C to exit
	dbot.B.Logger.Info("Wavy is now running. Press CTRL-C to exit.")
	s := make(chan os.Signal, 1)
	signal.Notify(s, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-s
}
