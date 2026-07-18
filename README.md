Ok, ajustando pra um meio-termo — natural, mas sem exagero:

```bash
# 1. Clone the repo
git clone https://github.com/0xmakarov/discord-rpc-linux
cd discord-rpc-linux

# 2. Set up a venv and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# (if pip gives you trouble, use this instead:)
# pip install -r requirements.txt --break-system-packages

# 3. If it complains about "xcb"
sudo apt install libxcb-cursor0

# 4. Run it
python3 main.py
```

Before running, register an app on Discord:
1. Go to https://discord.com/developers/applications → **New Application**
2. Copy the **Application ID** (that's your Client ID)
3. Under **Rich Presence → Art Assets**, upload the images you want to use

Then just paste the Client ID into the app, fill in Details/State, and hit **Activate Presence** — make sure Discord desktop is actually open first.
