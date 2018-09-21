import pyaudio
import wave
import sys

CHUNK = 1024
p = pyaudio.PyAudio()

def play_wav(filename: str):
    wf = wave.open(filename, 'rb')
    
    
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(CHUNK)
    
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    
    stream.stop_stream()
    stream.close()
 


if __name__ == '__main__':
    while(True):
        try:
            in_number = int(input('Input number: '))
        except:
            print("Is not number.")
            continue

        
    
    
    p.terminate()