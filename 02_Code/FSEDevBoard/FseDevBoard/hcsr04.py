#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2019.
#
# FSE 2019 is free software: you can redistribute it and/or modify
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
# along with FSE 2019.  If not, see <http://www.gnu.org/licenses/>.

"""Driver for GPIO ultrasonic sensor."""
import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import time
import wiringpi
from gpio_manager import GPIO_Manager


class UltrasonicTimeoutError(Exception):
    """UltrasonicRanger does not measure response to ping."""


class HCSR04(GPIO_Manager):
    """Interface with an HCSR04 ultrasonic range sensor."""

    _trigger_pin = 15
    _echo_pin = 14
    _pins = [_trigger_pin, _echo_pin]
    _timeout = 0.1  # seconds
    _average_count = 1

    def __init__(self):
        super(HCSR04, self).__init__()
        wiringpi.pinMode(self._trigger_pin, wiringpi.OUTPUT)
        wiringpi.pinMode(self._echo_pin, wiringpi.INPUT)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self

    @property
    def distance(self):
        """Measure time between sent impulse and measured reflectance."""

        def sense_echo_pin_change(initial_state, timeout):
            """Return time at which the echo pin's state changed."""
            while wiringpi.digitalRead(self._echo_pin) == initial_state:
                if time.time() > timeout:
                    raise UltrasonicTimeoutError("No response measured before "
                                                 "timeout.")
            return time.time()

        wiringpi.digitalWrite(self._trigger_pin, wiringpi.INPUT)
        time.sleep(0.000002)
        wiringpi.digitalWrite(self._trigger_pin, wiringpi.OUTPUT)
        time.sleep(0.00001)
        wiringpi.digitalWrite(self._trigger_pin, wiringpi.INPUT)

        timeout_end = time.time() + self._timeout

        start = sense_echo_pin_change(0, timeout_end)
        end = sense_echo_pin_change(1, timeout_end)

        duration = end - start
        distance = duration * 340.0 / 2.0 * 100
        return distance

    @property
    def average_distance(self):
        """Average multiple distance measurements."""
        distance_sum = 0.0
        error_count = 0
        for i in range(self._average_count):
            try:
                distance = self.distance
                distance_sum += distance
            except UltrasonicTimeoutError:
                error_count += 1
            if error_count > min(3, self._average_count) or distance_sum == 0:
                raise UltrasonicTimeoutError("3 consecutive bad soundings.")
        return distance_sum / self._average_count


if __name__ == "__main__":
    with HCSR04() as ultrasonic:
        while True:
            try:
                dis = ultrasonic.average_distance
                print(dis)
            except UltrasonicTimeoutError:
                print("Error during reading.")
            time.sleep(1)
