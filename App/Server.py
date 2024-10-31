# Needs a user login (AAA) Authentication, Authorisation & Auditing - Hash passwords - password resets & lockouts
# Needs Encryption of data sending
# Needs section to establish a p2p UDP socket between clients with keep-alive packets using pyaudio
# Needs to prevent replay attacks
#  


import socket
import threading
import sqlite3

DB_CONN_STR = "db\\MD_db"
db_conn = sqlite3.connect(DB_CONN_STR)
db_cursor = db_conn.cursor()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = input("Servers assigned IP on subnet ->: ") # socket.gethostbyname(socket.gethostname())
PORT = 5055
ADDR = (IP, PORT)

server.bind(ADDR)

# Command notation is: #IC{command} (arguments) 
# Kinda redundant 
INTERNAL_COMMANDS = ["exit", "call"]

# Before establish the p2p, currently will store a sessionID for each pending call
call_sessions = []

# -------- Functions --------
def handle_client(conn, addr):
    print(f"NEW CONNECTION: {conn}, {addr}")

    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if data: 
                # Determine if is command
                if "#IC" in data:
                    # "exit"
                    cmd = data[data.find("{")+1 : data.find("}")]  
                    args_str = data[data.find("(")+1 : data.find(")")] 
                    # [arg1, arg2, ...]
                    args = [arg.trim() for arg in args_str.split()]
                    if cmd == "exit":
                        conn.close()
                        print(f"Closing connection with {addr}")
                        break
                    if cmd == "call":
                        
                        # NOTE - Should determine session by looking at two peoples ID or groups ID
                        # args = [sessionID]
                        session_id = args[0]
                        if session_id in call_sessions:
                            # Person is accepting call
                            
                            call_sessions.remove(session_id)
                        else:
                            # Person began calling someone 
                            call_sessions.append(session_id)
                        establish_p2p_call(session_id)
                    

                # Else is casual data, currently just prints to cmdline
                print(data)

        except socket.error as e:
            print(e)



def handle_incoming_connections():
    """ This function will handle any incoming requests. A thread will be instantiated and stored in 'thread_instances' (list) """
    thread_instances = []
    server.listen()
    print(f"Server is listening at: {ADDR}")
    while True:
        conn, addr = server.accept()
        if conn:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread_instances.append(thread)
            thread.run()


def establish_p2p_call(session):
    """ Function establishes and handles UDP p2p connection between two clients for transmitting auditory data """
    



#  --------

if __name__ == "__main__":
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