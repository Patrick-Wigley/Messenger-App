# Needs a user login (AAA) Authentication, Authorisation & Auditing - Hash passwords - password resets & lockouts
# Needs Encryption of data sending
# Needs section to establish a p2p UDP socket between clients with keep-alive packets using pyaudio
# Needs to prevent replay attacks
#  

import socket
import threading
import smtplib
import sys
import os
from typing import Union


from dbModelManager import AccountManager, AccountManagerErrors, Account, ContactsManger, MessageManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Shared.SharedTools import (CMD,
                            extract_cmd, 
                            send_email,
                            pairing_function,
                            handle_recv,
                            handle_send,
                            gen_keys, handle_pubkey_share)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with open("Server\\details", "r") as file:
    data = file.read()
    if data:
        IP = data
    else:
        input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())
        
PORT = 5055
ADDR = (IP, PORT)
server.bind(ADDR)


# NOTE: THIS NEEDS TO BE USED SYNCHRONOUSLY

# Command notation is: #IC[command] (arguments) 


# (ClientID, IPV4)
current_ipv4s_in_use = []
current_conns_in_use = []
# -------- Functions --------

def handle_client_login(conn, addr, pub_priv_keys, cmd, args) -> Union[Account, None]:
    clients_account = AccountManager.handle_login(username=args[0], password=args[1])          
    if clients_account:
        if not clients_account.locked:
            if False: #NOTE ADD BACK: 
                if AccountManager.is_new_login_location(ipv4=addr[0], username=args[0]):    
                    send_email(receiver_email=clients_account.email, 
                            data=f"Hi {args[0]}, you have logged in at a different location, check that this is you?", 
                            subject="New Login Location")
            handle_send(conn, addr, cmd=cmd, args=True, pub_key=pub_priv_keys[0])
            return clients_account
        else:
            if False: #NOTE ADD BACK: 
                send_email(receiver_email=clients_account.email, 
                            data=f"Hi {args[0]}, we have locked your account - There has been multiple failed login attempts into your account.", 
                            subject="Are you trying to access your account?")
    return None

def handle_client_register(conn, addr, pub_priv_keys, cmd, args) -> Union[Account, None]:
    print(args)
    clients_account = AccountManager.handle_register(email=args[2], username=args[0], password=args[1], ipv4=addr[0], premium_member=args[3])
    if clients_account:
        if False: #NOTE ADD BACK
            send_email(receiver_email=clients_account.email, 
                    data=f"Welcome {args[1]} to the UOD Messenger app! Hosted at {IP}:{PORT} We have saved your account to this email. This social application is still in production!",
                    subject="The UOD Messenger App")
        
        handle_send(conn, addr, cmd=cmd, args=True, pub_key=pub_priv_keys[0])
        return clients_account
    return None

def handle_client_forgot_password(conn, addr, pub_priv_keys, cmd, args) -> None:
    """NOT FINISHED"""
    # NOT IMPLEMENTED YET
    if cmd == "ForgottenLogin":
        if AccountManager.handle_passwordreset(username=args[0]):
            handle_send(conn, addr, cmd=cmd, args=True, pub_key=pub_priv_keys[0])
            
        else:
            handle_send(conn, addr, cmd=cmd, args=False, pub_key=pub_priv_keys[0])
    ################



def handle_client_auth(conn, addr, pub_priv_keys) -> Union[Account, None]:
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
        result = handle_recv(conn, addr, priv_key=pub_priv_keys[1])
        if result != None:
            cmd, args = result
            print(result)
            if cmd == CMD.LOGIN:
                result = handle_client_login(conn, addr, pub_priv_keys, cmd, args)
                if result:
                    return result
            elif cmd == CMD.REGISTER:
                result = handle_client_register(conn, addr, pub_priv_keys, cmd, args)
                if result:
                    return result
            else:
                print(f"Received Something Unexpected in {handle_client_auth.__name__}: {result}")
                return None
        
            handle_send(conn, addr, cmd=cmd, args=False, pub_key=pub_priv_keys[0])

            if False:
               handle_client_forgot_password(conn, addr, pub_priv_keys, cmd, args)
        else:
            break
    
    return None
        
def handle_initial_communication():
    """ Setup with a client """
    pass

