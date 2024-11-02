import socket
import threading
import sys

import GlobalItems
import Ap_Tools

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = input("Devices assigned IP on subnet ->: ") #socket.gethostbyname(socket.gethostname())
PORT = 5055
ADDR = (IP, PORT)
SERVER_LOCATION = (input("Servers assigned IP on subnet ->:"), 5055)

kill_all_non_daemon = False


# If this is empty, should then handle GlobalItems.send_server_msg_buffer requets
priority_buffer = []


def login_handle() -> bool:
    """ Ran before main socket sending occurs, handles login """
    while not GlobalItems.logged_in:
        login_details = None if len(GlobalItems.send_server_msg_buffer) == 0 else GlobalItems.send_server_msg_buffer.pop()
        if login_details:
            # Currently, login is GlobalItems.send_server_msg_buffer.append(input("username & password syntax = (username,password)->:"))
            #login_cmd_formatted = f"IC[login] ({login_details})"
            # Should be "#IC{login} (username, password)"
            #print(f"login cmd formatted: {login_cmd_formatted}")
            client.send(login_details.encode("utf-8"))

            try:
                result = client.recv(1024).decode("utf-8")
                print(f"[server]: {result}")
                if result == "S":
                    # Successfully logged into account
                    # stores login for when logging in again
                    with open("cache.txt", "w") as cached_login:
                        # NOTE: FINISH USING JSON
                        cached_login.write(f"{login_details}")
                        cached_login.close()
                    GlobalItems.logged_in = True
                    
                    # Let window know
                    GlobalItems.interpreted_server_feedback_buffer.append("#IC[login](_, True)")

                elif result == "F":
                    GlobalItems.interpreted_server_feedback_buffer.append("#IC[login](Username_or_Password_is_incorrect, False)")

            except socket.error as e:
                print(e)
                sys.exit()
                
            


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
        # Current setup is stack - (in final product this should ideally be queued)
        outgoing = None if len(GlobalItems.send_server_msg_buffer) == 0 else GlobalItems.send_server_msg_buffer.pop()             #input("->: ")
        if outgoing:
            if "exit" in outgoing:
                print(f"Exiting thread: {threading.get_ident()}!")
                # Need to tell server
                client.send(r"#IC[exit]".encode("utf-8"))
                break
            if outgoing == "call":
                # Needs arg of person sending to & this persons id
                session_id = Ap_Tools.pairing_function(_, _)

            # Should be "if outgoing contains 'message' - (This should become a command with args as the person send to and the message being sent) "
            # #IC[msg] (Goku, 'hello, how are we Kakarot')
            elif outgoing:
                client.send(outgoing.encode("utf-8"))

            # currently not in use but may need if becomes non-daemon for any reason/test
            if kill_all_non_daemon:
                print("Ending Thread")
                break
            ##




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
   