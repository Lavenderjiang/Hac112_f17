import math, decimal
import random
from tkinter import *
from PIL import ImageTk, Image
from workingaubio import *
####################################
# helper
####################################

#from 112 website-- https://www.cs.cmu.edu/~112/schedule.html
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

###
#color range
###
def colorRange(strength, tempo, major):
    if major == True:
        Gmax = 255
        Gmin = 130
    else:
        Gmax = 120
        Gmin = 1
    
    Rmin = (strength+.1)*256//13
    Rmax = (strength+3.9)*256//13
    
    
    if tempo > 250:
        Bmax = 255
        Bmin = 244
    elif tempo < 50:
        Bmax = 11
        Bmin = 1
    else:
        Bmin = 256*(tempo-50)//250 +1
        Bmax = 256*(tempo)//250-1
    print(((Rmin, Rmax), (Gmin, Gmax), (Bmin, Bmax)))
    return ((Rmin, Rmax), (Gmin, Gmax), (Bmin, Bmax))



    
    
class ColorDots (object):
    
    cOctaves = (16.35, 32.70, 65.41, 130.81, 261.63, 523.25, 1046.50	, 2093, 4186)
    numOctaves = len(cOctaves)

    def __init__(self, freq, amp = 3):
        self.freq = freq #color
        self.amp = amp #size

    def octave(self):
        if self.freq < ColorDots.cOctaves[0]:
            
            self.octaves = -1
            
        elif self.freq >= ColorDots.cOctaves[-1]:
            self.octaves = 9
        else:
            for i in range(1, ColorDots.numOctaves):
                if self.freq < ColorDots.cOctaves[i]:
                    self.octaves = i-1
                    return
                    
    
    def freqPitch(self):
        self.octave()
        if self.octaves == -1:
            self.pitch = (-1, 0)
            return
        elif self.octaves == 9:
            self.pitch = (12, 0)
            return
        self.cents = 1200*math.log(self.freq/(ColorDots.cOctaves[self.octaves])
                            ,2)
        if self.cents >= 1150:
            # (0, 0-4)
            self.pitch = (0, self.cents%100)
        #returns (0-11, cents 5-120
        else:
            self.pitch = (roundHalfUp(self.cents/100), self.cents%100 +50)
        


    def color(self, colorRanges):
        self.octave()
        self.freqPitch()
        self.redRange = colorRanges[0]
        self.greenRange = colorRanges[1]
        self.blueRange = colorRanges[2]
        
        if self.pitch[0] == -1:
            red = (self.redRange[0]-1)
            green = (self.greenRange[0]-1)
            blue = (self.blueRange[0]-1)
            
        elif self.pitch[0] == 12:
            red = (self.redRange[1]+1)
            green = (self.greenRange[1]+1)
            blue = (self.blueRange[1]+1)
        else:
            red = ((self.pitch[0]/12+ self.pitch[1]/1200 )*(self.redRange[1]-self.redRange[0]) +
                self.redRange[0])
            green = ((self.pitch[0]/12 + self.pitch[1]/1200)*(self.greenRange[1]-self.greenRange[0]) +
                self.greenRange[0])
            blue = ((self.pitch[0]/12 + self.pitch[1]/1200)*(self.blueRange[1]-self.blueRange[0]) +
                self.blueRange[0])
        
        red = int(red)
        blue = int(blue)
        green = int(green)
        return [red, green, blue]

###
#tkinter
###

def init(data):
    data.filename = "br-mi.wav"
    data.colorRanges = colorRange(beatStrength(data.filename), getTempo(data.filename), False)
    data.dots = []
    for freq in detect(data.filename):
        data.dots.append(ColorDots(freq))
    data.x = 0
    data.y = 0

def mousePressed(event, data):
    pass
    
def keyPressed(event, data):
    pass   

def timerFired(data):
    pass

def redrawAll(canvas, data):
    for dot in data.dots:
        data.x = random.randint(0, data.width)
        data.y = random.randint(0, data.height)
        col = (dot.color(data.colorRanges)[0], dot.color(data.colorRanges)[1], dot.color(data.colorRanges)[2])
        hexCol = '#%02x%02x%02x' % col
        canvas.create_oval(data.x - 3, data.y - 3, data.x + 3, data.y + 3, fill = hexCol, width = 0)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#run(400, 400)

#This creates the main window of an application
window = Tk()
window.title("Join")
window.geometry("300x300")
window.configure(background='White')

path = "p1.jpg"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Start the GUI
window.mainloop()

###
#remove
#just for show
filename = "br-mi.wav"
colorRanges = colorRange(beatStrength(filename), getTempo(filename), False)
dot = ColorDots(70) #freq, amp
print (dot.color(colorRanges))