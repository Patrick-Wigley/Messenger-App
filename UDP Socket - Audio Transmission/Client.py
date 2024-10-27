import socket
import threading
from SoundHandling import start_recording_realtime, stop_recordings
import globals
import sys

IP = "192.168.0.42"
PORT = 5005

SERVER_ADDR = ("192.168.0.42", 5005)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connected = True

def client_handle():
    print(f"Sending data audio to: {SERVER_ADDR}")
    while connected:    
        if globals.frames_buffer_in:  
            client.sendto(globals.frames_buffer_in, SERVER_ADDR)
            # Used to determine size of bytes being sent:
            # size = sys.getsizeof(globals.frames_buffer)
            # client.sendto(str(size).encode("utf-8"), SERVER_ADDR)

            #print(frames_buffer[len(frames_buffer)-1])
    print(f"Ending connection with {SERVER_ADDR}")

if __name__ == "__main__":
    # Thread is for taking recording.
    recording_thread = threading.Thread(target=start_recording_realtime)
    client_thread = threading.Thread(target=client_handle)
    recording_thread.start()
    client_thread.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("Ending")
            # Cleanup
            stop_recordings()
            # Ending client_thread dirtly
            connected = False
            break

