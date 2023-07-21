package commands

import (
	"github.com/disgoorg/disgo/discord"
	"github.com/disgoorg/disgo/handler"
	"github.com/disgoorg/paginator"
	"github.com/wavy-bot/bot/dbot"
	"math"
)

// HelpHandler is the handler for the help command.
func HelpHandler(e *handler.CommandEvent) error {
	// Create fields for the embed
	var fields []discord.EmbedField
	// Create a variable for any errors
	var err error

	// Get the category from the interaction,
	// If the category is not provided, default to all commands
	data := e.SlashCommandInteractionData()
	category, ok := data.OptString("category")
	if !ok {
		category = "All"
	}

	// Create the fields based on the category
	switch category {
	case "All":
		// Create a variable for all commands
		var allCommands = CommandCategory{
			Name:     "All",
			Commands: []discord.ApplicationCommandCreate{},
		}
		// Add all commands to the allCommands variable
		for _, iCategory := range CommandCategories {
			allCommands.Commands = append(allCommands.Commands, iCategory.Commands...)
		}
		// Create the fields for all categories
		fields, err = CreateEmbedFieldsForCategory(allCommands)
		if err != nil {
			return err
		}
	case "General":
		// Create the fields for the General category
		fields, err = CreateEmbedFieldsForCategory(GeneralCommands)
		if err != nil {
			return err
		}
	case "Fun":
		// Create the fields for the Fun category
		fields, err = CreateEmbedFieldsForCategory(FunCommands)
		if err != nil {
			return err
		}
	case "Interaction":
		// Create the fields for the Interaction category
		fields, err = CreateEmbedFieldsForCategory(InteractionCommands)
		if err != nil {
			return err
		}
	}

	// Create a new paginator.Pages
	return dbot.B.Paginator.Create(e.Respond, paginator.Pages{
		// A unique ID for this paginator
		ID: e.ID().String(),
		// This is the function that will be called to create the embed for each page when the page is displayed
		PageFunc: func(page int, embed *discord.EmbedBuilder) {
			embed.SetTitlef("%s command help", category)
			// Loop 5 times
			for i := 0; i < 5; i++ {
				// If the page*5+i is greater than the length of the fields, break the loop
				if page*5+i >= len(fields) {
					break
				}
				// Add the field to the embed
				embed.AddField(fields[page*5+i].Name, fields[page*5+i].Value, false)
			}
			embed.SetColor(dbot.Config.EmbColour)
			embed.SetFooter("Wavy • https://wavybot.com", dbot.B.GetAvatar())
		},
		// The total number of pages
		Pages: int(math.Ceil(float64(len(fields)) / 5)),
		// Optional: If the paginator should only be accessible by the user who created it
		Creator: e.User().ID,
		// Optional: If the paginator should be deleted after x time after the last interaction
		ExpireMode: paginator.ExpireModeAfterLastUsage,
	}, false)
}
