# THIRD PARTY
import socket
import threading
import sys
import os
import rsa

# MESSENGER APP MODULES
import GlobalItems
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.UDPCalling.Send import begin_send_audio_data
from client.UDPCalling.Receive import begin_recv_audio_data
from Shared.SharedTools import (CMD,
                           extract_cmd,
                           handle_send,
                           handle_recv,
                           handle_pubkey_share,
                           gen_keys)


# Get stored IPV4 of servers location
with open("Shared\\details", "r") as file:
    data = file.read()
    if data:
        IP = data
        SERVER_IP = data
    else:
        IP = input("Devices assigned IP on subnet ->: ") #socket.gethostbyname(socket.gethostname())
        SERVER_IP = input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5055
ADDR = (IP, PORT)
SERVER_LOCATION = (SERVER_IP, 5055)
servers_session_pub_key = None
private_key = None

kill_all_non_daemon = False

server_specific_buffer = []


def login_handle() -> bool:
    """ Ran before main socket communications occurs, handles login """
    while not GlobalItems.logged_in:
        inputted_account_details = None if len(GlobalItems.send_server_msg_buffer) == 0 else GlobalItems.send_server_msg_buffer.pop()
        if inputted_account_details:
            handle_send(client, SERVER_LOCATION, request_out=inputted_account_details, pub_key=servers_session_pub_key, verbose=True)
            
            received = handle_recv(client, SERVER_LOCATION, priv_key=private_key)
            if received:
                cmd, args = received
                if cmd == CMD.LOGIN or cmd == CMD.REGISTER:
                    if "SUCCESS" in args[0]:
                        # Successfully logged into account
                        # stores login for when logging in again
                        with open("cache.txt", "w") as cached_login:
                            # NOTE: FINISH USING JSON
                            _, args = extract_cmd(inputted_account_details)
                            cached_login.write(f"{args}")
                            cached_login.close()
                        GlobalItems.logged_in = True
                        
                        print(f"Success on {cmd}")
                        # Let window know
                        if cmd == CMD.LOGIN:
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[login]('_', True)")
                        else:
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[register]('_', True)")
                    elif "FAIL" in args[0]:
                        if cmd == CMD.LOGIN:
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[login]('Username_or_Password_is_incorrect', False)")
                        else:
                            GlobalItems.interpreted_server_feedback_buffer.append("#IC[register]('Username_or_Email_is_taken', False)")
                else:
                    print(f"Received incorrect data from server? {received}")


def handle_connect():
    try:
        client.connect(SERVER_LOCATION)
        print(f"Successfully Connected to server at {SERVER_LOCATION}")
    except socket.error as e:
        print(e)
        sys.exit()
def handle_exit():
    print(f"Exiting thread: {threading.get_ident()}!")
    # Need to tell server
    handle_send(client, SERVER_LOCATION, "exit")


def server_handle():
    """ All server interacts, communications will be handled here 
        This is ran in its own thread - while it is daemon, it needs to be READ-ONLY. Cannot ask for inputs, no interupts and etc. """
    global kill_all_non_daemon, private_key, servers_session_pub_key
    
    # CONNECT TO SERVER
    handle_connect()

    # KEY GEN & SHARE
    # Sessions Key Generation 
    pub_key, private_key = gen_keys()
    # Share Generated Public Key & Recieve Servers Public Key FOR THIS SESSION
    servers_session_pub_key = handle_pubkey_share(client, SERVER_LOCATION, pub_key, verbose=True)
    pub_priv_keys = [servers_session_pub_key, private_key]


    # LOGIN
    # logged_in is a global here in 'client.py'
    login_handle()
    print("Logged in" if GlobalItems.logged_in else "NOT LOGGED IN")

    # MAIN NETWORK LOOP FOR PROGRAM - Handles all ingoings & outgoings of commands & their respective data
    if GlobalItems.logged_in:
        while True:
            # Logic here is if buffer has something to send to server, will shoot it off & receive something back

            # Current setup is stack - (in final product this should ideally be queued)
            # request_out will contain the command set from the window-module to do something with it here networkly
            request_out = None if len(GlobalItems.send_server_msg_buffer) == 0 else GlobalItems.send_server_msg_buffer.pop()
            if request_out:
                if CMD.EXIT in request_out:
                    handle_exit()
                    break

                elif CMD.CALLPERSON in request_out:
                    # Needs arg of person sending to & this persons id
                    handle_call_person(request_out=request_out, keys=pub_priv_keys)

                elif CMD.REFRESHCHATS in request_out:
                    handle_refresh_chats(request_out=request_out, keys=pub_priv_keys)

                elif CMD.SEARCHCONTACT in request_out:
                    handle_search_contacts(request_out=request_out, keys=pub_priv_keys)

                elif CMD.SAVECONTACT in request_out:
                    handle_save_contact(request_out=request_out, keys=pub_priv_keys)

                elif CMD.GETSAVECONTACTCHATS in request_out:
                    handle_get_chats(request_out=request_out, keys=pub_priv_keys) # MAKE BUTTON TO GET THIS REQUEST GOING

                elif CMD.GETMESSAGEHISTORY in request_out:
                    handle_get_chats_history(request_out=request_out, keys=pub_priv_keys)

                elif CMD.SENDMESSAGE in request_out:
                    handle_send_message(request_out=request_out, keys=pub_priv_keys)


                # Should be "if request_out contains 'message' - (This should become a command with args as the person send to and the message being sent) "
                # #IC[msg] (Goku, 'hello, how are we Kakarot')
                elif request_out:
                    client.send(request_out.encode("utf-8"))           

                #NOTE: After sending a cmd, should receive something back from server always. Even just an acknowledgement
    
        
    else:
        print("Failed to log in. Bye!")




