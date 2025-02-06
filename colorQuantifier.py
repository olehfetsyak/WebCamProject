from math import sqrt

class ColorQuantifier:
    def __init__(self, Light1, GreenRed1, YellowBlue1, Light2, GreenRed2, YellowBlue2):
        self.L1 = Light1
        self.a1 = GreenRed1
        self.b1 = YellowBlue1
        
        self.L2 = Light2
        self.a2 = GreenRed2
        self.b2 = YellowBlue2

    def calculateDeltaE(self):
        return sqrt((self.L2 - self.L1) ** 2 + (self.a2 - self.a1) ** 2 + (self.b2 - self.b1) ** 2)