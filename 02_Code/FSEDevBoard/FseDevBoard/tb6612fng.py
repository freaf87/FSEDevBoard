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

"""Driver for 2 TB6612FNG DC motors mounted to a single chassis."""
import sys
import os
from os.path import dirname
sys.path.append(dirname(__file__))

import time
import wiringpi
from gpio_manager import GPIO_Manager


class MotorDriver(GPIO_Manager):
    """Interface with 2 TB6612FNG DC Motor drivers."""
    # Configure motor 1
    _m1_dir1_pin = 19
    _m1_dir2_pin = 16
    _m1_pwm_pin  = 12

    # Configure motor 2
    _m2_dir1_pin = 26
    _m2_dir2_pin = 20
    _m2_pwm_pin = 13

    _standby_pin = 21

    PWM_OUTPUTS = [_m1_pwm_pin, _m2_pwm_pin]

    OUTPUT_PINS = [_m1_dir1_pin, _m1_dir2_pin,
                   _m2_dir1_pin, _m2_dir2_pin,
                   _standby_pin]
    _pins = PWM_OUTPUTS + OUTPUT_PINS

    @staticmethod
    def to_dc(dc):
        return int((1023 * dc) / 100)

    def __init__(self):
        if os.getuid():
            raise RuntimeError("MotorDriver can only be used by sudoer.")
        super(MotorDriver, self).__init__()
        for pin in self.OUTPUT_PINS:
            wiringpi.pinMode(pin, wiringpi.OUTPUT)

        for pin in self.PWM_OUTPUTS:
            wiringpi.pinMode(pin, wiringpi.PWM_OUTPUT)

    def right_forward(self):
        """Drive right motor forward."""
        wiringpi.digitalWrite(self._m1_dir1_pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._m1_dir2_pin, wiringpi.HIGH)

    def right_back(self):
        """Drive right motor back."""
        wiringpi.digitalWrite(self._m1_dir1_pin, wiringpi.HIGH)
        wiringpi.digitalWrite(self._m1_dir2_pin, wiringpi.LOW)

    def left_forward(self):
        """Drive left motor forward."""
        wiringpi.digitalWrite(self._m2_dir1_pin, wiringpi.HIGH)
        wiringpi.digitalWrite(self._m2_dir2_pin, wiringpi.LOW)

    def left_back(self):
        """Drive left motor back."""
        wiringpi.digitalWrite(self._m2_dir1_pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._m2_dir2_pin, wiringpi.HIGH)

    def forward(self, duty_cycle=25):
        """Drive chassis forward."""
        self.right_forward()
        self.left_forward()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def reverse(self, duty_cycle=25):
        """Drive chassis back."""
        self.right_back()
        self.left_back()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def right(self, duty_cycle=25):
        """Turn chassis clockwise."""
        self.right_forward()
        self.left_back()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def left(self, duty_cycle=25):
        """Turn chassis counterclockwise."""
        self.right_back()
        self.left_forward()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def stop(self):
        """Stop chassis."""
        for pin in self.PWM_OUTPUTS:
            wiringpi.pwmWrite(pin, 0)
        for pin in self.OUTPUT_PINS:
            wiringpi.digitalWrite(pin, wiringpi.LOW)

    def __exit__(self, *args):
        wiringpi.pwmWrite(self._m1_pwm_pin, 0)
        wiringpi.pwmWrite(self._m2_pwm_pin, 0)
        super(MotorDriver, self).__exit__()


if __name__ == '__main__':
    with MotorDriver() as tb6612fng:
        while True:
            print("forward")
            tb6612fng.forward(50)
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print("reverse")
            tb6612fng.reverse(50)
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print("left")
            tb6612fng.left(50)
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print("right")
            tb6612fng.right(50)
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print("Done!")
