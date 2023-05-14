package commands

import (
	"fmt"
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/wavy-bot/bot/dbot"
	"github.com/wavy-bot/bot/utils"
	"strconv"
)

// ServerInfoHandler is the handler for the serverinfo command.
func ServerInfoHandler(e *handler.CommandEvent) error {
	// Get caches
	caches := dbot.B.Client.Caches()

	// Get guild
	guild, _ := e.Guild()

	// Convert verification level to string
	var verificationLevel string
	switch guild.VerificationLevel {
	case discord.VerificationLevelNone:
		verificationLevel = "None ( ⚆ _ ⚆ )"
	case discord.VerificationLevelLow:
		verificationLevel = "Low ┬─┬ノ( º _ ºノ)"
	case discord.VerificationLevelMedium:
		verificationLevel = "Medium (is premium 😉)"
	case discord.VerificationLevelHigh:
		verificationLevel = "High (╯°□°)╯︵ ┻━┻"
	case discord.VerificationLevelVeryHigh:
		verificationLevel = "Very High ┻━┻ ミヽ(ಠ益ಠ)ノ彡 ┻━┻"
	}

	// Get channels
	var channels int
	caches.ChannelsForEach(func(channel discord.GuildChannel) {
		if channel.GuildID() == guild.ID {
			channels++
		}
	})

	return e.CreateMessage(discord.NewMessageCreateBuilder().
		SetEmbeds(discord.NewEmbedBuilder().
			SetTitlef("Info on %s", guild.Name).
			SetFields([]discord.EmbedField{
				{
					Name:  "ID",
					Value: guild.ID.String(),
				},
				{
					Name:  "Created",
					Value: fmt.Sprintf("<t:%d:F>", guild.CreatedAt().Unix()),
				},
				{
					Name:  "Owner",
					Value: fmt.Sprintf("<@%s>", guild.OwnerID.String()),
				},
				{
					Name:  "Members",
					Value: strconv.Itoa(guild.MemberCount),
				},
				{
					Name:  "Channels",
					Value: strconv.Itoa(channels),
				},
				{
					Name:  "Roles",
					Value: strconv.Itoa(caches.RolesLen(guild.ID)),
				},
				{
					Name:  "Boosts",
					Value: strconv.Itoa(guild.PremiumSubscriptionCount),
				},
				{
					Name:  "Verification level",
					Value: verificationLevel,
				},
				{
					Name:  "Emoji",
					Value: strconv.Itoa(caches.EmojisLen(guild.ID)),
				},
				{
					Name:  "Stickers",
					Value: strconv.Itoa(caches.StickersLen(guild.ID)),
				},
			}...).
			SetThumbnail(utils.GetGuildIcon(guild)).
			SetColor(dbot.Config.EmbColour).
			SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar()).
			Build()).
		Build())
}
