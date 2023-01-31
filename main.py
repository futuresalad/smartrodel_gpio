import os
import sys
import time
import threading
import smbus
import numpy as np
import spidev
import cv2 as cv
import RPi.GPIO as GPIO

from imusensor.MPU9250 import MPU9250

# GPIO setup
CS_ADC = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_ADC, GPIO.OUT)

class CAM():
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.writer = cv.VideoWriter('testvid.mp4', fourcc, 30, (width, height))

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

delay = 2 * 1_000_000 
starttime = time.time_ns()
lastread = starttime
readcount = 0

while True:
    
    # Capture frame-by-frame
    ret, frame = cam.cap.read()
    
    # write frame to file    
    cam.writer.write(frame)
    
    # Display the resulting frame
    #cv.imshow('frame', frame)
    
    if cv.waitKey(1) == ord('q'):
        break
        
    if ((time.time_ns()) - lastread) > delay:
        
        lastread = time.time_ns()
        seconds = ((lastread-starttime) / 1_000_000_000)
        sensor.imu.readSensor()
        sensor.imu.computeOrientation()
        adc_val = np.zeros(8)
        
        readcount = readcount+1
        
        for channel in range(8):
            adc_val[channel] = adc.read(channel)
        
        #print(adc_val)
        #print("roll: {0} ; pitch : {1} ; yaw : {2}".format(sensor.imu.roll, sensor.imu.pitch, sensor.imu.yaw))
        if seconds > 10:
            print(f'readcount: {readcount}')
            break
cam.cap.release()
cam.writer.release()
cv.destroyAllWindows()