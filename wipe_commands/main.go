/* MIT License
 *
 * Copyright (c) 2017 Roland Singer [roland.singer@desertbit.com]
 * Copyright (c) 2023 Robert Stokreef [hello@robert-s.dev]
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package main

import (
	"bufio"
	"context"
	"fmt"
	"github.com/disgoorg/disgo"
	"github.com/disgoorg/disgo/discord"
	log "github.com/sirupsen/logrus"
	"github.com/wavy-bot/bot/dbot"
	"os"
	"strings"
)

var logger *log.Logger

func init() {
	// Load config
	dbot.LoadConfig()

	// Set the logger
	logger = log.StandardLogger()
}

// askForConfirmation asks the user for confirmation. A user must type in "yes" or "no" and
// then press enter. It has fuzzy matching, so "y", "Y", "yes", "YES", and "Yes" all count as
// confirmations. If the input is not recognized, it will ask again. The function does not return
// until it gets a valid response from the user.
func askForConfirmation(s string) bool {
	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Printf("%s [y/n]: ", s)

		response, err := reader.ReadString('\n')
		if err != nil {
			logger.Fatal(err)
		}

		response = strings.ToLower(strings.TrimSpace(response))

		if response == "y" || response == "yes" {
			return true
		} else if response == "n" || response == "no" {
			return false
		}
	}
}

func main() {
	// Create a new DisGo client
	client, err := disgo.New(dbot.Config.Token)
	if err != nil {
		logger.Fatal("error while creating disgo client: ", err)
	}

	// Wipe all global commands if the user wants to
	c := askForConfirmation("Do you really want to wipe all global commands?")
	if c {
		_, err = client.Rest().SetGlobalCommands(client.ApplicationID(), []discord.ApplicationCommandCreate{})
		if err != nil {
			logger.Fatal("error while wiping global commands: ", err)
		}
		logger.Println("Successfully wiped global commands.")
	}

	// Wipe all admin guild commands if the user wants to
	gc := askForConfirmation("Do you also want to wipe all admin guild commands?")
	if gc {
		_, err = client.Rest().SetGuildCommands(client.ApplicationID(), dbot.Config.AdminGuild, []discord.ApplicationCommandCreate{})
		if err != nil {
			logger.Fatal("error while wiping admin guild commands: ", err)
		}
		logger.Println("Successfully wiped admin guild commands.")
	}

	// Defer closing the client
	defer client.Close(context.TODO())

	// Quit the program
	return
}