# -=-= POST-LOGIN FUNCTIONS =-=- #
def handle_request_out_decor(func):
    def inner(*args, **kwargs):
        handle_send(conn=client, request_out=kwargs["request_out"], pub_key=kwargs["keys"][0])
        while True:
            received = handle_recv(client, SERVER_LOCATION, priv_key=kwargs["keys"][1])
            if received:
                cmd, args = received
                if cmd in CMD.REQUEST_OUT_CMDS:
                    func(cmd, args)
                    break

                elif cmd in CMD.SERVER_SPECIFIC:
                    # Received Broadcast
                    server_specific_buffer.append(received)

    return inner



# These takes parameters & works in-conjuction with 'server_handle()'"
# These functions send message and then wait for the appropriate response to handle it (SYNCHRONOUS)
@handle_request_out_decor
def handle_call_person(cmd, args) -> None:
    """IC = CallPerson"""
    
    if args[0] == False:
        print("Person cannot be called right now")
    else:
        # Shall receive OTHER PERSONS IPV4 to dial in
        print(f"CAN CALL - calling IPV4: {args}")
        begin_send_audio_data(args[0])
        
        print(f"MY IP IS: {IP}")
        begin_recv_audio_data(IP)


@handle_request_out_decor
def handle_send_message(cmd, args) -> None:
    """IC = SendMessage"""

    GlobalItems.interpreted_server_feedback_buffer.append(f"#IC[SendMessage]({args})")


@handle_request_out_decor
def handle_get_chats_history(cmd, args) -> None:
    """IC = GetMessagesHistory"""
 
    GlobalItems.interpreted_server_feedback_buffer.append(f"#IC[GetMessagesHistory]({args})")


@handle_request_out_decor
def handle_refresh_chats(cmd, args) -> None:
    """IC = RefreshChats"""
   
    print(cmd, " and args: ", args)
        

@handle_request_out_decor
def handle_get_chats(cmd, args) -> None:
    """IC = GetSavedContactsChats"""
    
    if cmd == "GetSavedContactsChats":
        if args[0] != False:
            GlobalItems.interpreted_server_feedback_buffer.append(f"#IC[GetSavedContactsChats]({args})")
        else:
            GlobalItems.interpreted_server_feedback_buffer.append("#IC[GetSavedContactsChats](False)")


@handle_request_out_decor
def handle_save_contact(cmd, args) -> None:
    """IC = SaveContact"""
        
    if cmd == "SaveContact":
        if args[0] == True:
            print("Server sucessfuly saved contact")
            GlobalItems.interpreted_server_feedback_buffer.append("#IC[SaveContact](True)")
        else:
            print("Something went wrong when attempting to save contact")
            GlobalItems.interpreted_server_feedback_buffer.append("#IC[SaveContact](False)")

@handle_request_out_decor
def handle_search_contacts(cmd, args) -> None:
    """IC = SearchContact"""
    # Sending straight away as already formatted = make function for error handling these.
    
    if cmd == "SearchContact":
        print(f"Received: {args}")
        if args[0]:
            # Found results
            GlobalItems.interpreted_server_feedback_buffer.append(f"#IC[SearchContact]({args})")
        else:
            GlobalItems.interpreted_server_feedback_buffer.append("#IC[SearchContact](False)")
            # Did NOT find results






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