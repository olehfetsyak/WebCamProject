from math import sqrt

class ColorQuantifier:
    def __init__(self, Light1, GreenRed1, YellowBlue1, Light2, GreenRed2, YellowBlue2):
        self.L1 = int(Light1)
        self.a1 = int(GreenRed1)
        self.b1 = int(YellowBlue1)
        
        self.L2 = int(Light2)
        self.a2 = int(GreenRed2)
        self.b2 = int(YellowBlue2)

    def calculateDeltaE(self):
        return sqrt((self.L2 - self.L1) ** 2 + (self.a2 - self.a1) ** 2 + (self.b2 - self.b1) ** 2)