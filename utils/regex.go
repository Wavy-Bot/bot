package utils

import "regexp"

var (
	URLPattern = regexp.MustCompile(`https?://(?:www\.)?.+`)
)
