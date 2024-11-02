# Needs a user login (AAA) Authentication, Authorisation & Auditing - Hash passwords - password resets & lockouts
# Needs Encryption of data sending
# Needs section to establish a p2p UDP socket between clients with keep-alive packets using pyaudio
# Needs to prevent replay attacks
#  

import socket
import threading
from typing import Union

from dbModelManager import ModelManager, AccountManager, Account


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())
PORT = 5055
ADDR = (IP, PORT)

server.bind(ADDR)

# NOTE: THIS NEEDS TO BE USED SYNCHRONOUSLY
model_manager = ModelManager()

# Command notation is: #IC[command] (arguments) 
# Kinda redundant 
INTERNAL_COMMANDS = ["login", "exit", "call"]

# Before establish the p2p, currently will store a sessionID for each pending call
call_sessions = []

# -------- Functions --------
def extract_cmd(data) -> tuple:
    """ #IC{command} (arg1, arg2, ...) """

    cmd = data[data.find("[")+1 : data.find("]")]  
    args_str = data[data.find("(")+1 : data.find(")")] 
    args = [arg.replace(" ", "") for arg in args_str.split(",")]
    return (cmd, args)

def handle_recv(conn, addr) -> str:
    """ Recieves data send from client - (will always be a cmd) then returns it after formatting """
    data = conn.recv(1024).decode("utf-8") 
    return extract_cmd(data)

def handle_clients_login(conn, _) -> Union[Account, None]:
    """ Handles a login session for a client
        - Utilises AccountManager class to handle login authentication, account locking and the rest
        - Only accepts 'IC[login] (username, password)' here.
        """
    
    while True:
        try:
            print("Looking for login details")
            data = conn.recv(1024).decode("utf-8")  
            cmd, args = extract_cmd(data)
          
            if cmd == "login" and len(args) == 2:  
                login_attempt = AccountManager.handle_login(username=args[0], password=args[1])
                if login_attempt:                
                    conn.send("S".encode("utf-8"))
                    return login_attempt
                else:
                    conn.send("F".encode("utf-8"))
            elif cmd == "register":
                pass
            
            else:
                print("Something went wrong")
                return None

        except socket.error as e:
            print(e)
            return None
            

def handle_client(conn, addr):
    print(f"NEW CONNECTION: {conn}, {addr}")

    # Handle login here
    account = handle_clients_login(conn, addr)
    if account:
        print(f"(Account {account}) sucessfully logged in at ({addr}) ")

        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if data:
                    # #IC{cmd}(arg1, arg2, ..)
                    if "#IC" in data:
                        cmd, args = extract_cmd(data)
                        print(f"Recieved command {cmd}")
                        
                        if cmd == "exit":
                            conn.close()
                            print(f"Closing connection with {addr}")
                            break

                        if cmd == "call":
                            # NOTE - Should determine session by looking at two peoples ID or groups ID
                            # args = [sessionID]
                            # SESSIONID SHOULD BE DENOTED USING THE 'pairing function' IN 'Ap_Tools.py'
                            session_id = args[0]
                            if session_id in call_sessions:
                                # Person is accepting call
                                call_sessions.remove(session_id)
                            else:
                                # Person began calling someone 
                                call_sessions.append(session_id)
                            establish_p2p_call(session_id)

                        if cmd == "newcontact":
                            # args (other username, _)
                            # Find other person, store friendship in db
                            users = (account.username, args[0])


                    # Else is casual data, currently just prints to cmdline
                    print(f"[{account}]: {data}")

            except socket.error as e:
                print(e)
                break

    else:
        print("Twat this connection off, they're malicious as a mf ")


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
            # main thread does nothing yet. just idles, to keep server running till manual closure
            pass

else:
    print("This doesn't link to any external usage")

print(IP)
# conn, addr = sock.