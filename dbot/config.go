package dbot

import (
	"github.com/caarlos0/env/v8"
	"github.com/disgoorg/snowflake/v2"
	"github.com/hashicorp/go-envparse"
	"os"
)

// Config is the global configuration struct.
var Config *Configuration

// Configuration contains the configuration values for the bot.
type Configuration struct {
	// Debug is the debug mode of the bot.
	Debug bool `env:"DEBUG" envDefault:"false"`

	// Token is the token of the bot, this is used to authenticate with the Discord API.
	Token string `env:"TOKEN"`
	// AdminGuild is the guild ID of the admin guild, this is used to test slash commands without pushing them to all guilds.
	AdminGuild snowflake.ID `env:"ADMIN_GUILD" envDefault:""`
	// InvitePermissions is the permissions integer that is used when generating the invite link.
	// @TODO(Robert): Calculate permissions, admin perms are definitely not needed and are a security risk.
	InvitePermissions int `env:"INVITE_PERMISSIONS" envDefault:"8"`
	// SupportServerURL is the URL of the support server.
	SupportServerURL string `env:"SUPPORT_SERVER_URL" envDefault:"https://discord.wavybot.com"`

	// EmbColour is the colour of the embeds. This is a hex value, converted to an int with base 16.
	EmbColour int `env:"EMB_COLOUR" envDefault:"790311"`
	// EmbColourError is the colour of the error embeds. This is a hex value, converted to an int with base 16.
	EmbErrColour int `env:"EMB_ERR_COLOUR" envDefault:"16399360"`

	// SentryURL is the URL of the Sentry instance.
	SentryURL string `env:"SENTRY_URL"`
}

// LoadConfig loads the configuration from the environment variables.
func LoadConfig() {
	c := &Configuration{}

	// Load environment variables from .env file
	// and parse them into a map
	var envs map[string]string
	file, _ := os.Open(".env")
	envs, _ = envparse.Parse(file)

	// Parse the environment variables into the configuration struct
	if err := env.ParseWithOptions(c, env.Options{Environment: envs}); err != nil {
		B.Logger.Fatalf("Unable to parse config into struct: %v", err)
	}

	Config = c
}
