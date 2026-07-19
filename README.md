this is NOT done


making this because i want my situationship to be able to see the games im playing and discord won't detect my games on ubuntu!!!

original custom rpc made by 0xmakarov
expanded upon by me

sorry for the bunch of bad quality commit messages but yeah


similar install instructions as original:
```bash
# 1. Clone the repo
git clone https://github.com/2p2i5/linux-activitydetection-discord-rpc
cd linux-activitydetection-discord-rpc

# 2. Set up a venv and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# if pip gives you some trouble, use this instead
# pip install -r requirements.txt --break-system-packages

# 3. If it complains about "xcb"
sudo apt install libxcb-cursor0

# 4. Run it
python3 main.py
```

but i added `run.sh` which you can run cuz i don't wanna think about how to run it when i do. and maybe it's easier to do a service if you just have a .sh(?)


oh btw, before running, register an app on Discord:
1. Go to https://discord.com/developers/applications → **New Application**
2. Copy the **Application ID** (that's your Client ID)
3. Under **Rich Presence → Art Assets**, upload the images you want to use

then jus paste the Client ID into the app, fill in Details/State, and hit **Activate Presence** (make sure Discord desktop is actually open first)
