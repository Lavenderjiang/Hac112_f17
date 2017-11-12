import aubio
from workingaubio import *
from pydub import AudioSegment
from audio_segment_demo import *


def detect(filename):
        downsample = 8
        samplerate = 44100 // downsample
        win_s = 4096 // downsample # fft size
        hop_s = 512  // downsample # hop size
        s = aubio.source(filename, samplerate, hop_s)
        samplerate = s.samplerate
        tolerance = 0.8
        pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
        pitch_o.set_unit("freq")
        pitch_o.set_tolerance(tolerance)
        pitches = []
        confidences = []
        # total number of frames read
        total_frames = 0
        counter = 0
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()
            #print "%f %f %f" % (total_frames / float(samplerate), pitch, confidence)
            pitches += [pitch]
            confidences += [confidence]
            total_frames += read
            if read < hop_s: break
        letterList = []
        newPitches = []
        amplitudes = []
        for index in range(0, len(pitches)):
            totalFreq = 0
            if(index+5 <= len(pitches)):
                for freq in range(index, index+5):
                    totalFreq += pitches[freq]
                averageFreq = totalFreq/5
                newPitches.append(averageFreq)
            else:
                counter = 0
                for index in range(index, len(pitches)):
                    totalFreq += pitches[freq]
                    counter += 1
                averageFreq = totalFreq/counter
                newPitches.append(averageFreq)
            # loudness
            amp = getSection(filename,index, index + 5)
            amplitudes.append(amp.rms)
        for pi in newPitches:
            letterName = findPitchLetterName(pi)
            letterList.append(pi) # letterName -> pi for frequency numbers
        newList = modifyList(letterList)
        note = findModeInList(newList)
        #print(letterList, amplitudes)
        return letterList, amplitudes
        
def getPitchAndAmp(filename):
    f = detect(filename)
    # list of pitches
    freq = f[0]
    # list of amplitudes
    amp = f[1]
    List = []
    for i in range(len(freq)):
        List.append((freq[i], amp[i]))
    print(List)
    # list of tuples of pitch and amplitudes
    return List
    
    
def main():
    return getPitchAndAmp("connor.wav")
    
if __name__ == '__main__':
    main()
