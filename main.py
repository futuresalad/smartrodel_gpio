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

# Button callback functions
def btn1_callback():
        global rec_time
        start_record(rec_time)
        

def btn2_callback():
        pass        

def btn3_callback():
        pass

# Raspberry GPIO config
BTN_1 = 14
BTN_2 = 15
BTN_3 = 18

BTN_1 = Button(14, pull_up=True)
BTN_2 = Button(15, pull_up=True)
BTN_3 = Button(18, pull_up=True)

BTN_1.when_pressed = btn1_callback
BTN_2.when_pressed = btn2_callback
BTN_3.when_pressed = btn3_callback

#display.splash_image(1,6)
#display.splash_image(1,5)

while True:
        pass