package utils

// AccentColourBasedOnPct sets an accent colour based on the percentage provided.
func AccentColourBasedOnPct(percentage int) (accentColour int) {
	if percentage <= 100 {
		accentColour = 14753096
	}
	if percentage <= 75 {
		accentColour = 15357964
	}
	if percentage == 69 {
		accentColour = 13938487
	}
	if percentage <= 50 {
		accentColour = 16498468
	}
	if percentage <= 25 {
		accentColour = 2278750
	}

	return
}
