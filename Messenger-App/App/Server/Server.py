# Needs a user login (AAA) Authentication, Authorisation & Auditing - Hash passwords - password resets & lockouts
# Needs Encryption of data sending
# Needs section to establish a p2p UDP socket between clients with keep-alive packets using pyaudio
# Needs to prevent replay attacks
#  

import socket
import threading
import sys
import os
from typing import Union

from dbModelManager import AccountManager, Account, ContactsManger, MessageManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Shared.SharedTools import (extract_cmd, 
                           list_to_str_with_commas,
                           handle_recv,
                           handle_send,
                           pairing_function)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with open("Shared\\details", "r") as file:
    data = file.read()
    if data:
        IP = data
    else:
        input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())
        
PORT = 5055
ADDR = (IP, PORT)

server.bind(ADDR)

# NOTE: THIS NEEDS TO BE USED SYNCHRONOUSLY
#model_manager = ModelManager()

# Command notation is: #IC[command] (arguments) 
# Kinda redundant 
INTERNAL_COMMANDS = ["login", "exit", "call"]

# Before establish the p2p, currently will store a sessionID for each pending call
call_sessions = []
# (ClientID, IPV4)
current_ipv4s_in_use = []

# -------- Functions --------



def handle_clients_login(conn, addr) -> Union[Account, None]:
    """
    Params:
        - conn [Socket] 
        - addr [_RetAddress]
    Returns:
        - populated clients_account instance [Account] - On SUCCESSFUL Authentication
        - None [None] - On FAILED Authentication
    Does:
    - Utilises AccountManager class to handle login authentication, clients_account locking and the rest
    - Only accepts 'IC[login] (username, password)' here.
    """
    while True:
        print(f"Waiting for login details at: {addr}")
        result = handle_recv(conn, addr)
        if result:
            cmd, args = result
            if (cmd == "login" and len(args) == 2) or (cmd == "register" and len(args) == 3):  
                if cmd == "login":
                    clients_account = AccountManager.handle_login(username=args[0], password=args[1])
                else:
                    clients_account = AccountManager.handle_register(email=args[0], username=args[1], password=args[2], ipv4=addr[0])
                if clients_account:                
                    handle_send(conn, addr, cmd=cmd, args=["SUCCESS"])
                    return clients_account
                else:
                    handle_send(conn, addr, cmd=cmd, args=["FAIL"])
            

            # elif cmd == "register" and len(args) == 3:
            #     clients_account = AccountManager.handle_register(email=args[0], username=args[1], password=args[2], ipv4=addr[0])
            #     if clients_account:
            #         handle_send(conn, addr, cmd="register", args=["SUCCESS"])
            #         return clients_account
            #     else:
            #         handle_send(conn, addr, cmd="register", args=["FAIL"])

            else:
                print(f"Something went wrong - received: {result}")
                return None
        else:
            return None


def handle_client(conn, addr):
    print(f"NEW CONNECTION: {conn}, {addr}")
    
    # Handle login here
    clients_account = handle_clients_login(conn, addr)
    if clients_account:
        print(f"(Account {clients_account}) sucessfully logged in at ({addr}) ")
        print(f"this clients ID is {clients_account.id}")
        clients_ipv4_location_details = (clients_account.id, addr) 
        current_ipv4s_in_use.append(clients_ipv4_location_details)
        
        while True:
            received = handle_recv(conn, addr)
            if received:
                cmd, args = received
                print(f"Recieved command: {cmd}, args: {args}")
                
                if cmd == "exit":
                    conn.close()
                    print(f"Closing connection with {addr}")
                    break

                elif cmd == "CallPerson":
                    # NOTE - Should determine session by looking at two peoples ID or groups ID
                    # args = [sessionID]
                    # SESSIONID SHOULD BE DENOTED USING THE 'pairing function' IN 'Ap_Tools.py'
                    requested_clients_ipv4 = False
                    for client_and_ipv4 in current_ipv4s_in_use:
                        if str(args[0]) == str(client_and_ipv4[0]):
                            requested_clients_ipv4 = client_and_ipv4[1]
              
                    handle_send(conn=conn, addr=addr, cmd=cmd, args=requested_clients_ipv4)    
                    
                    #establish_p2p_call()


                    # pairing_function(session_id)
                    # session_id = args[0]
                    # if session_id in call_sessions:
                    #     # Person is accepting call
                    #     call_sessions.remove(session_id)
                    # else:
                    #     # Person began calling someone 
                    #     call_sessions.append(session_id)


                
                elif cmd == "SendMsgToLiveChat":
                    pass
                
                elif cmd == "SendMessage":
                    result = MessageManager.handle_send_message(message=args[0], sender_id=clients_account.id, receiver_id=args[1])
                    print(result)
                    handle_send(conn=conn, addr=addr, cmd=cmd, args=result)
                    
                elif cmd == "SearchContact":
                    result = ContactsManger.handle_search_contact(username=args[0])
                    print(result)
                    if result:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=[
                            (clients_account[0], clients_account[1]) for clients_account in result # SEND ALL ACCOUNTS (ID1, USERNAME1, ID2, USERNAME2, ...)
                            ])
                
                    else:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=['FAIL'])

                elif cmd == "SaveContact":
                    add_contact_result = ContactsManger.handleAddContactRelationship(thisID=clients_account.id, otherID=args[0], paired_value=pairing_function(int(clients_account.id), int(args[0])))
                    if add_contact_result:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=True)
                    else:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=["'FAIL'"])
                        

                elif cmd == "GetSavedContactsChats": #GetContacts
                    results = ContactsManger.handle_get_all_chats_for_contact(clients_account.id)
                    if results:
                        accounts = [ContactsManger.handle_search_contact(id=x[2])[0] for x in results]
                        
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=accounts)
                    else:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=False)

                elif cmd == "GetMessagesHistory":
                    results = MessageManager.handle_get_chat_instance_messages(sender_id=clients_account.id, receiver_id=args[0])
                    print(results)
                    
                    handle_send(conn=conn, addr=addr, cmd=cmd, args=results)
                else:
                    print("Received unkwown cmd - Is this implemented yet?")
                    break
               
                if cmd == "acceptContact":
                    pass
                    

            else:
                print(f"Received unknown data? \n-Connection: {addr} \n-Data: {received}")
                break
    else:
        print(f"Client at {addr} Failure to login")
    
    # Post session clean-up
    current_ipv4s_in_use.remove(clients_ipv4_location_details)


def handle_incoming_connections():
    """ This function will handle any incoming requests. A thread will be instantiated and stored in 'thread_instances' (list) """
    thread_instances = []
    server.listen()
    print(f"Server is listening at: {ADDR}")
    while True:
        conn, addr = server.accept()
        if conn:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            # When client exits need to remove thread from list - (or do i? can i just join all at the end and remove them then)
            thread_instances.append(thread)
            thread.start()
            


def establish_p2p_call(session):
    """ Function establishes and handles UDP p2p connection between two clients for transmitting auditory data """
    



#  --------

DEBUG = False
if __name__ == "__main__":
    
    if DEBUG:
        extract_cmd("IC{login} (patrick,pass)")
    else:
        
        # Begin 
        # main thread will remain free.
        
        # Thread created for handling connection requests and setting a thread for each connection 
        handle_connections_thread = threading.Thread(target=handle_incoming_connections)
        handle_connections_thread.start()

        while True:
            try:

                # main thread does nothing yet. just idles, to keep server running till manual closure
                pass
            except KeyboardInterrupt as _:
                sys.exit()

else:
    print("This doesn't link to any external usage")

print(IP)
# conn, addr = sock.