import aubio
from pydub import AudioSegment
from audio_segment_demo import *
import beat

def findPitchLetterName(frequency):
    if(frequency < 82 or frequency > 1000): return "silence"
    pitchDictionary = {"E2": 82.41, "F2": 87.31, "Gb2" : 92.50, "G2": 98.00,
        "Ab2": 103.83, "A2": 110.00, "Bb2": 116.54, "B2": 123.47, "C3": 130.81, 
        "Db3": 138.59, "D3": 146.83, "Eb3": 155.56, "E3": 164.81, "F3": 174.61, 
        "Gb3": 185.00, "G3": 196.00, "Ab3": 207.65, "A3": 220.00, "Bb3": 233.08, 
        "B3": 246.94, "C4": 261.63, "Db4": 277.18, "D4": 293.66, "Eb4": 311.13, 
        "E4": 329.63, "F4": 349.23, "Gb4": 369.99, "G4": 392.00, "Ab4": 415.30,
        "A4": 440.00, "Bb4": 466.16, "B4": 493.88, "C5": 523.25, "Db5": 554.37,
        "D5": 587.33, "Eb5": 622.25, "E5": 659.25, "F5": 698.46, "Gb5": 739.99,
        "G5": 783.99, "Ab5": 830.61, "A5": 880.00, "Bb5": 932.33, "B5": 987.77, 
        "C6": 1046.50 }
    for key in pitchDictionary:
        threshold = 10
        if(pitchDictionary[key] - threshold <= frequency 
            <= pitchDictionary[key] + threshold):
            return key
    return guess(frequency)


#improved pitch detection that is WAY better than my previous versions of the class :)
def guess(frequency):
    maxDif = 10000000
    note = None
    pitchDictionary = {"E2": 82.41, "F2": 87.31, "Gb2" : 92.50, "G2": 98.00,
        "Ab2": 103.83, "A2": 110.00, "Bb2": 116.54, "B2": 123.47, "C3": 130.81, 
        "Db3": 138.59, "D3": 146.83, "Eb3": 155.56, "E3": 164.81, "F3": 174.61, 
        "Gb3": 185.00, "G3": 196.00, "Ab3": 207.65, "A3": 220.00, "Bb3": 233.08, 
        "B3": 246.94, "C4": 261.63, "Db4": 277.18, "D4": 293.66, "Eb4": 311.13, 
        "E4": 329.63, "F4": 349.23, "Gb4": 369.99, "G4": 392.00, "Ab4": 415.30,
        "A4": 440.00, "Bb4": 466.16, "B4": 493.88, "C5": 523.25, "Db5": 554.37,
        "D5": 587.33, "Eb5": 622.25, "E5": 659.25, "F5": 698.46, "Gb5": 739.99,
        "G5": 783.99, "Ab5": 830.61, "A5": 880.00, "Bb5": 932.33, "B5": 987.77, 
        "C6": 1046.50 }
    for key in pitchDictionary:
        dif = abs(pitchDictionary[key] - frequency)
        if(dif < maxDif):
            maxDif = dif
            note = key
    return note

def modifyList(letterList):
    newLetterList = []
    for thing in letterList:
        if(thing != None):
            newLetterList.append(thing)
    return newLetterList

def findModeInList(letterList):
    currentNote = None
    maxCount = 10
    notes = []
    counter = 1
    for index in range(1, len(letterList)):
        if(index == len(letterList)-1 and counter >= maxCount):
            notes.append(letterList[index-1])
        elif(letterList[index-1] == letterList[index]):
            counter += 1
        else:
            if(counter >= maxCount):
                notes.append(letterList[index-1])
            counter = 1
    return notes

#modified from: https://git.aubio.org/?p=aubio.git;a=blob;f=python/demos/demo_pitch.py;h=81f17cd4b3eed408abb31adbccd1ba39296dbacd;hb=c3c6305987848593034cb34501a9d3bc7afd6e8c
# def detect(filename):
#         downsample = 8
#         samplerate = 44100 // downsample
#         win_s = 4096 // downsample # fft size
#         hop_s = 512  // downsample # hop size
#         s = aubio.source(filename, samplerate, hop_s)
#         samplerate = s.samplerate
#         tolerance = 0.8
#         pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
#         pitch_o.set_unit("freq")
#         pitch_o.set_tolerance(tolerance)
#         pitches = []
#         confidences = []
#         # total number of frames read
#         total_frames = 0
#         counter = 0
#         while True:
#             samples, read = s()
#             pitch = pitch_o(samples)[0]
#             confidence = pitch_o.get_confidence()
#             #print "%f %f %f" % (total_frames / float(samplerate), pitch, confidence)
#             pitches += [pitch]
#             confidences += [confidence]
#             total_frames += read
#             if read < hop_s: break
#         letterList = []
#         newPitches = []
#         amplitudes = []
#         for index in range(0, len(pitches)):
#             totalFreq = 0
#             if(index+5 <= len(pitches)):
#                 for freq in range(index, index+5):
#                     totalFreq += pitches[freq]
#                 averageFreq = totalFreq/5
#                 newPitches.append(averageFreq)
#             else:
#                 counter = 0
#                 for index in range(index, len(pitches)):
#                     totalFreq += pitches[freq]
#                     counter += 1
#                 averageFreq = totalFreq/counter
#                 newPitches.append(averageFreq)
#             # loudness
#             amp = getSection(filename,index, index + 5)
#             amplitudes.append(amp.rms)
#         for pi in newPitches:
#             #letterName = findPitchLetterName(pi)
#             letterList.append(pi) # letterName -> pi for frequency numbers
#         #newList = modifyList(letterList)
#         #note = findModeInList(newList)
#         return letterList, amplitudes


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
        for index in range(0, len(pitches)): #, len(pitches)//20):
            totalFreq = 0
            if(index+5 <= len(pitches)):
                for freq in range(index, index+5):
                    totalFreq += pitches[freq]
                averageFreq = totalFreq/5
                newPitches.append(averageFreq)
                # amp = getSection(filename, index, index + 5)
                # amplitudes.append(amp.rms)
            else:
                counter = 0
                for index in range(index, len(pitches)):
                    totalFreq += pitches[freq]
                    counter += 1
                averageFreq = totalFreq/counter
                newPitches.append(averageFreq)
                # amp = getSection(filename, index, index + len(pitches))
                # amplitudes.append(amp.rms)
        for pi in newPitches:
            letterName = findPitchLetterName(pi)
            letterList.append(pi)
        newList = modifyList(letterList)
        note = findModeInList(newList)
        return letterList