# Turn this into a loop function
def handle_client(conn, addr):
    print(f"NEW CONNECTION: {conn}, {addr}")
    clients_ipv4_location_details = None
    clients_conn_pubkey_details = None

    # Sessions Key Generation 
    # Generate Server Private & Public keys for this client session
    pub_key, priv_key = gen_keys() 
    #
    clients_pub_key = handle_pubkey_share(conn, addr, pub_key, verbose=True)
    
    # Handle login here
    clients_account = handle_client_auth(conn, addr, (clients_pub_key, priv_key))

    if clients_account:
        print(f"User {clients_account} sucessfully logged in at {addr} ")
        clients_ipv4_location_details = (clients_account.id, addr)
        clients_conn_pubkey_details = (clients_account.id, clients_account.username, conn, clients_pub_key)
        
        current_ipv4s_in_use.append(clients_ipv4_location_details)
        current_conns_in_use.append(clients_conn_pubkey_details)

        while True:
            received = handle_recv(conn, addr, priv_key=priv_key, verbose=False)
            if received:
                cmd, args = received
                print(f"Recieved command: {cmd}, args: {args}")
                
                if cmd == CMD.EXIT:
                    conn.close()
                    print(f"Closing connection with {addr}")
                    break

                elif cmd == CMD.CALLPERSON:
                    # NOTE - Should determine session by looking at two peoples ID or groups ID
                    # args = [sessionID]
                    # SESSIONID SHOULD BE DENOTED USING THE 'pairing function' IN 'Ap_Tools.py'
                    requested_clients_ipv4 = False
                    for client_and_ipv4 in current_ipv4s_in_use:
                        if str(args[0]) == str(client_and_ipv4[0]):
                            requested_clients_ipv4 = client_and_ipv4[1]
                    handle_send(conn=conn, addr=addr, cmd=cmd, args=requested_clients_ipv4, pub_key=clients_pub_key)    
                
                
                elif cmd == CMD.SENDMESSAGE:
                    sender_id=clients_account.id
                    receiver_id = args[1]
                    
                    message_prefixed = f"[{clients_account.username}] {args[0]}"
                    result = MessageManager.handle_send_message(message=message_prefixed, sender_id=sender_id, receiver_id=receiver_id)
                    handle_send(conn=conn, addr=addr, cmd=cmd, args=result, pub_key=clients_pub_key)
                    # IF RECEIVER IS ONLINE, UPDATE IN REAL-TIME FOR THEM
                    for id, _, connection, key in current_conns_in_use:
                        if str(receiver_id) == str(id):
                            print("Person is online")
                            # Refresh chat-log for person being sent message (AS THEY'RE ONLINE)
                            handle_send(conn=connection, cmd=CMD.UPDATE_CHAT_LOG_LIVE, args=sender_id, pub_key=key)
                            
                elif cmd == CMD.SEARCHCONTACT:
                    result = ContactsManger.handle_search_contact(username=args[0])
                    if result:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=[
                            (clients_account[0], clients_account[1]) for clients_account in result # SEND ALL ACCOUNTS (ID1, USERNAME1, ID2, USERNAME2, ...)
                            ], 
                            pub_key=clients_pub_key)
                    else:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=False, pub_key=clients_pub_key)

                elif cmd == CMD.SAVECONTACT:
                    add_contact_result = ContactsManger.handle_add_contact_relationship(thisID=clients_account.id, otherID=args[0], paired_value=pairing_function(int(clients_account.id), int(args[0])))
                    if add_contact_result:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=True, pub_key=clients_pub_key)
                    else:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=False, pub_key=clients_pub_key)
                        
                elif cmd == CMD.GETSAVECONTACTCHATS: 
                    results = ContactsManger.handle_get_all_chats_for_contact(clients_account.id)
                    if results:
                        accounts = [ContactsManger.handle_search_contact(id=x[2])[0] for x in results]

                        handle_send(conn=conn, addr=addr, cmd=cmd, args=accounts, pub_key=clients_pub_key)
                    else:
                        handle_send(conn=conn, addr=addr, cmd=cmd, args=False, pub_key=clients_pub_key)

                elif cmd == CMD.GETMESSAGEHISTORY:
                    results = MessageManager.handle_get_chat_instance_messages(sender_id=clients_account.id, receiver_id=args[0])
                    handle_send(conn=conn, addr=addr, cmd=cmd, args=results, pub_key=clients_pub_key)
                
                elif cmd == CMD.BROADCAST:
                    if clients_account.is_premium_member:
                        print("Account is allowed to use this feature")
                        for _, _, connection, key in current_conns_in_use:
                            handle_send(conn=connection, cmd=cmd, args=f"'PREMIUM MEMBER {clients_account.username} says:     {args[0]}'", pub_key=key)
                    else:
                        print("Account is NOT allowed to use this feature")
                        handle_send(conn=conn, cmd=CMD.BROADCAST_NOT_ALLOWED, pub_key=clients_pub_key)

                elif cmd == CMD.STILL_CONNECTED:
                    print("Connect is still alive")
                else:
                    print(f"Received: {received}")
                    

            else:
                print(f"Received unexpected: \n- At Connection: {addr} \n- Data: {received}")
                if not handle_check_connection_still_active(conn, priv_key):
                        print("Connection not sending")
                        break
                break

        # Post session clean-up
        print(f"User '{clients_account.username}' at '{addr[0]}:{addr[1]}' is disconnecting")
        current_ipv4s_in_use.remove(clients_ipv4_location_details)
        current_conns_in_use.remove(clients_conn_pubkey_details)
    else:
        print(f"Client at {addr} Failure to login")
    
def handle_check_connection_still_active(conn, key) -> bool:
    if handle_send(conn, cmd=CMD.STILL_CONNECTED, pub_key=key):
        return True
    else:
        return False


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