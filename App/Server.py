import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = "192.168.0.42" # socket.gethostbyname(socket.gethostname())
PORT = 5055
ADDR = (IP, PORT)

server.bind(ADDR)

# Command notation is: #IC{command}
# Kinda redundant 
INTERNAL_COMMANDS = ["exit"]


# -------- Functions --------

def handle_client(conn, addr):
    print(f"NEW CONNECTION: {conn}, {addr}")

    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if data: 
                # Determine if is command
                if "#IC" in data:
                    cmd = data[data.find("{")+1 : data.find("}")]                    
                    if cmd == "exit":
                        conn.close()
                        print(f"Closing connection with {addr}")
                        break

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