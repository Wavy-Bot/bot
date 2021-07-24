[![Logo Image](https://cdn.wavybot.com/wavy_logo.png)](https://wavybot.com)

# Wavy

Wavy is an open-source multi-purpose Discord bot powered by [Discord.py](https://discordpy.readthedocs.io/en/latest/).

## Tools and services used

<table>
  <tr>
    <td align="center"><a href="https://www.python.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png" width="100px;" alt=""/><br /><sub><b>Python 3</b></sub></a><br /></td>
    <td align="center"><a href="https://www.postgresql.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1200px-Postgresql_elephant.svg.png" width="100px;" alt=""/><br /><sub><b>PostgreSQL</b></sub></a><br /></td>
    <td align="center"><a href="https://www.jetbrains.com/pycharm/"><img src="https://i2.wp.com/clay-atlas.com/wp-content/uploads/2019/10/PyCharm_Logo.svg_.png?resize=1024%2C1024&ssl=1" width="100px;" alt=""/><br /><sub><b>PyCharm Professional</b></sub></a><br /></td>
    <td align="center"><a href="https://deepsource.io/"><img src="https://static.crozdesk.com/web_app_library/providers/logos/000/011/711/original/deepsource-1608196869-logo.png?1608196869" width="100px;" alt=""/><br /><sub><b>Deepsource</b></sub></a><br /></td>
    <td align="center"><a href="https://some-random-api.ml/"><img src="https://i.some-random-api.ml/logo.png" width="100px;" alt=""/><br /><sub><b>Some Random API</b></sub></a><br /></td>
  </tr>
</table>

## To-do list
Stuff I'm still working on; It's quite a list, but it's (hopefully) worth it.
_You might notice a weird pattern of completed items in this list, but that's just because I am doing database-related stuff now since I was still deciding what db engine to use._


- [ ] General cog
    - [x] Ping
    - [ ] Better help
    - [x] User info 
    - [x] Server info
    - [x] Bot info
    - [x] Avatar
    - [x] Invite
    

- [ ] Moderation cog
    - [x] Kick
    - [x] Ban
    - [x] Softban
    - [x] Unban
    - [ ] Mute
    - [ ] Unmute
    - [ ] Warn
    - [ ] Unwarn
    - [ ] Warnings
    - [x] Clear
    - [x] Nuke
    - [ ] Lock
    - [ ] Unlock
    - [ ] Snipe
    

- [ ] Ticket cog
    - [ ] Open ticket
    - [ ] Close ticket
    - [ ] Delete ticket
    - [ ] Rename ticket
    - [ ] Ticket transcript
    - [ ] Add user 
    - [ ] Remove user
    - [ ] Ticket categories
    

- [ ] Fun cog
    - [x] Reddit
        - [x] Meme
        - [x] Dank meme
        - [x] Reddit
    - [x] Randomizers
        - [x] Ship
        - [x] Howgay
        - [x] pp
        - [x] 8ball
    - [x] Random images
        - [x] Cat
        - [x] Dog
        - [x] Sad cat
        - [x] Duck
        - [x] Bird
        - [x] Bunny
        - [x] Bear
        - [x] Fox
        - [x] Shiba
        - [x] Sloth
        - [x] Panda
        - [x] Red panda
        - [x] Koala
        - [x] Raccoon
        - [x] Kangaroo
        - [x] Whale
        - [x] Lizard
        - [x] HTTP_Cat
        - [x] HTTP_Dog
        - [x] HTTP_Duck
    - [x] AI
      - [x] Cleverbot
    - [ ] Minecraft
      - [x] Skin
      - [x] Head
      - [x] UUID
      - [ ] Hypixel (I'll have to make a custom package for this)
    - [x] Leveling
      - [x] Level
      - [x] Leaderboard
    - [x]  Other
        - [x] Kill
        - [x] Heal
        - [x] Slap
        - [x] Punch
        - [x] Kiss
        - [x] Lick
        - [x] Laugh
        - [x] Pocky
    

- [x] Music cog
    - [x] Join
    - [x] Play
    - [x] Pause
    - [x] Resume
    - [x] Skip
    - [x] Disconnect
    - [x] Volume
    - [x] Shuffle
    - [x] Volume
    - [x] Equalizer
    - [x] Queue
    - [x] Now playing
    - [x] Swap DJ
    

- [x] NSFW cog
    - [x] Hentai
    - [x] Porn
    - [x] rule34
    

- [ ] Events cog
    - [x] Welcome messages event (on_member_join)
    - [x] Leave messages event (on_member_remove)
    - [x] Leveling event (on_message)
    - [x] Logging event (kick, ban, message delete, etc.)
    - [x] Cleverbot event (on_message)
    - [x] Bot guild join event (on_guild_join)
    - [x] Error handler event (on_command_error)
    - [x] Add rows to DB on join (on_guild_join)
    - [x] Add rows to DB on remove (on_guild_remove)
    - [ ] Automod

## License

See [LICENSE.MD](https://github.com/Wavy-Bot/bot/blob/main/LICENSE.md).