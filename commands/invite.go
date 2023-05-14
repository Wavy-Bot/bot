package commands

import (
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
)

// InviteHandler is the handler for the invite command.
func InviteHandler(e *handler.CommandEvent) error {
	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("Invite Wavy").
			SetDescriptionf("You can invite Wavy to your server [here](%s).\nNeed help? Join Wavy's support server [here](%s).", dbot.B.GetInviteLink(), dbot.Config.SupportServerURL).
			SetThumbnail(dbot.B.GetAvatar(discord.WithSize(4096))).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
