package commands

import (
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
)

// BotInfoHandler is the handler for the botinfo command.
func BotInfoHandler(e *handler.CommandEvent) error {
	// Get wavy stats
	version, goVersion, disGoVersion, disGoLinkVersion, uptime, shards, guilds, channels := dbot.B.GetStats()

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("Bot info").
			// TODO(Robert): Write a description.
			SetDescriptionf("I still have to write some description here so for now you get this useless placeholder text I guess\n\n**Stats**\nBot version: %s\nGo version: %s\nDisGo version: %s\n DisGoLink version: %s\nUptime: %s\nShards: %d\nGuilds: %d\nChannels: %d", version, goVersion, disGoVersion, disGoLinkVersion, uptime.String(), shards, guilds, channels).
			SetThumbnail(dbot.B.GetAvatar(discord.WithSize(4096))).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		AddActionRow(discord.ButtonComponent{
			Style: discord.ButtonStyleLink,
			Emoji: &discord.ComponentEmoji{
				Name: "😋",
			},
			Label: "Add me to your server!",
			URL:   dbot.B.GetInviteLink(),
		},
			discord.ButtonComponent{
				Style: discord.ButtonStyleLink,
				Emoji: &discord.ComponentEmoji{
					Name: "💡",
				},
				Label: "Support server",
				URL:   dbot.Config.SupportServerURL,
			}).
		Build())
}
