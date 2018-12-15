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
import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from smbus2 import SMBus
from gpio_manager import GPIO_Manager
#import os
import time
#import sys
import logging
import math

logger = logging.getLogger(__name__)

class PWM_Driver(GPIO_Manager):
    """ Interface class for PCA9685 """
    # intern registers
    _slaveAddr    = 0x54
    MODE1         = 0x00
    MODE2         = 0x01
    PRESCALE      = 0xFE
    LED0_ON_L     = 0x06
    LED0_ON_H     = 0x07
    LED0_OFF_L    = 0x08
    LED0_OFF_H    = 0x09
    ALL_LED_ON_L  = 0xFA
    ALL_LED_ON_H  = 0xFB
    ALL_LED_OFF_L = 0xFC
    ALL_LED_OFF_H = 0xFD


    # register values
    OUTDRV  = 0x04
    INVRT   = 0x10
    SLEEP   = 0x10
    ALLCALL = 0x01

    def __init__(self):
        super(PWM_Driver, self).__init__()
        self._bus = SMBus(1)
        self.setAllPwm(0, 0)
        self._bus.write_byte_data(self._slaveAddr, self.MODE1, self.ALLCALL)
        self._bus.write_byte_data(self._slaveAddr, self.MODE2, self.OUTDRV)
        time.sleep(0.01)
        mode1 = self._bus.read_byte_data(self._slaveAddr, self.MODE1)
        mode1 = mode1 & (~self.SLEEP)
        self._bus.write_byte_data(self._slaveAddr, self.MODE1, mode1)
        time.sleep(0.01)

    def setPwmFreq(self, freq): #freq in hz[1/s]
        """ Set PWM frequency in Hz"""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        logger.debug('Setting PWM frequency to {0} Hz'.format(freq))
        logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        logger.debug('Final pre-scale: {0}'.format(prescale))
        oldmode = self._bus.read_byte_data(self._slaveAddr, self.MODE1);
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self._bus.write_byte_data(self._slaveAddr, self.MODE1, newmode)  # go to sleep
        self._bus.write_byte_data(self._slaveAddr, self.PRESCALE, prescale)
        self._bus.write_byte_data(self._slaveAddr, self.MODE1, oldmode)
        time.sleep(0.01)
        self._bus.write_byte_data(self._slaveAddr, self.MODE1, oldmode | 0x80)

    def setPwmFromOnAndOffTime (self, channel, on, off):
        """Sets a single PWM channel."""
        self._bus.write_byte_data(self._slaveAddr, self.LED0_ON_L+4*channel, on & 0xFF)
        self._bus.write_byte_data(self._slaveAddr, self.LED0_ON_H+4*channel, on >> 8)
        self._bus.write_byte_data(self._slaveAddr, self.LED0_OFF_L+4*channel, off & 0xFF)
        self._bus.write_byte_data(self._slaveAddr, self.LED0_OFF_H+4*channel, off >> 8)

    def setPwmFromDutyCycle(self, channel, dutyCycle):
        """Set Duty cycle of PWM"""
        if dutyCycle < 0  or dutyCycle > 100:
            raise ValueError("Duty Cycle shall be in between 0% and 100%")
        ontime  = 0
        offtime = int((dutyCycle*4096)/100)-1
        self.setPwmFromOnAndOffTime(channel, ontime, offtime)

    def setAllPwm(self, on, off):
        """ Set all pwm chanels to specified on and off values """
        self._bus.write_byte_data(self._slaveAddr, self.ALL_LED_ON_L, on & 0xFF)
        self._bus.write_byte_data(self._slaveAddr, self.ALL_LED_ON_H, on >> 8)
        self._bus.write_byte_data(self._slaveAddr, self.ALL_LED_OFF_L, on & 0xFF)
        self._bus.write_byte_data(self._slaveAddr, self.ALL_LED_OFF_H, on >> 8)

if __name__ == "__main__":
    with PWM_Driver() as pwm:
        try:
            pwm.setPwmFreq(60)
            while True:
                pwm.setPwmFromDutyCycle(13,  1)
                pwm.setPwmFromDutyCycle(14,  0)
                pwm.setPwmFromDutyCycle(15,  0)
                time.sleep(1)

                pwm.setPwmFromDutyCycle(13,  0)
                pwm.setPwmFromDutyCycle(14,  1)
                pwm.setPwmFromDutyCycle(15,  0)
                time.sleep(1)

                pwm.setPwmFromDutyCycle(13,  0)
                pwm.setPwmFromDutyCycle(14,  0)
                pwm.setPwmFromDutyCycle(15,  1)
                time.sleep(1)

        except KeyboardInterrupt:
            print("Closing ...")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            pwm.setAllPwm(0,0)

