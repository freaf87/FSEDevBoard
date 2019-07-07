#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2020.
#
# FSE 2020 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FSE 2020 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FSE 2020.  If not, see <http://www.gnu.org/licenses/>.

import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import time
import wiringpi as wp
from FseDevBoard.rgbLed import RGBLED
from FseDevBoard.buzzer import BUZZER
from FseDevBoard.lcd1602 import LCD1602
from FseDevBoard.rotaryEncoder import ROTARYENCODER

buttonPressed = False

class STUDATTENDANCE(object):
    """ Student Attendance Program """
    def __init__(self):
        self.rgbled = RGBLED()
        self.buzzer = BUZZER(4)
        self.rgbled.pwmDriver.setPwmFreq(600)
        self.lcd = LCD1602(0x27)
        self.rotEnc = ROTARYENCODER()

        wp.wiringPiISR(self.rotEnc.getSWButtonPin(), wp.GPIO.INT_EDGE_FALLING,self.buttonISR)

    def setLEDColor(self, color):
        """ Set RGB color """
        self.rgbled.setRChannelPWM(color[0]/255.0*100)
        self.rgbled.setGChannelPWM(color[1]/255.0*100)
        self.rgbled.setBChannelPWM(color[2]/255.0*100)

    def buttonISR(channel):
        global buttonPressed
        buttonPressed = True
        #print("bottonPressed")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        """Release internally used resources."""
        self.rgbled.__exit__()
        self.buzzer.__exit__()
        self.lcd.__exit__()

if __name__ == "__main__":
    global buttonPressed

    with STUDATTENDANCE() as studAtt:

        studAtt.lcd.clearLcd()
        studAtt.lcd.write(0, 0, 'Welcome')
        studAtt.lcd.write(0, 1, 'Press to start')
        tmpCounter = 0
        while True:
            studAtt.setLEDColor((0, 255, 0))
            studAtt.rotEnc.computeEncoder()
            if (tmpCounter != studAtt.rotEnc.getCounter()):
                studAtt.lcd.write(0, 0, str(studAtt.rotEnc.getCounter()))
                print('counter = ', studAtt.rotEnc.getCounter())
                tmpCounter = studAtt.rotEnc.getCounter()
            if buttonPressed == True:
                buttonPressed = False
                studAtt.lcd.clearLcd()
                studAtt.rotEnc.setCounter(0)
                studAtt.lcd.write(0, 0, str(studAtt.rotEnc.getCounter()))

