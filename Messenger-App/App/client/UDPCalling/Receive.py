import socket
import threading
from UDPCalling.SoundHandling import play_recording_realtime
import client.UDPCalling.UDPCalling_GlobalItems as UDPCalling_GlobalItems
import random

def setup_pyaudio_thread():
   output_thread = threading.Thread(target=play_recording_realtime)
   output_thread.start()

def setup_networking(addr=None):
   server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   print(f"Setting up UDP RECEIVING: {addr}")
   try:
      server.bind(addr)
      print(f"Receiving at: {addr}")
   except socket.error as e:
      print(f"Couldnt set up UDP RECEIVIBG \nERROR IS '{e}'")
       
   return server


def begin_recv_audio_data(ip):
   addr = (ip, 5006) #random.randint(5077, 5099))
   server = setup_networking(addr)
   setup_pyaudio_thread()

   while True:
      data, addr = server.recvfrom(65536) #4129 #2081
      UDPCalling_GlobalItems.frames_buffer_out.put(data)














# Ideally, there server will establish a p2p connection between two nodes. this will be where analog communications occur via UDP
# For this example, the server side will act as one of the clients. 

if __name__ == "__main__":
   IP = input("Servers assigned IP on subnet ->: ")
   PORT = random.randint(7006, 8006)
   ADDR = (IP, PORT)

   server = setup_networking(ADDR)
   setup_pyaudio_thread()

   while True:
      # NOTE - Use one thread for receiving data and outputting it (garentees just output what is received straight away)
      data, addr = server.recvfrom(65536) #4129 #2081

      UDPCalling_GlobalItems.frames_buffer_out.put(data)
      

      #print(f"[{addr}]: {data}")

      #print(f"[{addr}]: {data.decode('utf-8')}")
      
      #NOTE NEED THIS IF REVERTING TO SEPERATION VERSION

      # if len(GlobalItems.frames_buffer_out) >= 5:
      #    GlobalItems.frames_buffer_out[4] = data
      # else:
      #    GlobalItems.frames_buffer_out.append(data)


else:
   print("Hello from UDP-AUDIO RECEIVING!")
   #recv_audio_data()