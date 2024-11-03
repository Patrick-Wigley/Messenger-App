import socket
import threading
import sys
import os

import GlobalItems

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Shared.SharedTools import (pairing_function, 
                           extract_cmd,
                           handle_send,
                           handle_recv)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open("Shared\\details", "r") as file:
    data = file.read()
    if data:
        IP = data
        SERVER_IP = data
    else:
        IP = input("Devices assigned IP on subnet ->: ") #socket.gethostbyname(socket.gethostname())
        SERVER_IP = input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())


PORT = 5055
ADDR = (IP, PORT)
SERVER_LOCATION = (SERVER_IP, 5055)

kill_all_non_daemon = False


def login_handle() -> bool:
    """ Ran before main socket communications occurs, handles login """
    while not GlobalItems.logged_in:
        inputted_account_details = None if len(GlobalItems.send_server_msg_buffer) == 0 else GlobalItems.send_server_msg_buffer.pop()
        if inputted_account_details:
            cmd, args = extract_cmd(inputted_account_details)
            handle_send(client, SERVER_LOCATION, cmd=cmd, args=args)
            
            received = handle_recv(client, SERVER_LOCATION)
            if received:
                cmd, args = received
                if cmd == "login" or cmd == "register":
                    if args[0] == "SUCCESS":
                        # Successfully logged into account
                        # stores login for when logging in again
                        with open("cache.txt", "w") as cached_login:
                            # NOTE: FINISH USING JSON
                            cached_login.write(f"{inputted_account_details}")
                            cached_login.close()
                        GlobalItems.logged_in = True
                        
                        # Let window know
                        if cmd == "login":
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[login](_, True)")
                        else:
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[register](_, True)")
                    elif args[0] == "FAIL":
                        if cmd == "login":
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[login](Username_or_Password_is_incorrect, False)")
                        else:
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[register](Username_or_Email_is_taken, False)")
                else:
                    print(f"Received incorrect data from server? {received}")
                # elif cmd == "register":
                #     print(args)
                #     if args[0] == "SUCCESS":
                #         GlobalItems.interpreted_server_feedback_buffer.append("#IC[register](_, True)")
                #     elif args[0] == "FAIL":
                #         GlobalItems.interpreted_server_feedback_buffer.append("#IC[register](Username_or_Email_is_taken, False)")



def handle_exit():
    print(f"Exiting thread: {threading.get_ident()}!")
    # Need to tell server
    handle_send(client, SERVER_LOCATION, "exit")


def server_handle():
    """ All server connection, communications will be handled here 
        This is ran in its own thread - while it is daemon, it needs to be READ-ONLY. Cannot ask for inputs, no interupts and etc. """

    global kill_all_non_daemon
    
    try:
        client.connect(SERVER_LOCATION)
        print(f"Successfully Connected to server at {SERVER_LOCATION}")
    except socket.error as e:
        print(e)
        sys.exit()

    # logged_in is a global here in 'client.py'
    login_handle()
    print("Logged in" if GlobalItems.logged_in else "NOT LOGGED IN")

    while True:
        # Logic here is if buffer has something to send to server, will shoot it off & receive something back

        # Current setup is stack - (in final product this should ideally be queued)
        request_out = None if len(GlobalItems.send_server_msg_buffer) == 0 else GlobalItems.send_server_msg_buffer.pop()             #input("->: ")
        if request_out:
            if "exit" in request_out:
                handle_exit()
                break
            if request_out == "call":
                # Needs arg of person sending to & this persons id
                session_id = pairing_function(_, _)

            # Should be "if request_out contains 'message' - (This should become a command with args as the person send to and the message being sent) "
            # #IC[msg] (Goku, 'hello, how are we Kakarot')
            elif request_out:
                client.send(request_out.encode("utf-8"))           

            #NOTE: After sending a cmd, should receive something back from server always. Even just an acknowledgement



def establish_p2p_private_connection():
    """ From client need to request to p2p connect to a client. Server should pair other person if they wish to communicate 
       """



# Begin 
if __name__ == "__main__":
    # Probably run some tests? 
    print("This doesn't run directly yet")

else:
    # -- Runs through MainWindow.py
    print("Hello from client.py")
    # main thread will remain free.
  
   

def get_server_handle() -> server_handle:
    return server_handle
   