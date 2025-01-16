# THIRD PARTY
import socket
import threading
import sys
import os
from pathlib import Path
import rsa
import time

# MESSENGER APP MODULES
import GlobalItems
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.UDPCalling.Send import begin_send_audio_data
from client.UDPCalling.Receive import begin_recv_audio_data
from Shared.SharedTools import (CMD,
                           extract_cmd, format_ic_cmd,
                           handle_send,
                           handle_recv,
                           handle_pubkey_share,
                           gen_keys)


file = Path(GlobalItems.IPS_FILE_LOCATION)
if file.exists():
    # Get stored IPV4 of servers location
    with open(GlobalItems.IPS_FILE_LOCATION, "r") as file:
        data = file.read()
        if data:
            ip, server_ip = data.split(",")
            IP = ip
            SERVER_IP = server_ip
else:
    IP = input("Devices assigned IP on subnet ->: ") #socket.gethostbyname(socket.gethostname())
    SERVER_IP = input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5055
ADDR = (IP, PORT)
SERVER_LOCATION = (SERVER_IP, 5055)
servers_session_pub_key = None
private_key = None
pub_priv_key = []
kill_all_non_daemon = False

server_specific_buffer = []



def save_credentials_cache(username_and_password: list) -> None:
    # stores login for when logging in again
    with open(GlobalItems.CREDENTIAL_CACHE_FILE_LOCATION, "w") as cached_login:
        # NOTE: FINISH USING JSON
        username, password = username_and_password[0], username_and_password[1]
        cached_login.write(f"{username},{password}")
        cached_login.close()


def handle_register(inputted_account_details):
    handle_send(client, SERVER_LOCATION, request_out=inputted_account_details, pub_key=servers_session_pub_key)
        
    received = handle_recv(client, SERVER_LOCATION, priv_key=private_key)
    if received:
        cmd, args = received
        if cmd == CMD.REGISTER:
            if args[0]:
                GlobalItems.logged_in = True
                print(f"Success on {cmd}")
                save_credentials_cache(extract_cmd(inputted_account_details)[1])

                GlobalItems.interpreted_server_feedback_buffer.append("#IC[register]('_', True)")
            else:
                GlobalItems.interpreted_server_feedback_buffer.append("#IC[register]('Username_or_Email_is_taken', False)")

def handle_login(autoconnect, inputted_account_details=None):
    if autoconnect:
        cache_file = Path(GlobalItems.CREDENTIAL_CACHE_FILE_LOCATION)
        if cache_file.exists():
            with open(GlobalItems.CREDENTIAL_CACHE_FILE_LOCATION, "r") as cached_login:
                username, password = str(cached_login.read()).split(",")
                handle_send(client, SERVER_LOCATION, 
                            request_out=f"#IC[{CMD.LOGIN}]('{username}', '{password}')",
                            pub_key=servers_session_pub_key, verbose=True)        
        else:
            print("ERROR ON RECONNECT - CACHE HAS BEEN CORRUPTED OR DELETED")
            return sys.exit()
    else:
        handle_send(client, SERVER_LOCATION, request_out=inputted_account_details, pub_key=servers_session_pub_key, verbose=True)
            
    received = handle_recv(client, SERVER_LOCATION, priv_key=private_key, verbose=True)
    if received:
        cmd, args = received
        if cmd == CMD.LOGIN:
            if args[0]:
                # Successfully logged into account
                if not autoconnect:
                    save_credentials_cache(extract_cmd(inputted_account_details)[1])
                    # Let window know
                    GlobalItems.interpreted_server_feedback_buffer.append("#IC[login]('_', True)")

                GlobalItems.logged_in = True
                print(f"Success on {cmd}")
            else:
                if autoconnect:
                    print("[RELOGIN WAS NOT ACCEPTED]")
                    sys.exit()
                else:
                    GlobalItems.interpreted_server_feedback_buffer.append("#IC[login]('Username_or_Password_is_incorrect', False)")
        else:
            print(f"RECIEVED SOMETHING UNEXPECTED - {received}")


def handle_authenticate(autoconnect):
    while not GlobalItems.logged_in:
        if autoconnect:
            print("Relogging in")
            handle_login(autoconnect=True)
        else:
            inputted_account_details = None if len(GlobalItems.request_out_buffer) == 0 else GlobalItems.request_out_buffer.pop()
            if inputted_account_details:
                if CMD.LOGIN in inputted_account_details:
                    handle_login(autoconnect, inputted_account_details)
                elif CMD.REGISTER in inputted_account_details:
                    handle_register(inputted_account_details)
                else:
                    print(f"RECEIVED SOMETHING UNEXCPTED WHILE HANDLING AUTHENTICATION - {inputted_account_details}")
            
     

def save_ip_details():
    with open("Shared\\details", "w") as file:
        file.write(f"{IP},{SERVER_IP}")
        file.close()
def handle_connect():
    while True:
        try:
            client.connect(SERVER_LOCATION)
            print(f"Successfully Connected to server at {SERVER_LOCATION}")
            save_ip_details()
            break
        except socket.error as e:
            print(f"Failed to connect to server - it may be down - {e}")
            time.sleep(5)


def handle_exit():
    print(f"Exiting thread: {threading.get_ident()}!")
    # Need to tell server
    handle_send(client, SERVER_LOCATION, CMD.EXIT)
    
