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

"""Driver for a pushbutton."""
import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import time
import wiringpi
from gpio_manager import GPIO_Manager


class PUSHBUTTON(GPIO_Manager):
    """Driver for an LED connected by GPIO."""

    _pin = 25
    _pins = [_pin]

    def __init__(self):
        super(PUSHBUTTON, self).__init__()
        wiringpi.pinMode(self._pin, wiringpi.INPUT)
        self.state = False

    def getPBStatus(self):
        return wiringpi.digitalRead(self._pin)


if __name__ == "__main__":
    with PUSHBUTTON() as PB:
        while True:
            if PB.getPBStatus() == False:
                print("Pushbutton pressed...")
            time.sleep(0.25)
