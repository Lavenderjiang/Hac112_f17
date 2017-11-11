#audio lecture
#audio segment demo

from pydub import AudioSegment
from pyaudiodemo import play
import threading

def soundFromFile(file):
    return AudioSegment.from_wav(file)

def getSection(file, start, end):
    sound = soundFromFile(file)
    newSound = sound[start:end]
    return exportToFile(newSound, "slice.wav")
