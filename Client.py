import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = "192.168.0.42" #socket.gethostbyname(socket.gethostname())
PORT = 5055
ADDR = (IP, PORT)
SERVER_LOCATION = ("192.168.0.42", 5055)

kill_all_non_daemon = False

message_buffer = []
# If this is empty, should then handle message_buffer requets
priority_buffer = []

def server_handle():
    """ All server connection, communications will be handled here 
        This is ran in its own thread - while it is daemon, it needs to be READ-ONLY. Cannot ask for inputs, no interupts and etc. """

    global kill_all_non_daemon
    
    print(f"Attempting to connect to: {SERVER_LOCATION}")
    client.connect(SERVER_LOCATION)
    print("Connected")

    while True:
        # Current setup is stack - (in final product this should ideally be queued)
        outgoing = None if len(message_buffer) == 0 else message_buffer.pop()             #input("->: ")
        if outgoing == "exit":
            print(f"Exiting thread: {threading.get_ident()}!")
            # Need to tell server
            client.send(r"#IC{exit}".encode("utf-8"))
            break

        # currently not in use but may need if becomes non-daemon for any reason/test
        if kill_all_non_daemon:
            print("Ending Thread")
            break
        ##

        if outgoing:
            client.send(outgoing.encode("utf-8"))



def establish_p2p_private_connection():
    """ From client need to request to p2p connect to a client. Server should pair other person if they wish to communicate 

       """


# Begin 
if __name__ == "__main__":
    # Probably run some tests? 
    print("This only doesn't run directly yet")
    

   

else:
    # -- Runs through GUI.py

    # main thread will remain free.
   # server_handle()

    # Thread created for handling connection requests and setting a thread for each connection 
    handle_connections_thread = threading.Thread(target=server_handle)
    # Daemon threads ensures they finish when the program is exited - ALTHOUGH, cannot handle communication with current setup? maybe its because I am asking for an input? rather than keeping the thread read-only to send data 

    handle_connections_thread.setDaemon(True)
    handle_connections_thread.start()

    
   