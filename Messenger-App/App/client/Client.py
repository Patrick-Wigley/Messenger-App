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
                           extract_cmd, format_ic_cmd,
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
pub_priv_key = []
kill_all_non_daemon = False

server_specific_buffer = []


def login_handle() -> bool:
    """ Ran before main socket communications occurs, handles login """
    while not GlobalItems.logged_in:
        inputted_account_details = None if len(GlobalItems.request_out_buffer) == 0 else GlobalItems.request_out_buffer.pop()
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
    handle_send(client, SERVER_LOCATION, CMD.EXIT)
    

def server_handle():
    """ All server interacts, communications will be handled here 
        This is ran in its own thread - while it is daemon, it needs to be READ-ONLY. Cannot ask for inputs, no interupts and etc. """
    global kill_all_non_daemon, private_key, servers_session_pub_key, pub_priv_key
    
    # CONNECT TO SERVER
    handle_connect()

    # KEY GEN & SHARE
    # Sessions Key Generation 
    pub_key, private_key = gen_keys()
    # Share Generated Public Key & Recieve Servers Public Key FOR THIS SESSION
    servers_session_pub_key = handle_pubkey_share(client, SERVER_LOCATION, pub_key, verbose=True)
    pub_priv_key = [servers_session_pub_key, private_key]


    # LOGIN
    # logged_in is a global here in 'client.py'
    login_handle()
    print("Logged in" if GlobalItems.logged_in else "NOT LOGGED IN")

    # Spin up two threads, one for pushing messages out to the server, another for receiving messages 

    # MAIN NETWORK LOOP FOR PROGRAM - Handles all ingoings & outgoings of commands & their respective data
    if GlobalItems.logged_in:
        t_requests_out = threading.Thread(target=handle_requests_out, args=([servers_session_pub_key]))
        t_requests_in = threading.Thread(target=handle_requests_in, args=([private_key]))
        t_requests_out.start()
        t_requests_in.start()   

        while True:
            GlobalItems.request_out_buffer.append(f"#IC[{input('Command ->: ')}]({input('Args (arg1, arg2, ..) ->: ')})")
        
    else:
        print("Failed to log in. Bye!")


def handle_requests_out(pub_key):
    """ Will run in its own thread """
    while True:
        # Logic here is if buffer has something to send to server, will shoot it off & receive something back

        # Current setup is stack - (in final product this should ideally be queued)
        # request_out will contain the command set from the window-module to do something with it here networkly
        request_out = None if len(GlobalItems.request_out_buffer) == 0 else GlobalItems.request_out_buffer.pop()
        if request_out:
            if CMD.EXIT in request_out:
                    handle_exit()
                    break
            else:
                handle_send(conn=client, request_out=request_out, pub_key=pub_key)


def handle_requests_in(priv_key):
    while True:
        received = handle_recv(client, SERVER_LOCATION, priv_key=priv_key)
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
                print(f"BROADCAST: {args[0]}")
            elif cmd == CMD.BROADCAST_NOT_ALLOWED:
                GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.BROADCAST_NOT_ALLOWED))


            else:
                print(f"Received something unexpcted from server: {received}")




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
        GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.GETSAVECONTACTCHATS, args))
    else:
        GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.GETSAVECONTACTCHATS, False))

def handle_save_contact(args) -> None:
    if args[0] == True:
        print("Server sucessfuly saved contact")
        GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.SAVECONTACT, True))
    else:
        print("Something went wrong when attempting to save contact")
        GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.SAVECONTACT, False))

def handle_search_contacts(args) -> None:
    print(f"Received: {args}")
    if args[0]:
        # Found results
        GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.SEARCHCONTACT, args))
    else:
        # Did NOT find results
        GlobalItems.interpreted_server_feedback_buffer.append(format_ic_cmd(CMD.SEARCHCONTACT, False))



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