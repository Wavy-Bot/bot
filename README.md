<h4 align="center">Wavy is currently in alpha. This means that the bot is not yet ready for public use and things <i>will</i> break. ⚠️</h4>

<p align="center">
    <a href="https://wavybot.com">
        <img src="https://user-images.githubusercontent.com/42699143/209726312-2fa4f736-bc01-499c-beb2-6d0ebf22c689.png" alt="Wavy" width="900" style="border-radius: 10px">
    </a>
</p>

<p align="center">
    <a href="LICENSE.md">
        <img src="https://img.shields.io/github/license/Wavy-Bot/bot?color=%23a42e2b&labelColor=%23a42e2b&logo=gnu&style=for-the-badge" alt="GPL-3.0 License">
    </a>
    <a href="https://discord.wavybot.com">
        <img src="https://img.shields.io/discord/710436465938530307?color=%235865F2&labelColor=%235865F2&label=Discord&logo=discord&logoColor=white&style=for-the-badge" alt="Wavy's Discord support server member count">
    </a>
    <a href="go.mod.old">
        <img src="https://img.shields.io/github/go-mod/go-version/Wavy-Bot/bot?style=for-the-badge" alt="Go version">
    </a>
    <a href="https://github.com/Wavy-Bot/bot/stargazers">
        <img src="https://img.shields.io/github/stars/Wavy-Bot/bot?color=%23ffce3d&labelColor=&logo=github&style=for-the-badge" alt="Stargazers">
    </a>
</p>

<h4 align="center">The blazing-fast Discord bot.</h4>

<p align="center">
    <a target="_blank" href="https://discord.com/invite/Nbcf36Fge5">
        <img src="https://invidget.switchblade.xyz/Nbcf36Fge5" alt="Discord invite">
    </a>
</p>

<p align="center">
  <a href="https://wavybot.com">Website</a>
  •
  <a href="https://github.com/Wavy-Bot/bot">GitHub</a>
  •
  <a href="https://discord.wavybot.com" target="_blank">Discord</a>
</p>

<p align="center">
    <a target="_blank" href="https://hostvio.net">
        <img src="https://sq3.nl/images/hostvio.png" alt="Hostvio logo" width="900">
    </a>
    Proudly hosted by <a target="_blank" href="https://hostvio.net">Hostvio</a>
</p>

# Wavy
Wavy is an open-source Discord bot built with [DisGo](https://github.com/disgoorg/disgo).

## Feature requests
Want a new feature you think is missing? Please [open an issue](https://github.com/Wavy-Bot/bot/issues/new) or join [Wavy's Discord server](https://discord.wavybot.com) and we'll look into it!

## Community Standards
Please refer to the list of community standards below:
- [README](https://github.com/Wavy-Bot/bot/blob/main/README.md) (this file)
- [Code of Conduct](https://github.com/Wavy-Bot/bot/blob/main/CODE_OF_CONDUCT.md)
- [License](https://github.com/Wavy-Bot/bot/blob/main/LICENSE.md)
- [To-do list](https://github.com/Wavy-Bot/bot/projects/2)
- Clear roadmap (to be added)
- Contributing guidelines (to be added)
- Issue templates (to be added)
- Pull request templates (to be added)

## Versioning and releases
Wavy uses [Semantic Versioning](https://semver.org/). This means that the version number will be in the format of:

**major.minor.patch**
- **Major**: Breaking changes, the bot is no longer compatible with previous versions.
- **Minor**: New features, no breaking changes.
- **Patch**: Bug fixes and small improvements.

Next to that, any production-ready release will be pushed to the `production` branch, and any development release will be pushed to the `development` branch.

## How to use
The following has been tested on Alpine linux 3.17.x.

### Prerequisites:
- A terminal emulator or CMD (if on Windows).
- [git](https://git-scm.com/downloads)
- [Go, tested on 1.20.3](https://www.python.org/downloads/)
- [An app on Discord](https://discord.com/developers/applications) with bot usage enabled
- [A Lavalink instance](https://github.com/freyacodes/Lavalink)
- [A Sentry application](https://sentry.io)

```bash
git clone https://github.com/Wavy-Bot/bot.git
cd bot
```
Then copy the `.env.example` file to `.env` and edit it using your preferred text editor.

Afterwards, rename the `lavalink.example.json` file to `lavalink.json` and also edit that.

Finally, start the bot with the following commands:
```bash
go get
go build -o wavy cmd/wavy/main.go
./wavy
```

### Docker
If you want to use Docker instead, you can use the following commands:
```bash
docker volume create wavy-data
docker run -d --name wavy -v wavy-data:/wavy ghcr.io/wavy-wavy/wavy:production
```

## License
See [LICENSE.MD](LICENSE.md).