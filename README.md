# discord-rpc-linux

Custom Discord Rich Presence for Linux, made because some custom rps only ships a
Windows build. Same idea: pick your Details/State text, set some images,
maybe a couple of buttons, hit activate, done. I decided to do it cuz i was bored tho

by 0xmakarov

## Heads up before you use it

Discord won't take a rich presence from just anything — you need your own
"application" registered on their developer portal. That's how CustomRPs
works too, it just hides this step from you. Here it's the opposite: you
register your own app, which means you control exactly what images show up.

### 1. Register an app on Discord

1. https://discord.com/developers/applications → New Application
2. Whatever name you give it is what shows up as "Playing `<name>`"
3. Copy the Application ID, that's your Client ID
4. Rich Presence → Art Assets → upload the images you want, each one gets a
   key (name you pick). You'll type that key into the app, not the file itself

### 2. Install deps (Kali / Debian)

Kali blocks system-wide pip by default, so either:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

or just force it:

```bash
pip install -r requirements.txt --break-system-packages
```

If Qt complains about missing `xcb` stuff:

```bash
sudo apt install libxcb-cursor0
```

### 3. Run it

```bash
python3 main.py
```

### 4. Using it

Paste your Client ID, fill in Details/State, image keys, buttons if you
want them, hit **Activate Presence**. Discord has to actually be open.

Profiles let you save different setups (one per game/thing) and switch
between them from the dropdown instead of retyping everything. Closing the
window just sends it to the tray, presence keeps running — use the tray
menu to quit for real.

## Files

- `main.py` — the GUI (PySide6)
- `presence_manager.py` — talks to Discord over IPC
- `profiles.py` — saves profiles to `~/.config/discord-rpc-linux/profiles.json`

## Known limitations

- Needs the Discord desktop client, not the browser version
- Flatpak Discord puts its IPC socket somewhere else
  (`~/.var/app/com.discordapp.Discord/...`), you may need to symlink it
  into `~/.config/discord/` — open an issue if this bites you
- You won't see your own buttons on your own profile, only other people
  looking at you will — that's just how Discord works, not a bug here