def getAmp(filename):
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
            amp = getSection(filename, index, )#, index + 5)
            amplitudes.append(amp.rms)
        return amplitudes

def detectKey(filename):
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
        for index in range(0, len(pitches), len(pitches)//20):
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
        for pi in newPitches:
            letterName = findPitchLetterName(pi)
            letterList.append(letterName)
        newList = modifyList(letterList)
        note = findModeInList(newList)
        # letterList is a list of all notes
        # need most common and second most common
        return mode(letterList)

def soundFromFile(file):
    return AudioSegment.from_wav(file)

def duration(filename):
    song = AudioSegment.from_wav(filename)
    return song.duration_seconds

def mode(letterList):
    notes = {}
    for i in letterList:
        i = i[:-1]
        if i in notes and i != "silenc":
            notes[i] += 1
        elif i not in notes and i != "silenc":
            notes[i] = 1
    
    maxNum = -1
    for note in notes:
        if notes[note] > maxNum:
            maxNote = note
            maxNum = notes[note]
    tonic = maxNote
    
    oldMaxNum = maxNum
    maxNum = -1
    for note in notes:
        if notes[note] > maxNum and notes[note] < oldMaxNum:
            maxNote = note
            maxNum = notes[note]
    dominant = maxNote
    
    noteVal = {"C": 1, "Db": 2, "D": 3, "Eb": 4, "E": 5, "F": 6, "Gb": 7, "G":8, "Ab":9, "A":10, "Bb":11, "B":12}
    
    dif = (noteVal[dominant] - noteVal[tonic]) % 12
    
    return (dif, tonic, dominant)

def buildChords(note, chordType, inversion):
    if(note != []):
        note = note[0]
        noteOrder = ["E2","F2", "Gb2", "G2",
            "Ab2", "A2", "Bb2", "B2", "C3", 
             "Db3", "D3", "Eb3", "E3", "F3", 
            "Gb3", "G3", "Ab3","A3", "Bb3", 
            "B3", "C4",  "Db4",  "D4", "Eb4",
            "E4", "F4", "Gb4", "G4", "Ab4",
            "A4", "Bb4", "B4", "C5", "Db5",
            "D5", "Eb5", "E5", "F5", "Gb5",
            "G5","Ab5", "A5", "Bb5", "B5",
            "C6", "Db6", "D6", "Eb6", "E6", 
            "F6", "Gb5", "G5"]
        indexOfRoot = noteOrder.index(note)
        root = noteOrder[indexOfRoot]
        if(chordType == "Major"):
            majorThird = 4
            m3 = noteOrder[indexOfRoot + majorThird]
            third = m3
        elif(chordType == "Minor"):
            minorThird = 3
            m3 = noteOrder[indexOfRoot + minorThird]
            third = m3
        perfectFifth = 7
        p5 = noteOrder[indexOfRoot + perfectFifth]
        octave = 12
        fifth = p5
        if(inversion == 1):
            root = m3
            third = p5
            fifth = noteOrder[indexOfRoot + octave]
        if(inversion == 2):
            indexOfFifth = noteOrder.index(p5)
            root = noteOrder[indexOfFifth-octave]
            third = noteOrder[indexOfRoot]
            indexOfThird = noteOrder.index(m3)
            fifth = noteOrder[indexOfThird]
        chord = [root, third, fifth]
        return chord

def getTempoAndBeat(filename):
    path = filename
    return beat.get_file_bpm(path)

def getTempo(filename):
    return getTempoAndBeat(filename)[0]

def getBeat(filename):
    return getTempoAndBeat(filename)[1]

def beatStrength(filename):
    beats = getBeat(filename)
    maxBeat = -1
    sum = 0
    for b in beats:
        if b > maxBeat:
            maxBeat = b
        sum += b
    avg = sum / len(beats)
    proportion = avg / maxBeat
    proportion *= 9
    proportion = 9 - proportion
    return proportion

