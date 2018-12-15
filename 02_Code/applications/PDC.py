#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2019.
#
# FSE 2019 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FSE 2019 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FSE 2019.  If not, see <http://www.gnu.org/licenses/>.

"""Robot interface combining ultrasonic, LED and motor drivers."""

import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import time
from  FseDevBoard.rgbLed import RGBLED
from  FseDevBoard.buzzer import BUZZER
from  FseDevBoard.hcsr04 import HCSR04, UltrasonicTimeoutError

class PDC(object):
    """ PDC class """
    def __init__(self):
        self.ultrasonic = HCSR04()
        self.rgbled = RGBLED()
        self.buzzer = BUZZER()
        self.rgbled.pwmDriver.setPwmFreq(600)

    def setPDCColor(self, color):
        """ Set RGB color """
        self.rgbled.setRChannelPWM(color[0]/255.0*100)
        self.rgbled.setGChannelPWM(color[1]/255.0*100)
        self.rgbled.setBChannelPWM(color[2]/255.0*100)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        """Release internally used resources."""
        self.ultrasonic.__exit__()
        self.rgbled.__exit__()
        self.buzzer.__exit__()

    @property
    def getDistance(self):
        """Return distance to nearest obstacle in cm or None."""
        try:
            distance = self.ultrasonic.average_distance
        except UltrasonicTimeoutError:
            distance = None
        return distance

    def dist2color(self, dist):
        if dist > 100:
            return (0,0,0)
        elif dist <= 100 and dist > 25:
            return (0,255,0)
        elif dist <=25 and dist > 15:
            arg_r = -25.5 * dist + 637.5
            return (arg_r, 255,0)
        elif dist <=15 and dist> 5:
            arg_g = 25.5 * dist - 127.5
            return  (255,arg_g,0)
        else:
            return (255,0,0)

    @property
    def hex_to_rgb(hex_value):
        r_dec = (hex_value & 0xff0000) >> 16
        g_dec = (hex_value & 0x00ff00) >> 8
        b_dec = (hex_value & 0x0000ff)
        return (r_dec, g_dec, b_dec)

if __name__ == "__main__":
    with PDC() as pdc:
        while True:
            dist = pdc.getDistance
            if dist is not None:
                if dist <=30 and dist >=1:
                    pdc.buzzer.buzzForTime(dist*0.02)
                pdc.setPDCColor(pdc.dist2color(dist))
                print("distance = {0} cm".format(dist))


