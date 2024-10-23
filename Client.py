import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (IP, PORT)
SERVER_LOCATION = ("192.168.0.42", 5050)


message_buffer = []
# If this is empty, should then handle message_buffer requets
priority_buffer = []

def server_handle():
    """ All server connection, communications will be handled here """
    print(f"Attempting to connect to: {SERVER_LOCATION}")
    client.connect(SERVER_LOCATION)

    client.send("test".encode("utf-8"))


def establish_p2p_private_connection():
    """ From client need to request to p2p connect to a client. Server should pair other person if they wish to communicate 

       """


# Begin 
if __name__ == "__main__":
    # Probably run some tests? 
    pass

   

else:
    # -- Runs through GUI.py

    # main thread will remain free.
    
    # Thread created for handling connection requests and setting a thread for each connection 
    handle_connections_thread = threading.Thread(target=server_handle)
    # Daemon threads ensures they finish when the program is exited 
    handle_connections_thread.setDaemon(True)
    handle_connections_thread.start()

    
   