#!/usr/bin/python3

import cProfile
import os
import sys
import time
import threading
import numpy as np
import spidev
import cv2 as cv
from gpiozero import Button, DigitalOutputDevice
from cam import Cam
from sensors import Imu
#from display import Display
import concurrent.futures

print("Entered python script")

# Setting up peripheral objects
#display = Display()
cam = Cam()
#adc = Adc(12)
imu = Imu(0x68)
# Initializing recording time variable
rec_time = 60
rec_started = False

def start_record(rec_time):

        #for t in range(3):
        #        display.splash_image(0.7, 3-t)
        #display.splash_image(0,0)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
        #future_sensor = executor.submit(adc.cont_read, rec_time, 4)
                future_sensor = executor.submit(imu.cont_read, rec_time) #imu
                future_cam = executor.submit(cam.record, rec_time)

                print("Recording started")
                print("Waiting to finish threads")

                concurrent.futures.wait([future_sensor, future_cam], return_when=concurrent.futures.ALL_COMPLETED)
                #concurrent.futures.wait([future_sensor], return_when=concurrent.futures.ALL_COMPLETED)
        
        print("All threads finished")

        rec_started = False
        
        #display.splash_image(0,5)



if __name__ == '__main__':

        print("BTN1 pressed")
        time.sleep(1)
        start_record(rec_time)