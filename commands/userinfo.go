package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"strconv"
	"strings"
)

// UserInfoHandler is the handler for the userinfo command.
func UserInfoHandler(e *handler.CommandEvent) error {
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
	case discord.ApplicationCommandTypeUser:
		data := e.UserCommandInteractionData()
		member = data.TargetMember()
	}

	// Create user role string
	roles := make([]string, len(member.RoleIDs))
	for i, role := range member.RoleIDs {
		roles[i] = fmt.Sprintf("<@&%d>", role)
	}

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitle("Info on "+member.User.Username).
			SetFields([]discord.EmbedField{
				{
					Name:  "Display name",
					Value: member.EffectiveName(),
				},
				{
					Name:  "ID",
					Value: member.User.ID.String(),
				},
				{
					Name:  "Created at",
					Value: fmt.Sprintf("<t:%d:F>", member.User.CreatedAt().Unix()),
				},
				{
					Name:  "Joined at",
					Value: fmt.Sprintf("<t:%d:F>", member.JoinedAt.Unix()),
				},
				{
					Name:  "Bot?",
					Value: strconv.FormatBool(member.User.Bot),
				},
				{
					Name:  "System?",
					Value: strconv.FormatBool(member.User.System),
				},
				{
					Name:  "Roles",
					Value: fmt.Sprintf("%s", strings.Join(roles, ", ")),
				},
			}...).
			SetThumbnail(member.User.EffectiveAvatarURL(discord.WithSize(4096))).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
