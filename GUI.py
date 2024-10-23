# This will be using TKinter 
# My plan is to make a messager application with file & textual sending capabilities.

from Client import *

import sys
import time


print("gui stuff")
while True:
    # main thread does nothing yet. just idles, to keep server running till manual closure
    msg = input("From Main Thread! ->: ")
    message_buffer.append(msg)
    
    if msg == "exit":
        print("Exiting MAIN THREAD!")
        break