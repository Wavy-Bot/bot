package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
)

// SlapHandler is the handler for the slap command.
func SlapHandler(e *handler.CommandEvent) error {
	// If the user kisses themselves, send a different message
	var message string

	// Create a new resolved member
	var member discord.ResolvedMember

	// Get the user from the command interaction data
	// If the user is not provided, default to the user who ran the command
	switch e.ApplicationCommandInteraction.Data.Type() {
	case discord.ApplicationCommandTypeSlash:
		var ok bool

		data := e.SlashCommandInteractionData()
		member, ok = data.OptMember("user")
		switch ok {
		case true:
			message = fmt.Sprintf("%s slaps %s", e.Member().EffectiveName(), member.EffectiveName())
		case false:
			member = *e.Member()
			message = fmt.Sprintf("%s slaps themselves", member.EffectiveName())
		}
	case discord.ApplicationCommandTypeUser:
		data := e.UserCommandInteractionData()
		executor := e.Member()
		member = data.TargetMember()
		switch executor.User.ID == member.User.ID {
		case true:
			message = fmt.Sprintf("%s slaps themselves", executor.EffectiveName())
		case false:
			message = fmt.Sprintf("%s slaps %s", executor.EffectiveName(), member.EffectiveName())
		}
	}

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle(message).
			SetImage(utils.SlapGIF()).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
