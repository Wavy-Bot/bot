package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
	"math/rand"
)

// ShipHandler is the handler for the ship command.
// Now kith.
func ShipHandler(e *handler.CommandEvent) error {
	// Get the command interaction data
	var data = e.SlashCommandInteractionData()

	// Get the users from the slash command interaction data
	first := data.Member("first")
	second := data.Member("second")

	// Get a random size
	percentage := rand.Intn(100)
	bar := utils.ProgressBar(percentage)

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("🚢 ship machine 🚢").
			SetDescriptionf("%s\n%s — %s", utils.StringBasedOnPercentage(percentage), first, second).
			AddField(fmt.Sprintf("%d%%", percentage), bar, true).
			SetColor(utils.AccentColourBasedOnPct(percentage)).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
