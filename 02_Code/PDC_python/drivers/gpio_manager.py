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

"""Bookkeeper for GPIO devices."""

import wiringpi


class GPIO_Manager(object):
    """A manager to bundle bookkeeping work with GPIO pins."""

    devices = []
    # To be implemented by subclasses
    _pins = []

    def __init__(self):
        """Perform GPIO setup if necessary."""
        if not self.devices:
            wiringpi.wiringPiSetupGpio()
        self.devices.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        """Cleanup GPIOs if necessary."""
        self.devices.remove(self)
        for pin in self._pins:
            wiringpi.digitalWrite(pin, wiringpi.LOW)
            wiringpi.pinMode(pin, wiringpi.INPUT)
