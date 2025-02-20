from math import sqrt, atan2, degrees, cos, sin

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
    
    def calculateDeltaEModern(self):
        chroma1 =  sqrt((self.a1 ** 2) + (self.b1 ** 2))
        chroma2 =  sqrt((self.a2 ** 2) + (self.b2 ** 2))

        change_light = (self.L1 + self.L2) / 2
        change_chroma = (chroma1 + chroma2) / 2

        chroma_adjust = 0.5 * (1 -  sqrt(max(0, (change_chroma ** 7) / ((change_chroma ** 7) + 25**7))))

        a1_prime = self.a1 * (1 + chroma_adjust)
        a2_prime = self.a2 * (1 + chroma_adjust)

        chroma1_prime =  sqrt((a1_prime ** 2) + (self.b1 ** 2))
        chroma2_prime =  sqrt((a2_prime ** 2) + (self.b2 ** 2))

        change_chroma_prime = (chroma1_prime + chroma2_prime) / 2

        hue1 =  degrees( atan2(self.b1, a1_prime)) if  degrees( atan2(self.b1, a1_prime)) >= 0 else ( degrees( atan2(self.b1, a1_prime)) + 360)
        hue2 =  degrees( atan2(self.b2, a2_prime)) if  degrees( atan2(self.b2, a2_prime)) >= 0 else ( degrees( atan2(self.b2, a2_prime)) + 360)

        hue_angle = ((hue1 + hue2 + 360) / 2) if abs(hue1 - hue2) > 180 else ((hue1 + hue2) / 2)

        hue_rotation_term = 1 - (0.17 *  cos(hue_angle - 30)) + (0.24 *  cos(2 * hue_angle)) + (0.32 *  cos(3 * hue_angle + 6)) - (0.2 *  cos(4 * hue_angle - 63))

        change_hue = hue2 - hue1
        if (abs(hue2 - hue1) > 180) and (hue2 < hue1):
            change_hue += 360
        elif hue2 > hue1:
            change_hue -= 360

        delta_light_prime = self.L2 - self.L1
        delta_chroma_prime = chroma2_prime - chroma1_prime
        delta_hue_angle = 2 * sqrt(max(0, chroma1_prime * chroma2_prime)) * degrees(sin(change_hue / 2))

        s_L = 1 + ((0.015 * ((change_light - 50) ** 2)) / sqrt(20 + ((change_light - 50) ** 2)))
        s_C = 1 + 0.045 * change_chroma_prime
        s_H = 1 + 0.015 * change_chroma_prime * hue_rotation_term

        change_theta = 30 * (2.718 ** (-(((delta_hue_angle - 275) / 25) ** 2)))

        r_C = 2 * sqrt(max(0, (change_chroma ** 7) / ((change_chroma ** 7) + 25**7)))
        r_T = -r_C * degrees(sin(2 * change_theta))

        deltaE = sqrt(
            max(0, (((delta_light_prime) / s_L) ** 2)) +
            max(0, (((delta_chroma_prime) / s_C) ** 2)) +
            max(0, (((delta_hue_angle) / s_H) ** 2)) +
            r_T * max(0, ((delta_chroma_prime) / s_C)) * max(0, ((delta_hue_angle) / s_H))
        )

        return deltaE
