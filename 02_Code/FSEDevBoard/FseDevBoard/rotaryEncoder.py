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

"""Driver for rotary encoder."""
import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import time
import wiringpi as wp
from gpio_manager import GPIO_Manager

counter = 0

class ROTARYENCODER(GPIO_Manager):
    """Interface with a rotary encoder."""

    def __init__(self, clk = 17, dt = 18, sw = 27):
        super(ROTARYENCODER, self).__init__()
        self.encA_pin = clk
        self.encB_pin  = dt
        self.sw_pin  = sw
        self._pins = [self.encA_pin, self.encB_pin, self.sw_pin]

        wp.pinMode(self.encA_pin, wp.INPUT)
        wp.pinMode(self.encB_pin, wp.INPUT)
        wp.pinMode(self.sw_pin  , wp.INPUT)
        wp.pullUpDnControl(self.sw_pin, wp.GPIO.PUD_UP)
        #wp.wiringPiISR(self.sw_pin, wp.GPIO.INT_EDGE_FALLING,self.buttonISR)

        self.flag = 0
        self.lastEncBStatus = 0
        self.currentEncBStatus = 0
        self.buttonPress = False

    def getSWButtonPin(self):
        return self.sw_pin

    def computeEncoder(self):
        global counter
        self.lastEncBStatus = wp.digitalRead(self.encB_pin)
        while(not wp.digitalRead(self.encA_pin)):
            self.currentEncBStatus = wp.digitalRead(self.encB_pin)
            self.flag = 1
        if self.flag == 1:
            self.flag = 0
            if (self.lastEncBStatus == 0) and (self.currentEncBStatus ==1):
                counter = counter + 1
            if (self.lastEncBStatus == 1) and (self.currentEncBStatus ==0):
                counter = counter - 1

    #def buttonISR(channel):
    #    global counter
    #    counter = 0


    def loop(self):
        global counter
        tmp = 0
        while True:
            self.computeEncoder()
            if tmp != counter:
                print('counter = ', counter)
                tmp = counter


    def getCounter(self):
        global counter
        return counter

    def setCounter(self, cnt):
        global counter
        counter = cnt

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self

if __name__ == "__main__":
#    with ROTARYENCODER() as enc:
#       while True:
#            enc.loop()
    enc = ROTARYENCODER()
    print(enc.getSWButtonPin())
    enc.loop()
