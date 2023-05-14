package utils

import (
	"math/rand"
	"strings"
)

var EightBallMessages = []string{
	"It is certain",
	"It is decidedly so.",
	"Without a doubt",
	"Yes - definitely.",
	"You may rely on it.",
	"As I see it, yes.",
	"Most likely.",
	"Outlook good.",
	"Yes.",
	"Signs point to yes.",
	"Reply hazy, try again.",
	"Ask again later.",
	"Better not tell you now.",
	"Cannot predict now.",
	"Concentrate and ask again.",
	"Don't count on it.",
	"My reply is no.",
	"My sources say no",
	"Outlook not so good.",
	"Very doubtful.",
}

// ProgressBar returns a progress bar with a length of 10 characters made out of the white and black large square emoji.
func ProgressBar(percentage int) string {
	// Create progress bar
	return strings.Repeat("⬜", percentage/10) + strings.Repeat("⬛", 10-(percentage/10))
}

// PP returns a... uh... pp.
func PP(size int) string {
	return "8" + strings.Repeat("=", size) + "D"
}

// EightBallMessage returns a random 8ball message.
func EightBallMessage() string {
	return EightBallMessages[rand.Intn(len(EightBallMessages))]
}

// StringBasedOnPercentage returns a string based on the percentage provided.
func StringBasedOnPercentage(percentage int) (message string) {
	if percentage <= 100 {
		message = "\\*jaw drops to floor, eyes pop out of sockets\\*"
	}
	if percentage <= 75 {
		message = "damn"
	}
	if percentage == 69 {
		message = "nice."
	}
	if percentage <= 50 {
		message = "not bad, not great"
	}
	if percentage <= 25 {
		message = "uh oh stinky"
	}

	return
}
