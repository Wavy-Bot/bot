package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
)

// AvatarHandler is the handler for the avatar command.
func AvatarHandler(e *handler.CommandEvent) error {
	// Create a map for all avatars
	var avatars map[string]string
	// Create a new resolved member
	var member discord.ResolvedMember

	// Get the user from the command interaction data
	// If the user is not provided, default to the user who ran the command
	switch e.ApplicationCommandInteraction.Data.Type() {
	case discord.ApplicationCommandTypeSlash:
		var ok bool

		data := e.SlashCommandInteractionData()
		member, ok = data.OptMember("user")
		if !ok {
			member = *e.Member()
		}

		// Get the server-specific option
		serverSpecific := e.SlashCommandInteractionData().Bool("server-specific")

		// Get all avatars
		if serverSpecific {
			avatars = utils.GetMemberAvatars(member, discord.WithSize(4096))
		} else {
			avatars = utils.GetUserAvatars(member.User, discord.WithSize(4096))
		}
	case discord.ApplicationCommandTypeUser:
		data := e.UserCommandInteractionData()
		member = data.TargetMember()
		avatars = utils.GetMemberAvatars(member, discord.WithSize(4096))
	}

	// Create a string with all avatar formats. If GIF is not available, don't include it.
	avatarString := fmt.Sprintf("[WebP](%s) | [PNG](%s) | [JPG](%s)", avatars["webp"], avatars["png"], avatars["jpg"])
	if avatars["gif"] != "" {
		avatarString += fmt.Sprintf(" | [GIF](%s)", avatars["gif"])
	}

	// Send the avatar embed
	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitlef("Avatar for %s", member.EffectiveName()).
			SetDescription(avatarString).
			SetImage(avatars["webp"]).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
