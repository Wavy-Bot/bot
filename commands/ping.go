package commands

import (
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
)

// PingHandler is the handler for the ping command.
func PingHandler(e *handler.CommandEvent) error {
	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("Pong! :ping_pong:").
			SetDescriptionf("Took %dms", e.Client().Gateway().Latency().Milliseconds()).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
