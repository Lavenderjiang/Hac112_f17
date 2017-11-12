import math, decimal
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
        Gmin = 195
    else:
        Gmax = 61
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
    return ((Rmin, Rmax), (Gmin, Gmax), (Bmin, Bmax))



    
    
class ColorDots (object):
    
    cOctaves = (16.35, 32.70, 65.41, 130.81, 261.63, 523.25, 1046.50	, 2093, 4186)
    numOctaves = len(cOctaves)

    def __init__(self, freq, amp):
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
        self.color = (str(red) +"-"+ str(green) +"-"+ str(blue))
        return self.color
###
#remove
#just for show
colorRanges = colorRange(3, 201, False)
dot = ColorDots(70, 40) #freq, amp
print (dot.color(colorRanges))