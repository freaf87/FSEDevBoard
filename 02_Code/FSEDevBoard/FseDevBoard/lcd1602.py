#!/usr/bin/env python

import time
import smbus2 as smbus

class LCD1602():
    """ Driver for a 1602 LCD"""
    def __init__(self, addr):
        self.bus = smbus.SMBus(1)
        self.BLEN = 1
        self.LCD_ADDR = addr
        self.sendCmd(0x33) # Must initialize to 8-line mode at first
        time.sleep(0.005)
        self.sendCmd(0x32) # Then initialize to 4-line mode
        time.sleep(0.005)
        self.sendCmd(0x28) # 2 Lines & 5*7 dots
        time.sleep(0.005)
        self.sendCmd(0x0C) # Enable display without cursor
        time.sleep(0.005)
        self.sendCmd(0x01) # Clear Screen
        self.bus.write_byte(self.LCD_ADDR, 0x08)

    def writeWord(self, addr, data):
        temp = data
        if (self.BLEN == 1):
            temp |= 0x08
        else:
            temp &= 0xF7
        self.bus.write_byte(addr ,temp)


    def sendCmd(self, cmd):
        # Send bit7-4 firstly
        buf = cmd & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.writeWord(self.LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.writeWord(self.LCD_ADDR ,buf)

        # Send bit3-0 secondly
        buf = (cmd & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.writeWord(self.LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.writeWord(self.LCD_ADDR ,buf)

    def sendData(self, data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.writeWord(self.LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.writeWord(self.LCD_ADDR ,buf)

        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.writeWord(self.LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.writeWord(self.LCD_ADDR ,buf)


    def clearLcd(self):
        self.sendCmd(0x01)# clear display

    def enableBackLight(self):
        self.bus.write_byte(0x27, 0x08)
        self.bus.close()

    def write(self, x, y, str):
        if x < 0:
            x= 0
        if x > 15:
            x= 15
        if y < 0:
            x= 0
        if x > 1:
            x= 1
        #Move Cursor
        addr = 0x80 + 0x40*y +x
        self.sendCmd(addr)
        for chr in str:
            self.sendData(ord(chr))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self


if __name__ == '__main__':
    with LCD1602(0x27) as lcd:
        lcd.write(0, 0, 'Welcome')
        lcd.write(0, 1, 'Press to start')
