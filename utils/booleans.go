// Package utils provides utility functions for the bot.
// TODO(Robert): Split this package into multiple packages.
// See https://google.github.io/styleguide/go/best-practices.html#util-packages
package utils

// NewFalse is a helper function to create a pointer to a false boolean.
func NewFalse() *bool {
	b := false
	return &b
}
