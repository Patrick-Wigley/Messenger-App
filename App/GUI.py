# This will be using TKinter 
# My plan is to make a messager application with file & textual sending capabilities.

from Client import *

import sys
import time

# NOTE 24/10/24 00:23
# Main thread is free. 
# populates buffer which is fed into stream inside Client.py.
# exit handling on server side and threads is done 
# Data sending thread is Daemon meaning it should close when program is finished - issue was having is non-daemon threads cant perform interupts



print("gui stuff")
while True:
    # main thread does nothing yet. just idles, to keep server running till manual closure
    try:
        msg = input("From Main Thread! ->: ")
        message_buffer.append(msg)
        
        
        if msg == "exit":
            print("Exiting MAIN THREAD!")
            break
    except KeyboardInterrupt as user_exit:
        message_buffer.append("exit")
        break