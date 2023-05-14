package utils

import (
	"github.com/disgoorg/disgo/discord"
	"strings"
)

// GetMemberAvatars returns all avatar URLs of a member.
func GetMemberAvatars(m discord.ResolvedMember, size discord.CDNOpt) (avatars map[string]string) {
	// Create a map of the avatar URLs.
	avatars = make(map[string]string)

	// Add the avatar URLs to the map.
	if m.Avatar != nil {
		avatars["webp"] = m.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatWebP), size)
		avatars["png"] = m.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatPNG), size)
		avatars["jpg"] = m.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatJPEG), size)
		if strings.HasPrefix(*m.Avatar, "a_") {
			avatars["gif"] = m.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatGIF), size)
		}
	} else {
		avatars = GetUserAvatars(m.User, size)
	}

	// Return the map of avatar URLs.
	return
}
