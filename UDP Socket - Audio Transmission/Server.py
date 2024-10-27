import socket
import threading
from SoundHandling import play_recording_realtime
import globals


IP = "192.168.0.42"
PORT = 5005
ADDR = (IP, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

print(f"Listening at: {ADDR}")

output_thread = threading.Thread(target=play_recording_realtime)
output_thread.start()

# Ideally, there server will establish a p2p connection between two nodes. this will be where analog communications occur via UDP
# For the example, the server side will act as one of the clients. 

while True:
    data, addr = server.recvfrom(2081)
    print(f"[{addr}]: {data}")
   # print(f"[{addr}]: {data.decode('utf-8')}")
    
    globals.frames_buffer_out = data

    # if len(data >= 5):
    #     globals.frames_buffer_out[4] = data
    # else:
    #     globals.frames_buffer_out.append(data)
