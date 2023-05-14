package utils

import (
	"github.com/disgoorg/disgo/discord"
	"strings"
)

// GetUserAvatars returns all avatar URLs of a user.
func GetUserAvatars(u discord.User, size discord.CDNOpt) (avatars map[string]string) {
	// Create a map of the avatar URLs.
	avatars = make(map[string]string)

	// Add the avatar URLs to the map.
	avatars["webp"] = u.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatWebP), size)
	avatars["png"] = u.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatPNG), size)
	avatars["jpg"] = u.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatJPEG), size)
	if strings.HasPrefix(*u.Avatar, "a_") {
		avatars["gif"] = u.EffectiveAvatarURL(discord.WithFormat(discord.ImageFormatGIF), size)
	}

	// Return the map of avatar URLs.
	return
}
