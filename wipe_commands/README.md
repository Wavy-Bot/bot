<p align="center">
    <a href="https://wavybot.com">
        <img src="https://user-images.githubusercontent.com/42699143/209726312-2fa4f736-bc01-499c-beb2-6d0ebf22c689.png" alt="Wavy" width="900" style="border-radius: 10px">
    </a>
</p>

<p align="center">
    <a href="LICENSE.md">
        <img src="https://img.shields.io/badge/LICENSE-MIT?color=%23a51931&labelColor=%23a51931&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCEtLXphei0tPgo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgaGVpZ2h0PSIxNjYiIHdpZHRoPSIzMjEiPgo8ZyBzdHJva2Utd2lkdGg9IjM1IiBzdHJva2U9IiNGRkZGRkYiPgo8cGF0aCBkPSJtMTcuNSwwdjE2Nm01Ny0xNjZ2MTEzbTU3LTExM3YxNjZtNTctMTY2djMzbTU4LDIwdjExMyIvPgo8cGF0aCBkPSJtMTg4LjUsNTN2MTEzIiBzdHJva2U9IiNGRkZGRkYiLz4KPHBhdGggZD0ibTIyOSwxNi41aDkyIiBzdHJva2Utd2lkdGg9IjMzIi8+CjwvZz4KPC9zdmc+&logoWidth=25&style=for-the-badge" alt="MIT License">
    </a>
    <a href="https://discord.wavybot.com">
        <img src="https://img.shields.io/discord/710436465938530307?color=%235865F2&labelColor=%235865F2&label=Discord&logo=discord&logoColor=white&style=for-the-badge" alt="Wavy's Discord support server member count">
    </a>
    <a href="go.mod">
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

# Wavy command wiper

This is a simple command wiper that will wipe all global application commands associated with the current bot application from your Discord server. It also supports wiping all application commands from the admin guild provided in the configuration.

## Usage

First, clone the entire repository and install the dependencies:

```bash
go get
``` 

Then, copy `.env.example` to `.env` and fill in the required values.

Finally, run the command wiper:

```bash
cd wipe_commands
go run main.go
```

## License
See [LICENSE.MD](LICENSE.md).