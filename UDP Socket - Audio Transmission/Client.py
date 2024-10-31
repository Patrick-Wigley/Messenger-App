import socket
import threading
from SoundHandling import start_recording_realtime, stop_recordings
import GlobalItems
import sys

IP = input("Devices assigned IP on subnet ->:")
PORT = 5005

SERVER_ADDR = (IP, 5005)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connected = True

def client_handle():
    print(f"Sending data audio to: {SERVER_ADDR}")
    while connected:    
        if not GlobalItems.frames_buffer_in.empty():
            data = GlobalItems.frames_buffer_in.get()
            client.sendto(data, SERVER_ADDR)
            
        else:
            pass
            # print("Frame buffer is empty")
            # Used to determine size of bytes being sent:
            # size = sys.getsizeof(GlobalItems.frames_buffer)
            # client.sendto(str(size).encode("utf-8"), SERVER_ADDR)
            #print(frames_buffer[len(frames_buffer)-1])

        if GlobalItems.frames_buffer_in.full():
            print("INPUT BUFFER IS FULL")


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

