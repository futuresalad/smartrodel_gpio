import os
import sys
import time
import smbus
import numpy as np
import spidev
import RPi.GPIO as GPIO

from imusensor.MPU9250 import MPU9250

# GPIO setup
CS_ADC = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_ADC, GPIO.OUT)

class IMU():
    def __init__(self):
        address = 0x68
        bus = smbus.SMBus(1)
        self.imu = MPU9250.MPU9250(bus, address)
        imu.begin()


class ADC():
    def __init__(self):
        
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000

    def read(self, channel):

        adc = self.spi.xfer2([1, (8+channel)<<4, 0]) # 00000001, 1xxx0000, 00000000, xxx is the channel id
        data = ((adc[1]&3) << 8) + adc[2]
        return data


imu = IMU()
adc = ADC()

while True:
	imu.readSensor()
	imu.computeOrientation()

    for channel in range(8):
        print(adc.read(channel))

    print("roll: {0} ; pitch : {1} ; yaw : {2}".format(imu.roll, imu.pitch, imu.yaw))