def handle_get_keys():
    global servers_session_pub_key, private_key

    # KEY GEN & SHARE
    pub_key, private_key = gen_keys()
    # Share pub_key and recevied server_session_pub_key
    servers_session_pub_key = handle_pubkey_share(client, SERVER_LOCATION, pub_key, verbose=True)

    
def handle_initial_communications(autoconnect=False):
    GlobalItems.logged_in = False

    # CONNECT TO SERVER
    handle_connect()
    # GENERATE KEYS AND GET SERVERS PUBLIC KEY
    handle_get_keys()
    # LOGIN OR REGISTER
    handle_authenticate(autoconnect)


def server_handle():
    """ All server interacts, communications will be handled here 
        This is ran in its own thread - while it is daemon, it needs to be READ-ONLY. Cannot ask for inputs, no interupts and etc. """
    global kill_all_non_daemon, private_key, servers_session_pub_key, pub_priv_key
    
    handle_initial_communications()

    print("Logged in" if GlobalItems.logged_in else "NOT LOGGED IN")

    # Spin up two threads, one for pushing messages out to the server, another for receiving messages from server
    if GlobalItems.logged_in:
        t_requests_out = threading.Thread(target=handle_requests_out)
        t_requests_in = threading.Thread(target=handle_requests_in)
        t_requests_out.start()
        t_requests_in.start()   

        while True:
            GlobalItems.request_out_buffer.append(f"#IC[{input('Command ->: ')}]({input('Args (arg1, arg2, ..) ->: ')})")
        
    else:
        print("Failed to log in. Bye!")


def loop_functions(func):
    def inner():
        while True:
            result = func()
            if result == False:
                break
    return inner

@loop_functions
def handle_requests_out() -> bool:
    """ Will run in its own thread """
    global servers_session_pub_key

    # request_out will contain the command sent from the window-module
    request_out = None if len(GlobalItems.request_out_buffer) == 0 else GlobalItems.request_out_buffer.pop()
    if request_out and GlobalItems.logged_in:
            if CMD.EXIT in request_out:
                    handle_exit()
                    return False # Break Loop
            else:
                handle_send(conn=client, request_out=request_out, pub_key=servers_session_pub_key)
    return True # Do not break loop

@loop_functions
def handle_requests_in() -> bool:
    """ Will run in its own thread """
    global private_key
  
    received = handle_recv(client, SERVER_LOCATION, priv_key=private_key)
    if received:
        cmd, args = received

        if cmd == CMD.CALLPERSON:
            # Needs arg of person sending to & this persons id
            handle_call_person(args)

        elif cmd == CMD.SEARCHCONTACT:
            handle_search_contacts(args)

        elif cmd == CMD.SAVECONTACT:
            handle_save_contact(args)

        elif cmd == CMD.GETSAVECONTACTCHATS:
            handle_get_chats(args) # MAKE BUTTON TO GET THIS REQUEST GOING

        elif cmd == CMD.GETMESSAGEHISTORY:
            handle_get_chats_history(args)

        elif cmd == CMD.SENDMESSAGE:
            handle_send_message(args)

        elif cmd == CMD.UPDATE_CHAT_LOG_LIVE:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.UPDATE_CHAT_LOG_LIVE, args))

        elif cmd == CMD.BROADCAST:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.BROADCAST, args))
        elif cmd == CMD.BROADCAST_NOT_ALLOWED:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.BROADCAST_NOT_ALLOWED))

        elif cmd == CMD.STILL_CONNECTED:
            GlobalItems.request_out_buffer.append(format_ic_cmd(CMD.STILL_CONNECTED))
        else:
            print(f"Received something unexpcted from server: {received}")
    else:
        # Server has turned off - Begin auto-reconnecting 
        handle_auto_reconnect() # Will return once succesfully reconnected & logged in
    
    return True # Do not break loop

def handle_auto_reconnect():
    global client
    print("ATTEMPTING TO RECONNECT")
    
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    handle_initial_communications(autoconnect=True)


def handle_call_person(args) -> None:    
    if args[0] == False:
        print("Person cannot be called right now")
    else:
        # Shall receive OTHER PERSONS IPV4 to dial in
        print(f"CAN CALL - calling IPV4: {args}")
        begin_send_audio_data(args[0])
        
        print(f"MY IP IS: {IP}")
        begin_recv_audio_data(IP)

def handle_send_message(args) -> None:
    #GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.SENDMESSAGE, args)) SYNC
    GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SENDMESSAGE, args))    # ASYNC

def handle_get_chats_history(args) -> None:
    GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.GETMESSAGEHISTORY, args))


def handle_get_chats(args) -> None:
    if args[0] != False:
        GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.GETSAVECONTACTCHATS, args))
    else:
        GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.GETSAVECONTACTCHATS, False))

def handle_save_contact(args) -> None:
    if args[0] == True:
        print("Server sucessfuly saved contact")
        GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SAVECONTACT, True))
    else:
        print("Something went wrong when attempting to save contact")
        GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SAVECONTACT, False))

def handle_search_contacts(args) -> None:
    print(f"Received: {args}")
    if args[0]:
        # Found results
        GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SEARCHCONTACT, args))
    else:
        # Did NOT find results
        GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SEARCHCONTACT, False))



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