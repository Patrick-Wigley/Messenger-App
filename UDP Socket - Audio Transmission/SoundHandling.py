import pyaudio as pya
import wave
import numpy as np
import threading
import GlobalItems
import time
import socket


#import matplotlib.pyplot as plt 

FRAMES_PER_BUFFER = 1024
FORMAT = pya.paInt16
CHANNELS = 2
FRAMERATE = 44100
p = pya.PyAudio()

def get_recording(duration=5):
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER,
                    input=True)

    # Could do "while playing=True" and have another thread which waits for the user to click end recording - or something along those lines
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


recording = False
def start_recording_realtime():
    """ Runs in its own thread """
    global recording
    
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER,
                    input=True)
  
    print("Microphone is being captured")
    recording = True
    while recording:
      GlobalItems.frames_buffer_in.put(stream.read(FRAMES_PER_BUFFER))

    print("Microphone capture has finished")

def stop_recordings():
    global recording
    
    while recording:
      try:
        recording = False
      except threading.BrokenBarrierError as e:
         print(f"[Threading Error]: {e}")


def play_recording_realtime():
    stream = p.open(format=pya.paFloat32, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER, 
                    input=False, output=True)

    playing = True
    while playing:
        if not GlobalItems.frames_buffer_in.empty():
          stream.write(GlobalItems.frames_buffer_in.get())
          time.sleep(1)


def recv_and_play_recording_realtime():
    """ This function combines 'play_recording_realtime' & networking side of analog comm """
    stream = p.open(format=pya.paFloat32, channels=CHANNELS, rate=FRAMERATE, frames_per_buffer=FRAMES_PER_BUFFER, 
                    input=False, output=True)
    
    IP = "192.168.0.42"
    PORT = 5005
    ADDR = (IP, PORT)


    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)

    print(f"[UDP SERVER] Listening at: {ADDR}")
    
    playing = True
    while playing:
      stream.write(server.recvfrom(2081))
      

if __name__ == "__main__":
    # test
    pass
    

    #save_recording_into_file(get_recording(5))