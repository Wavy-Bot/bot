package commands

import (
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
)

// EightBallHandler is the handler for the 8ball command.
// It is certain. Or is it?
func EightBallHandler(e *handler.CommandEvent) error {
	// Get the command interaction data
	var data = e.SlashCommandInteractionData()

	// Get the question from the slash command interaction data
	question := data.String("question")

	// Get message
	message := utils.EightBallMessage()

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("Q: "+question).
			SetDescription("A: "+message).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
