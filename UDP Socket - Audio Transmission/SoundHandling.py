import pyaudio as pya
import wave
import numpy as np
import threading
import globals

#import matplotlib.pyplot as plt 

FRAMES_PER_BUFFER = 1024
FORMAT = pya.paInt16
CHANNELS = 1
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
      globals.frames_buffer_in = stream.read(FRAMES_PER_BUFFER)
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
       if globals.frames_buffer_out:
        stream.write(globals.frames_buffer_out)


if __name__ == "__main__":
    save_recording_into_file(get_recording(5))