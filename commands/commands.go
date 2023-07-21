package commands

import (
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/json"
	"github.com/wavy-bot/bot/utils"
)

// CommandCategory is a category of commands.
type CommandCategory struct {
	// Name of the category.
	Name string
	// Commands in the category.
	Commands []discord.ApplicationCommandCreate
}

// CommandCategories combines all command categories.
var CommandCategories = []CommandCategory{
	GeneralCommands,
	FunCommands,
	InteractionCommands,
}

// Commands contains all commands.
var Commands []discord.ApplicationCommandCreate

// GeneralCommands contains all general commands.
var GeneralCommands = CommandCategory{
	Name: "General",
	Commands: []discord.ApplicationCommandCreate{
		discord.SlashCommandCreate{
			Name:        "ping",
			Description: "Pong! Nice shot!",
		},
		discord.SlashCommandCreate{
			Name:        "help",
			Description: "Here to help!",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionString{
					Name:        "category",
					Description: "The category to get help for.",
					Required:    false,
					Choices: []discord.ApplicationCommandOptionChoiceString{
						{
							Name:  "All",
							Value: "All",
						},
						{
							Name:  "General",
							Value: "General",
						},
						{
							Name:  "Fun",
							Value: "Fun",
						},
						{
							Name:  "Interaction",
							Value: "Interaction",
						},
						{
							Name:  "Music",
							Value: "Music",
						},
					},
				},
			},
		},
		discord.SlashCommandCreate{
			Name:        "avatar",
			Description: "Get the avatar of a user.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to get the avatar of. Defaults to yourself.",
					Required:    false,
				},
				discord.ApplicationCommandOptionBool{
					Name:        "server-specific",
					Description: "Whether to get the server-specific avatar of the user.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.UserCommandCreate{
			Name:         "Avatar",
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "botinfo",
			Description: "Get information about the bot.",
		},
		discord.SlashCommandCreate{
			Name:         "serverinfo",
			Description:  "Get information about the server.",
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "userinfo",
			Description: "Get information about a user.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to get the information of. Defaults to yourself.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.UserCommandCreate{
			Name:         "Info",
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "invite",
			Description: "Get the invite link for the bot.",
		},
	},
}

// FunCommands contains all fun commands.
var FunCommands = CommandCategory{
	Name: "Fun",
	Commands: []discord.ApplicationCommandCreate{
		discord.SlashCommandCreate{
			Name:        "howgay",
			Description: "Schlatt simulator.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to get the gayness of. Defaults to yourself.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "pp",
			Description: "Calculates the size of someone's fellow uhm... member.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to get the pp size of. Defaults to yourself.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "8ball",
			Description: "Ask the magic 8ball a question. Come, come now, don't be shy.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionString{
					Name:        "question",
					Description: "The question to ask the 8ball. 100% accurate, I swear.",
					Required:    true,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "ship",
			Description: "Who will be the next couple? 👀",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "first",
					Description: "The first user to ship.",
					Required:    true,
				},
				discord.ApplicationCommandOptionUser{
					Name:        "second",
					Description: "The second user to ship.",
					Required:    true,
				},
			},
			DMPermission: utils.NewFalse(),
		},
	},
}

// InteractionCommands contains all interaction commands.
var InteractionCommands = CommandCategory{
	Name: "Interactions",
	Commands: []discord.ApplicationCommandCreate{
		discord.SlashCommandCreate{
			Name:        "kiss",
			Description: "Uhm yeah, I don't know what to say here.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to kiss. Defaults to yourself.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.UserCommandCreate{
			Name:         "Kiss",
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "hug",
			Description: "Wuv you",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to hug. Defaults to yourself.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.UserCommandCreate{
			Name:         "Hug",
			DMPermission: utils.NewFalse(),
		},
		discord.SlashCommandCreate{
			Name:        "slap",
			Description: "Urusai or something, idk.",
			Options: []discord.ApplicationCommandOption{
				discord.ApplicationCommandOptionUser{
					Name:        "user",
					Description: "The user to slap. Defaults to yourself.",
					Required:    false,
				},
			},
			DMPermission: utils.NewFalse(),
		},
		discord.UserCommandCreate{
			Name:         "Slap",
			DMPermission: utils.NewFalse(),
		},
	},
}

func init() {
	// Combine all commands slices.
	for _, category := range CommandCategories {
		Commands = append(Commands, category.Commands...)
	}
}

// CreateEmbedFieldsForCategory creates embed fields for a command category.
func CreateEmbedFieldsForCategory(category CommandCategory) (fields []discord.EmbedField, err error) {
	// Loop through all commands in the category.
	for _, command := range category.Commands {
		// Only add slash commands.
		if command.Type() == discord.ApplicationCommandTypeSlash {
			// Marshal the command to JSON.
			var marshaledCommand []byte
			marshaledCommand, err = command.MarshalJSON()
			if err != nil {
				return
			}

			// Unmarshal the command to a slash command.
			var slashCommand discord.SlashCommand
			err = json.Unmarshal(marshaledCommand, &slashCommand)

			// Add the command to the fields.
			fields = append(fields, discord.EmbedField{
				Name:  slashCommand.Name(),
				Value: slashCommand.Description,
			})
		}
	}

	return
}
