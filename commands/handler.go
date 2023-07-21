package commands

import (
	"github.com/disgoorg/disgo/handler"
)

// CreateHandler creates a new command handler for the bot.
func CreateHandler() *handler.Mux {
	// Create a new command handler
	h := handler.New()

	// Slash commands //

	// General commands
	// Register the ping command
	h.Command("/ping", PingHandler)
	// Register the help command
	h.Command("/help", HelpHandler)
	// Register the avatar command
	h.Command("/avatar", AvatarHandler)
	// Register the botinfo command
	h.Command("/botinfo", BotInfoHandler)
	// Register the serverinfo command
	h.Command("/serverinfo", ServerInfoHandler)
	// Register the userinfo command
	h.Command("/userinfo", UserInfoHandler)
	// Register the invite command
	h.Command("/invite", InviteHandler)

	// Fun commands
	// Register the howgay command
	h.Command("/howgay", HowGayHandler)
	// Register the pp command
	h.Command("/pp", PPHandler)
	// Register the 8ball command
	h.Command("/8ball", EightBallHandler)
	// Register the ship command
	h.Command("/ship", ShipHandler)

	// Interaction commands
	// Register the kiss command
	h.Command("/kiss", KissHandler)
	// Register the hug command
	h.Command("/hug", HugHandler)
	// Register the slap command
	h.Command("/slap", SlapHandler)

	// User commands //

	// General commands
	// Register the avatar user command
	h.Command("/Avatar", AvatarHandler)
	// Register the info user command
	h.Command("/Info", UserInfoHandler)

	// Interaction commands
	// Register the kiss user command
	h.Command("/Kiss", KissHandler)
	// Register the hug user command
	h.Command("/Hug", HugHandler)
	// Register the slap user command
	h.Command("/Slap", SlapHandler)

	return h
}
