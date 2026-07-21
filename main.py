import time
import psutil
import json

from pypresence import Presence
from pathlib import Path

# sorry for the sloppy code but at least it's not ai!!!!!
# i swear someday i will organize it into functions

sleepTime = 15 # The amount of time the program will pause before checking if the game is running again. Pypresence claimed that you can only change the RPC every 15 seconds, so the default is the recommendation. Not sure of the problems with ratelimit beyond that.
config = True
itopen = False
client_id = 0


def detectProcess():
    dalist = Path("list.json")
    if not dalist.exists():
        config = True
        print("!!! No game list found. Please configure some games first with the 's' option.")
        print("Exiting program...")
        time.sleep(3)
        quit()

    with open("list.json", "r") as f:
        content = json.load(f)

    for p in psutil.process_iter():
        for i in content["games"]:
            # print(i["processname"],p.name())
            if i["processname"] == p.name():
                # print("Found running process")
                return i["discordid"]
    
    return False

print("\n\n\n\n")
print("You are running version 1.0.2")
print("This project supports Palestine and is against AI usage.")

while True:
    if config:
        ans = input("\nPlease select what you want to do:\n Type 'p' to see currently running processes.\n Type 's' to add a process to the detection list.\n Type 'a' to activate the detector.\n\n> ")
        if ans.lower() == "p":
            print("\nProcesses that are currently running:")
            for p in psutil.process_iter():
                print(str(p.pid)+" "+str(p.name()))
        elif ans.lower() == "s":
            processName = input("\nPlease write the exact name of the process you want to add to the detection list, case sensitive\n> ")
            
            gameID = "none yet"
            searching = True
            while searching:
                searchers = input("\nTo display the corresponding rich presence for a process, the discord game ID of that process is needed. You can now either use different search terms to browse Discord's list of detectable programs (time this takes may depend on device), or input the game/application ID manually. The list is found by sending a request (including opening the page in a browser) to https://discord.com/api/v10/games/detectable, and you can search that list manually. Alternatively, you can make your own application in the Discord Developer Portal and put its client/application ID here (Discord TOS may have issues with making applications that 'impersonate' existing games, so be careful).\n Type 's' to search with terms.\n Type 'i' to manually add the ID.\n> ")
                if searchers == "i":
                    gameID = input("Input the ID now.\n> ")
                elif searchers == "s":
                    agreed = False
                    while not agreed:
                        terms = input("\nInput any search terms separated by only a comma (default is process name):\n> ").split(",")
                        if not terms or terms == [""]:
                            terms = [processName]
                        
                        print("Terms: \n"+str(terms))

                        if input("\nDoes this look right, or would you like to re-input the additional queries? (Y/N)\n> ").lower() == "y":
                            agreed = True
                        else:
                            terms = []

                    deteclis = open("detectable.json", "r")
                    with open("detectable.json", "r") as fil:
                        data = json.load(fil)
                    for gam in data:
                        # print("Game:"+str(gam["name"]))
                        for q in terms:
                            # print("query:"+str(q))
                            # print(str(gam["name"]).lower().__contains__(q.lower()))
                            if str(gam["name"]).lower().__contains__(q.lower()) and searching:
                                accepted = input("\nFound a match.\n Discord recorded game name: "+ gam["name"] +"\n Discord recorded game ID: "+ gam["id"]+ "\n\nWould you like to accept this, or keep searching? (Y/N)\n>")
                                if accepted.lower() == "y":
                                    gameID = gam["id"]
                                    searching = False
                                    break
                if gameID == "none yet":
                    print("No game ID found, resetting search.")

            confirm = input("\nDeducted that process name is '"+processName+"' and ID is '"+gameID+"'. Would you like to add this to the list now? (Y/N)\n> ")
            if confirm.lower() == "y":
                new_game = { "processname": processName, "discordid": gameID }
                dalist = Path("list.json")
                if not dalist.exists():
                    print("list.json doesn't exist, making one")
                    template = {"games":[{"processname":processName,"discordid": gameID}]}
                    with open('list.json', 'w') as json_file:
                        json.dump(template, json_file, indent=4)
                else:
                    with open("list.json", "r+") as file:
                        list = json.load(file)
                        list["games"].append(new_game)
                        file.seek(0)
                        json.dump(list, file, indent=4)

                print("\nWritten to list.json. Deleting processes from the list must be done manually, by editing the file list.json.\n")
        elif ans.lower() == "a":
            config = False
            print("\nStarting detection..")
    else:
        identity = detectProcess()
        if identity != False and identity != client_id:
            if itopen:
                RPC.close()
                itopen = False
            client_id = identity
            print("attempting to set rpc to "+identity)
            RPC = Presence(client_id)
            RPC.connect()
            RPC.update()
            itopen = True
        elif identity == client_id and itopen:
            try:
                RPC.close()
                itopen = False
            except():
                print("exception")
        
        time.sleep(sleepTime) # the pypresence thing said that you can only change presence every 15 seconds so i recommend that

