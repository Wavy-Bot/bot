![GitHub](https://img.shields.io/github/license/Wavy-Bot/bot?color=A42E2B&logo=gnu&logoColor=white&style=for-the-badge)
[![Discord](https://img.shields.io/discord/710436465938530307?color=%235865F2&label=Discord&logo=discord&logoColor=white&style=for-the-badge)](https://discord.wavybot.com)
![Python version](https://img.shields.io/badge/Python-3.8-blue?style=for-the-badge&logo=python&logoColor=ffce3d&color=376f9e)
![GitHub Stars](https://img.shields.io/github/stars/Wavy-Bot/bot?color=%23ffce3d&logo=github&style=for-the-badge)

[![Logo Image](https://repository-images.githubusercontent.com/376505145/389bce00-cc35-11eb-8aab-bb86194ee165)](https://wavybot.com)

# Wavy
Wavy is an open-source Discord bot built with [Pycord](https://github.com/Pycord-Development/pycord). We are actively looking for contributors and beta testers, if you wish to participate please join [Wavy's Discord server](https://discord.wavybot.com)!

## Feature requests
Want a new feature you think is missing? Please [open an issue](https://github.com/Wavy-Bot/bot/issues/new) or join [Wavy's Discord server](https://discord.wavybot.com)!

## Tools and services used
<table>
    <tr>
        <td align="center"><a href="https://www.python.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png" width="100px;" alt="Python"/><br /><sub><b>Python 3</b></sub></a><br /></td>
        <td align="center"><a href="https://pycord.dev/"><img src="https://pycord.dev/static/img/logo.png?size=100" width="100px;" alt="Pycord"/><br /><sub><b>Pycord</b></sub></a><br /></td>
        <td align="center"><a href="https://www.mongodb.com/"><img src="https://cdn.iconscout.com/icon/free/png-256/mongodb-3629020-3030245.png" width="100px;" alt="MongoDB"/><br /><sub><b>MongoDB</b></sub></a><br /></td>
        <td align="center"><a href="https://github.com/Devoxin/Lavalink.py"><img src="https://serux.pro/9e83af1581.png" width="100px;" alt="Lavalink.py"/><br /><sub><b>Lavalink.py</b></sub></a><br /></td>
        <td align="center"><a href="https://www.jetbrains.com/pycharm/"><img src="https://i2.wp.com/clay-atlas.com/wp-content/uploads/2019/10/PyCharm_Logo.svg_.png?resize=1024%2C1024&ssl=1" width="100px;" alt="PyCharm"/><br /><sub><b>PyCharm</b></sub></a><br /></td>
        <td align="center"><a href="https://deepsource.io/"><img src="https://static.crozdesk.com/web_app_library/providers/logos/000/011/711/original/deepsource-1608196869-logo.png?1608196869" width="100px;" alt="Deepsource"/><br /><sub><b>Deepsource</b></sub></a><br /></td>
        <td align="center"><a href="https://sentry.io/"><img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia-exp1.licdn.com%2Fdms%2Fimage%2FC4D0BAQHke-g6rQfT6w%2Fcompany-logo_200_200%2F0%3Fe%3D2159024400%26v%3Dbeta%26t%3Daylls3BhohFGOtGX_opiZqRkxF9ZO91EIF3CEnm-xEQ&f=1&nofb=1" width="100px;" alt="Sentry"/><br /><sub><b>Sentry</b></sub></a><br /></td>
    </tr>
</table>
<table>
    <tr>
        <td align="center"><a href="https://hostvio.net"><img src="https://sq3.group/images/hostvio.png" alt="Hostvio"/><br /><sub><b>Hostvio</b></sub></a><br /></td>
    </tr>
</table>

## Community Standards
Please refer to the list of community standards below.
- [README](https://github.com/Wavy-Bot/bot/blob/main/README.md) (this file)
- [Code of Conduct](https://github.com/Wavy-Bot/bot/blob/main/CODE_OF_CONDUCT.md)
- [License](https://github.com/Wavy-Bot/bot/blob/main/LICENSE.md)
- [To-do list](https://github.com/Wavy-Bot/bot/projects/2)
- Clear roadmap (to be added)
- Contributing guidelines (to be added)
- Issue templates (to be added)
- Pull request templates (to be added)

## Versioning and releases
Wavy uses the following versioning pattern:

**major.minor.patch**
- **Major**: Breaking changes, the bot is no longer compatible with previous versions.
- **Minor**: New features, no breaking changes.
- **Patch**: Bug fixes and small improvements.

Next to that, any production-ready release will be pushed to the `release` branch, and any development release will be pushed to the `main` branch.

## How to use
The following has been tested on Ubuntu 20.04 and Alpine linux 3.16.x.

### Prerequisites:
- A terminal emulator or CMD (if on Windows).
- [git](https://git-scm.com/downloads)
- [Python >= 3.8, tested on 3.8.](https://www.python.org/downloads/)
- [An app on Discord](https://discord.com/developers/applications) with bot usage enabled
- [A Lavalink instance](https://github.com/freyacodes/Lavalink)
- [A MongoDB instance](https://www.mongodb.com/)
- [A Sentry application](https://sentry.io)
- [A Reddit application](https://www.reddit.com/prefs/apps)
- [A Spotify application](https://developer.spotify.com/dashboard/applications)
- [Top.gg API key (optional)](https://top.gg/)
- [Discord Bots API key (optional)](https://discord.bots.gg/)
- [Discord Bot List API key (optional)](https://discordbotlist.com/)
- [Discords API key (optional)](https://discords.com/)

```bash
git clone https://github.com/Wavy-Bot/bot.git
cd bot
```
Then copy the `.env.example` file to `.env` and edit it using your preferred text editor.

Afterwards, rename the `lavalink.example.json` file to `lavalink.json` and also edit that.

Finally, start the bot with the following commands:
```bash
# You may need to use the python, pip3 or pip command(s) instead of python3
# depending on your platform and/or linux distribution.
python3 -m pip install pipenv
pipenv install
python3 main.py
```

### Docker
If you want to use Docker instead, you can use the following commands:
```bash
docker volume create wavy-data
docker run -d --name wavy -v wavy-data:/app ghcr.io/wavy-bot/bot
```

Need more help? Join [Wavy's Discord server](https://discord.wavybot.com)!

## License
See [LICENSE.MD](https://github.com/Wavy-Bot/bot/blob/main/LICENSE.md).