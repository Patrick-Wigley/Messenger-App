import socket
import threading

import os
import sys


from UDPCalling.SoundHandling import start_recording_realtime, stop_recordings


import client.UDPCalling.UDPCalling_GlobalItems as UDPCalling_GlobalItems
import random


connected = True


def setup_networking(addr=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return client
    #print(f"Setting up UDP SENDING: {addr}")
    #try:
        #client.bind(addr)
     #   print(f"Sending from: {addr}")
    #except socket.error as e:
     #   print(f"\nCouldnt set up UDP SENDING \nERROR IS '{e}'")
       


def client_handle(ip):
   
    addr = (ip, 5005) #random.randint(5056, 5076))
    client = setup_networking(addr)   
    send_to_addr = (ip, 5005)
    print(f"SENDING AUDIO UDP DATA TO {send_to_addr}")

    while connected:    
        if not UDPCalling_GlobalItems.frames_buffer_in.empty():
            data = UDPCalling_GlobalItems.frames_buffer_in.get()
            client.sendto(data, addr)
    
        if UDPCalling_GlobalItems.frames_buffer_in.full():
            print("INPUT BUFFER IS FULL")

    print(f"Ending connection with {SERVER_ADDR}")

def begin_send_audio_data(ip):
    recording_thread = threading.Thread(target=start_recording_realtime)
    print(ip)
    client_thread = threading.Thread(target=client_handle, args=([ip]))
    recording_thread.start()
    client_thread.start()


    if False:
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







if __name__ == "__main__":
    IP = input("Devices assigned IP on subnet ->:")
    # WOULD NOT IDEALLY USE RANDOM MODULE HERE - IF HAVE TIME, CHOOSE AN APPRORIATE PORT THAT DIFFERENCE FROM RECEIVING AND SENDING SOCKETS
    PORT = random.randint(6005, 7005)

    SERVER_ADDR = (IP, PORT)

    
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

