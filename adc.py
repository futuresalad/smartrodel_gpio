import time
import numpy as np
import spidev
import RPi.GPIO as GPIO

CS_ADC = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_ADC, GPIO.OUT)

# MCP3008 Pinout
# CH0 -|1 * 16|- VDD
# CH1 -|2   15|- Vref
# CH2 -|3   14|- AGND
# CH3 -|4   13|- CLK
# CH4 -|5   12|- Dout
# CH5 -|6   11|- Din
# CH6 -|7   10|- CS
# CH7 -|8 __ 9|- DGND

# Raspberry Pi Pinout
# CS -> GPIO25 (Pin 22)
# VDD -> VREF 3.3V (Pin 17)
# AGND, DGND -> GND (Pin 25, 20)
# MOSI -> GPIO10 (Pin 19)
# MISO -> GPIO9 (Pin 21)
# CLK -> GPIO11 (Pin 23)


class ADC():
    def __init__(self):
        
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000

    def read(self, channel):

        adc = self.spi.xfer2([1, (8+channel)<<4, 0]) # 00000001, 1xxx0000, 00000000, xxx is the channel id
        data = ((adc[1]&3) << 8) + adc[2]
        return data

adc = ADC()

if __name__ == "__main__":

    print("reading for 10 seconds")
    
    for reading in range(100):
        GPIO.output(CS_ADC, GPIO.LOW)
        print(adc.read(0))
        GPIO.output(CS_ADC, GPIO.HIGH)
        time.sleep(0.1)
