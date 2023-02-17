#!/usr/bin/python
 
import spidev
import time
import os
from gpiozero import DigitalOutputDevice 

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
CS_ADC = DigitalOutputDevice(12, active_high=False, initial_value=False)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    CS_ADC.on()
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = (((adc[1]&3) << 8) + adc[2])
    CS_ADC.off()
    return data

while True:
    tick = time.time()
    # Read the light sensor data
    print(ReadChannel(0))
    print(time.time()- tick)
 
 