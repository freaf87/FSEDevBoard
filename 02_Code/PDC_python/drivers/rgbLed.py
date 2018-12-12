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


from gpio_manager import GPIO_Manager
from PCA9685 import PWM_Driver
import os
import time
import sys
import logging

logger = logging.getLogger(__name__)

class RGB_LED(GPIO_Manager):
    """ Interface class for FSEDevBoard onboard LED """
    def __init__(self):
        super(RGB_LED, self).__init__()
        self._RChannel = 13
        self._GChannel = 14
        self._BChannel = 15
        self.pwmDriver = PWM_Driver()

    def setRChannelPWM(self,dutyCycle):
        self.pwmDriver.setPwmFromDutyCycle(self._RChannel, dutyCycle)

    def setGChannelPWM(self,dutyCycle):
        self.pwmDriver.setPwmFromDutyCycle(self._GChannel, dutyCycle)

    def setBChannelPWM(self,dutyCycle):
        self.pwmDriver.setPwmFromDutyCycle(self._BChannel, dutyCycle)

    def setRGBDutycycles(self, dutyCycleRChannel, dutyCycleGChannel, dutyCycleBChannel):
        self.setRChannelPWM(dutyCycleRChannel)
        self.setGChannelPWM(dutyCycleGChannel)
        self.setBChannelPWM(dutyCycleBChannel)

if __name__ == "__main__":
     with RGB_LED() as rgbLed:
         try:
             rgbLed.pwmDriver.setPwmFreq(60)
             while True:
                    rgbLed.setRGBDutycycles(2, 0, 0)
                    time.sleep(0.5)

                    rgbLed.setRGBDutycycles(0, 2, 0)
                    time.sleep(0.5)

                    rgbLed.setRGBDutycycles(0, 0, 2)
                    time.sleep(0.5)

         except KeyboardInterrupt:
            print(" Closing ...")
         except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
         finally:
             rgbLed.pwmDriver.setAllPwm(0,0)

