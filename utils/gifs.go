package utils

import (
	"crypto/rand"
	"math/big"
)

var KissGIFs = []string{
	"https://media1.tenor.com/images/4b5d5afd747fe053ed79317628aac106/tenor.gif",
	"https://media1.tenor.com/images/d307db89f181813e0d05937b5feb4254/tenor.gif",
	"https://media1.tenor.com/images/2f23c53755a5c3494a7f54bbcf04d1cc/tenor.gif",
	"https://media1.tenor.com/images/7fd98defeb5fd901afe6ace0dffce96e/tenor.gif",
	"https://media1.tenor.com/images/ea9a07318bd8400fbfbd658e9f5ecd5d/tenor.gif",
	"https://media1.tenor.com/images/a390476cc2773898ae75090429fb1d3b/tenor.gif",
	"https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif",
	"https://media1.tenor.com/images/e76e640bbbd4161345f551bb42e6eb13/tenor.gif",
}

var HugGIFs = []string{
	"https://c.tenor.com/8Jk1ueYnyYUAAAAC/hug.gif",
	"https://c.tenor.com/3mr1aHrTXSsAAAAC/hug-anime.gif",
	"https://c.tenor.com/gKlGEBBkliwAAAAC/anime-yuru-yuri.gif",
	"https://c.tenor.com/QTbBCR3j-vYAAAAd/hugs-best-friends.gif",
	"https://c.tenor.com/wUQH5CF2DJ4AAAAC/horimiya-hug-anime.gif",
	"https://c.tenor.com/0T3_4tv71-kAAAAC/anime-happy.gif",
	"https://c.tenor.com/35RotStN1BkAAAAC/anime-hug-anime.gif",
	"https://c.tenor.com/1T1B8HcWalQAAAAC/anime-hug.gif",
	"https://c.tenor.com/9e1aE_xBLCsAAAAC/anime-hug.gif",
	"https://c.tenor.com/lzKyZchfMzAAAAAC/anime-hug.gif",
	"https://c.tenor.com/Ct4bdr2ZGeAAAAAC/teria-wang-kishuku-gakkou-no-juliet.gif",
	"https://c.tenor.com/O3qIam1dAQQAAAAC/hug-cuddle.gif",
	"https://c.tenor.com/QwHSis0hNEQAAAAC/love-hug.gif",
	"https://c.tenor.com/7zb6sgeEKIEAAAAC/snap.gif",
	"https://c.tenor.com/5UwhB5xQSTEAAAAC/anime-hug.gif",
	"https://c.tenor.com/H7i6GIP-YBwAAAAC/a-whisker-away-hug.gif",
	"https://c.tenor.com/S3KQ1sDod7gAAAAC/anime-hug-love.gif",
	"https://c.tenor.com/n0qIE_8B0JcAAAAC/gif-abrazo.gif",
	"https://c.tenor.com/AvXyGGhalDsAAAAC/anime-hug.gif",
	"https://c.tenor.com/ggKei4ayfIAAAAAC/anime-hug.gif",
	"https://c.tenor.com/TJuvig1CFBQAAAAd/the-pet-girl-of-sakurasou-sakurasou-no-pet-na-kanojo.gif",
	"https://c.tenor.com/we1trpFB2F0AAAAC/neko-hug.gif",
	"https://c.tenor.com/mB_y2KUsyuoAAAAC/cuddle-anime-hug.gif",
	"https://c.tenor.com/-3I0yCd6L6AAAAAC/anime-hug-anime.gif",
	"https://c.tenor.com/TBU7HopBhYgAAAAC/anime-anime-hug.gif",
	"https://c.tenor.com/XyMvYx1xcJAAAAAC/super-excited.gif",
	"https://c.tenor.com/Cy8RWMcVDj0AAAAd/anime-hug.gif",
	"https://c.tenor.com/gyiM68xD1MQAAAAC/anime-cute.gif",
}

var SlapGIFs = []string{
	"https://media1.tenor.com/images/477821d58203a6786abea01d8cf1030e/tenor.gif",
	"https://media1.tenor.com/images/fe39cfc3be04e3cbd7ffdcabb2e1837b/tenor.gif",
	"https://media1.tenor.com/images/612e257ab87f30568a9449998d978a22/tenor.gif",
	"https://media1.tenor.com/images/a9b8bd2060d76ec286ec8b4c61ec1f5a/tenor.gif",
	"https://media1.tenor.com/images/9ea4fb41d066737c0e3f2d626c13f230/tenor.gif",
	"https://media1.tenor.com/images/3fd96f4dcba48de453f2ab3acd657b53/tenor.gif",
	"https://media1.tenor.com/images/528ff731635b64037fab0ba6b76d8830/tenor.gif",
	"https://media1.tenor.com/images/d14969a21a96ec46f61770c50fccf24f/tenor.gif",
	"https://media1.tenor.com/images/416ce127ae441cff2825ce2b992df736/tenor.gif",
	"https://media1.tenor.com/images/7437caf9fb0bea289a5bb163b90163c7/tenor.gif",
	"https://media1.tenor.com/images/0a3e109296e16977a61ed28c1e5bf7bf/tenor.gif",
}

// KissGIF returns a random kiss gif.
func KissGIF() string {
	nBig, err := rand.Int(rand.Reader, big.NewInt(int64(len(KissGIFs))))
	if err != nil {
		return ""
	}
	n := nBig.Int64()
	return KissGIFs[n]
}

// HugGIF returns a random hug gif.
func HugGIF() string {
	nBig, err := rand.Int(rand.Reader, big.NewInt(int64(len(HugGIFs))))
	if err != nil {
		return ""
	}
	n := nBig.Int64()
	return HugGIFs[n]
}

// SlapGIF returns a random slap gif.
func SlapGIF() string {
	nBig, err := rand.Int(rand.Reader, big.NewInt(int64(len(SlapGIFs))))
	if err != nil {
		return ""
	}
	n := nBig.Int64()
	return SlapGIFs[n]
}
