package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
)

// HowGayHandler is the handler for the howgay command.
// In case you still haven't figured it out, this is a very serious command.
// Please don't take it too seriously, love you all <3
func HowGayHandler(e *handler.CommandEvent) error {
	// Get the command interaction data
	var data = e.SlashCommandInteractionData()

	// Get the user from the slash command interaction data
	// If the user is not provided, default to the user who ran the command
	member, ok := data.OptMember("user")
	if !ok {
		member = *e.Member()
	}

	// Get a random percentage
	percentage, err := utils.RandomNumber(100)
	if err != nil {
		return err
	}
	bar := utils.ProgressBar(percentage)

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("🏳‍🌈 gay detection machine 🏳‍🌈").
			AddField(fmt.Sprintf("%s is %d%% gay", member.EffectiveName(), percentage), bar, true).
			SetColor(utils.AccentColourBasedOnPct(percentage)).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
