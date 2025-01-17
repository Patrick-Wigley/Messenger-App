# THIRD PARTY
import socket
import threading
import sys
import os
from pathlib import Path
import time



# MESSENGER APP MODULES
import GlobalItems
# Client Specific
from Ap_Tools import (
    save_credentials_cache,
    save_ip_details,
    loop_function,
    HandleIncommingCommands
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Shared.SharedTools import (CMD,
                           extract_cmd, format_ic_cmd,
                           handle_send,
                           handle_recv,
                           handle_pubkey_share,
                           gen_keys)
# END OF IMPORTS



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


@loop_function
def handle_authenticate(autoconnect: list) -> bool:
    if autoconnect[0]:
        print("Relogging in")
        handle_login(autoconnect=True)
    else:
        inputted_account_details = None if len(GlobalItems.request_out_buffer) == 0 else GlobalItems.request_out_buffer.pop()
        if inputted_account_details:
            if CMD.LOGIN in inputted_account_details:
                handle_login(False, inputted_account_details)
            elif CMD.REGISTER in inputted_account_details:
                handle_register(inputted_account_details)
            else:
                print(f"RECEIVED SOMETHING UNEXCPTED WHILE HANDLING AUTHENTICATION - {inputted_account_details}")
    
    return not GlobalItems.logged_in
        
     


def handle_connect():
    while True:
        try:
            client.connect(SERVER_LOCATION)
            print(f"Successfully Connected to server at {SERVER_LOCATION}")
            save_ip_details(IP, SERVER_IP)
            break
        except socket.error as e:
            print(f"Failed to connect to server - it may be down - {e}")
            time.sleep(5)
def handle_auto_reconnect():
    global client
    print("ATTEMPTING TO RECONNECT")
    # Reinstatiate socket
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    handle_initial_communications(autoconnect=True)

def handle_exit():
    print(f"Exiting thread: {threading.get_ident()}!")
    # Need to tell server
    handle_send(client, SERVER_LOCATION, CMD.EXIT)
    sys.exit()

def handle_get_keys():
    global servers_session_pub_key, private_key

    # KEY GEN & SHARE
    pub_key, private_key = gen_keys()
    # Share pub_key and recevied server_session_pub_key
    servers_session_pub_key = handle_pubkey_share(client, SERVER_LOCATION, pub_key, verbose=True)

    
def handle_initial_communications(autoconnect=False):
    """ Handles Connection, Key-Share, Authentiction """
    GlobalItems.logged_in = False

    # CONNECT TO SERVER
    handle_connect()
    # GENERATE KEYS AND GET SERVERS PUBLIC KEY
    handle_get_keys()
    # LOGIN OR REGISTER
    handle_authenticate(autoconnect=autoconnect)


def server_handle():
    """ Main function for network side of client """ 
    
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


@loop_function
def handle_requests_out() -> bool:
    """ Will run in its own thread """
    global servers_session_pub_key

    # request_out will contain the command sent from the window-module
    request_out = None if len(GlobalItems.request_out_buffer) == 0 else GlobalItems.request_out_buffer.pop()
    if request_out and GlobalItems.logged_in:
            if CMD.EXIT in request_out:
                    handle_exit()
                    return False # Do not Loop again
            else:
                handle_send(conn=client, request_out=request_out, pub_key=servers_session_pub_key)
    return True # Loop again

@loop_function
def handle_requests_in() -> bool:
    """ Will run in its own thread """
    global private_key
  
    received = handle_recv(client, SERVER_LOCATION, priv_key=private_key)
    if received:
        cmd, args = received

        if cmd == CMD.CALLPERSON:
            # Needs arg of person sending to & this persons id
            HandleIncommingCommands.handle_call_person(args, IP)

        elif cmd == CMD.SEARCHCONTACT:
            HandleIncommingCommands.handle_search_contacts(args)

        elif cmd == CMD.SAVECONTACT:
            HandleIncommingCommands.handle_save_contact(args)

        elif cmd == CMD.GETSAVECONTACTCHATS:
            HandleIncommingCommands.handle_get_chats(args) # MAKE BUTTON TO GET THIS REQUEST GOING

        elif    cmd == CMD.GETMESSAGEHISTORY or\
                cmd == CMD.SENDMESSAGE or\
                cmd == CMD.UPDATE_CHAT_LOG_LIVE or\
                cmd == CMD.BROADCAST or\
                cmd == CMD.BROADCAST_NOT_ALLOWED or\
                cmd == CMD.STILL_CONNECTED:
        
            HandleIncommingCommands.update_window_event_trigger(cmd=cmd, args=args)


        else:
            print(f"Received something unexpcted from server: {received}")
    else:
        # Server has turned off - Begin auto-reconnecting 
        handle_auto_reconnect() # Will return once succesfully reconnected & logged in
    
    return True # Loop again



# Begin 
if __name__ == "__main__":
    # Probably run some tests? 
    print("This doesn't run directly yet")

else:
    # -- Runs through MainWindow.py
    print("Hello from client.py")
    # main thread will remain free.

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
        IP = input("Devices assigned IP on subnet ->: ")        #socket.gethostbyname(socket.gethostname())
        SERVER_IP = input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())


    PORT = 5055
    ADDR = (IP, PORT)
    SERVER_LOCATION = (SERVER_IP, 5055)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servers_session_pub_key = None
    private_key = None
    kill_all_non_daemon = False


  
   

def get_server_handle() -> server_handle:
    return server_handle