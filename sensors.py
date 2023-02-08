import smbus
from imusensor.MPU9250 import MPU9250
import time
import numpy as np
import spidev
from gpiozero import DigitalOutputDevice
import pandas as pd

class Imu():
    def __init__(self):
        address = 0x68
        bus = smbus.SMBus(1)
        self.imu = MPU9250.MPU9250(bus, address)
        self.imu.begin()

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

class Adc():
    def __init__(self, pin):
        
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000
        self.CS_ADC = DigitalOutputDevice(pin, active_high=False, initial_value=True)

    def read(self, channel):

        adc = self.spi.xfer2([1, (8+channel)<<4, 0]) # 00000001, 1xxx0000, 00000000, xxx is the channel id
        data = ((adc[1]&3) << 8) + adc[2]
        print("and here")
        return data

    def cont_read(self, duration_s, num_channels):
        
        # waiting for all threads to be set up
        print("ADC sensor started")

        df = pd.DataFrame(columns=['time', 'vl', 'vr', 'hl', 'hr'])
        

        sample_rate = 100
        sample_period = (1/sample_rate)
        start_time = time.time()
        last_reading = start_time
        
        while (time.time() < (start_time + duration_s)):

            current_time = time.time()
            elapsed_time = current_time - last_reading
            try:
                if (elapsed_time >= sample_period):

                    data = np.zeros(num_channels+1)
                    data[0] = current_time
                    for channel in range(num_channels):
                        
                        self.CS_ADC.on()
                        data[channel] = self.read(channel)
                        self.CS_ADC.off()
                        last_reading = time.time()


            except Exception as e:
                print(e)


                    

if __name__ == "__main__":
    adc = Adc(12)
    print("reading for 10 seconds")
    
    for reading in range(5000):
        CS_ADC.off()
        print(adc.read(0))
        CS_ADC.on()
        time.sleep(0.02)
