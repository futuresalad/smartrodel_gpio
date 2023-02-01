import os
import sys
import time
import threading
import numpy as np
import spidev
import cv2 as cv
import RPi.GPIO as GPIO
from cam import Cam, progress
from sensors import Adc, Imu

def readSensors(duration_s):

    delay_ns = 20 * 1_000_000
    readcount = 0
    now = time.time_ns()
    starttime = now
    lastread = now
    duration_ns = duration_s * int(1e9)
    imu_vals = []

    while (time.time_ns() < (now + duration_ns)):

        if ((time.time_ns()) - lastread) > delay_ns:
        
            lastread = time.time_ns()
            sensor.imu.readSensor()
            sensor.imu.computeOrientation()
            adc_val = np.zeros(8)
            imu_vals.append([sensor.imu.GyroVals[0], sensor.imu.GyroVals[1], sensor.imu.GyroVals[2]])
            readcount = readcount+1
            
            for channel in range(8):
                adc_val[channel] = adc.read(channel)
    
    print(readcount)


# GPIO setup
CS_ADC = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_ADC, GPIO.OUT)

sensor = Imu()
adc = Adc()
cam = Cam()

duration = 20

prog_thread = threading.Thread(target=progress, args=(duration,))
cam_thread = threading.Thread(target=cam.record, args=(duration,))
sensor_thread = threading.Thread(target=readSensors, args=(duration,))


if __name__ == "__main__":
    
    print("Starting threads")

    cam_thread.start()
    sensor_thread.start()
    prog_thread.start()

    print("Waiting to finish threads")
    
    cam_thread.join()
    sensor_thread.join()
    prog_thread.join()

    print("All threads finished")

