package utils

import "github.com/disgoorg/disgo/discord"

// GetGuildIcon returns the icon of a guild.
func GetGuildIcon(g discord.Guild, opts ...discord.CDNOpt) string {
	if g.IconURL() == nil {
		// Return the default avatar.
		return discord.DefaultUserAvatar.URL(discord.ImageFormatWebP, discord.QueryValues{
			"size": "4096",
		})
	} else {
		// Return the avatar of the user.
		return *g.IconURL(opts...)
	}
}
