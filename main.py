import time
import psutil

from pypresence import Presence

# client_id = "358425800766128128"
# RPC = Presence(client_id)  # Initialize the client class
# RPC.connect()  # Start the handshake loop

# if input("Y to disconnect: ").lower() == "y":
#     RPC.close()

config = True

while True:
    if config:
        ans = input("\nPlease select what you want to do:\n Type 'p' to see currently running processes.\n Type 's' to add a process to the dectection list.\n Type 'a' to activate the detector.\n\n> ")
        if ans.lower() == "p":
            print("\nrocesses that are currently running:")
            for p in psutil.process_iter():
                print(str(p.pid)+" "+str(p.name()))
        elif ans.lower() == "s":
            processName = input("\nPlease write the exact name of the process you want to add to the detection list, case sensitive\n> ")
            
            list = open("list.txt", "a")
            list.write(str(processName)+"\n")
            list.close()

            print("\nWritten. Deleting processes from the list must be done manually, by editing the file list.txt.\n")
        elif ans.lower() == "a":
            config = False
    else:
        time.sleep(10)
        list = open("list.txt", "r")
        content = list.read()
        list.close()
        listed = content.split("\n")
        for p in psutil.process_iter():
            for i in listed:
                if p.name() == i:
                    print("detected "+ i)
        print("finished detecting")
            
            



# while True:  # The presence will stay on as long as the program is running
    # time.sleep(15)  # Can only update rich presence every 15 seconds
