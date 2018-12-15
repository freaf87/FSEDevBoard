#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2017.
#
# FSE 2017 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FSE 2017 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FSE 2017.  If not, see <http://www.gnu.org/licenses/>.

"""Driver for a BUZZER."""
import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import time
import wiringpi
from gpio_manager import GPIO_Manager
from time import sleep

class BUZZER(GPIO_Manager):
    """Driver for a BUZZER connected by GPIO."""

    _pin = 17
    _pins = [_pin]

    def __init__(self):
        super(BUZZER, self).__init__()
        wiringpi.pinMode(self._pin, wiringpi.OUTPUT)

    def buzzerHigh(self):
        wiringpi.digitalWrite(self._pin, wiringpi.OUTPUT)

    def buzzerLow(self):
        wiringpi.digitalWrite(self._pin, wiringpi.INPUT)

    def buzzForTime(self, time):
        self.buzzerHigh()
        sleep(time)
        self.buzzerLow()
        sleep(time)

if __name__ == "__main__":
    with BUZZER() as buzzer:
        while True:
            for i in list(range(40,0,-1)):
                print ("distance = {0} cm".format(i))
                if i <= 30 and i >= 1:
                    buzzer.buzzForTime(i*0.02)
                sleep(0.1)
