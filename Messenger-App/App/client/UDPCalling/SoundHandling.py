import pyaudio as pya
import wave
#import numpy as np
import threading
import client.UDPCalling.UDPCalling_GlobalItems as UDPCalling_GlobalItems
import time
import socket


#import matplotlib.pyplot as plt 

FRAMES_PER_BUFFER = 2048
FORMAT = pya.paInt32
CHANNELS = 1
FRAMERATE = 44100
p = pya.PyAudio()

def get_recording(duration=5):
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER,
                    input=True)

    # Could do "while outputting=True" and have another thread which waits for the user to click end inputting - or something along those lines
    # FIXED DURATION
    print("Recording")
    frames = []
    for _ in range(0, int(FRAMERATE/FRAMES_PER_BUFFER * duration)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()    

    return (frames, stream, p)

def play_recorded(frames):
    stream = p.open(format=pya.paFloat32, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER, 
                    input=False, output=True)

    while frames:
      try:
        if frames:
          stream.write(frames[0])
          list(frames).remove(frames[0])
        else:
           break
      except IndexError as e:
        print(f"[play_recorded()]: Broke erroronously - {e}")
        break 


def save_recording_into_file(recording_data):
    """
      @param recording_data - [Tuple]
        (frames [list], stream [_Stream] pyaudio_instance [PyAudio])
      """    
    frames, _, _ = recording_data

    file_name = "test.wav"
    wf = wave.open(file_name, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(FRAMERATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def stop_recordings():
    global inputting
    
    while inputting:
      try:
        inputting = False
      except threading.BrokenBarrierError as e:
         print(f"[Threading Error]: {e}")


inputting = False
outputting = False
def start_recording_realtime(sender_socket=None):
    """ Runs in its own thread """
    global inputting
    
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER,
                    input=True, output=False)
  
    print("Microphone is being captured")
    inputting = True
    while inputting:
      sender_socket.sendall(stream.read(FRAMES_PER_BUFFER))
  
    print("Microphone capture has finished")



def play_recording_realtime(listener_socket=None):
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER, 
                    input=False, output=True)

    outputting = True
    while outputting:
        data, _ = listener_socket.recvfrom(FRAMES_PER_BUFFER*4)
        stream.write(data)

        #stream.write(UDPCalling_GlobalItems.frames_buffer_in.get())
          
      

if __name__ == "__main__":
    # test
    pass
    

    #save_recording_into_file(get_recording(5))