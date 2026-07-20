A solution to Discord's problem of not detecting activities on Ubuntu Linux. This program detects configured processes and activates a corresponding rich presence for Discord. Built-in search for detectable applications by calling https://discord.com/api/v10/games/detectable.


made this because i want my situationship to be able to see the games im playing and discord won't detect my games on ubuntu!!! i have no idea what i'm doing but it seems i'm making progress

many many thanks to the people in the Discord Linux (https://discord.gg/discord-linux) & Discord Developers (https://discord.gg/discord-developers) communities. i would have given up by now w/o their guidance (https://discord.com/channels/613425648685547541/1130595287078015027/1528497133412552765 & https://discord.com/channels/96230004047740928/257592796704145429/1528494216358133892)

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

# 3. If it complains about "xcb" (this instruction was from the original thing i forked from: https://github.com/0xmakarov/discord-rpc-linux idk if it's needed)
sudo apt install libxcb-cursor0

# 4. Run it
./run.sh
```
