package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
	"math/rand"
)

// PPHandler is the handler for the pp command.
// It handles a lot of pp. 'ery noice.
func PPHandler(e *handler.CommandEvent) error {
	// Get the command interaction data
	var data = e.SlashCommandInteractionData()

	// Get the user from the slash command interaction data
	// If the user is not provided, default to the user who ran the command
	member, ok := data.OptMember("user")
	if !ok {
		member = *e.Member()
	}

	// Get a random size
	size := rand.Intn(20)
	pp := utils.PP(size)

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("pp size calculator™").
			AddField(fmt.Sprintf("%s's pp size", member.EffectiveName()), pp, true).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
