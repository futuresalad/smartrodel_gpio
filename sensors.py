from mpu6050 import mpu6050
import time
import numpy as np
import spidev
from gpiozero import DigitalOutputDevice
import pandas as pd

class Imu():
    def __init__(self, address):
        
        self.address = address
        self.sensor = mpu6050(self.address)
        self.sample_rate = 50
        self.sample_period = 1/self.sample_rate
        self.filename_gyro = "messdaten/csv/gyro_data.csv"
        self.filename_accel = "messdaten/csv/accel_data.csv"

    def cont_read(self, duration):

        print("IMU sensor started")

        try:
            data_gyro = []
            data_accel = []
            sample_accel = []
            sample_gyro = []
            elapsed_time = 0
            last_reading = 0
            start_time = time.time()

            while (time.time() <= (start_time + duration)):

                current_time = time.time()
                elapsed_time = current_time - last_reading

                if (elapsed_time >= self.sample_period):

                    sample_gyro = self.sensor.get_gyro_data()
                    sample_accel = self.sensor.get_accel_data()
                    last_reading = time.time()

                if last_reading != 0:
                    data_gyro.append([last_reading, sample_gyro['x'], sample_gyro['y'], sample_gyro['z']])
                    data_accel.append([last_reading, sample_accel['x'], sample_accel['y'], sample_accel['z']])         

        except Exception as e:
            print(e)

        
        try:
            print("Writing to dataframe")
            gyro_data_df = pd.DataFrame(data_gyro, columns=['time','x','y','z'])
            accel_data_df = pd.DataFrame(data_accel, columns=['time','x','y','z'])
            
            print("Writing to CSV")
            gyro_data_df.to_csv(self.filename_gyro, sep=',' , index=None)
            accel_data_df.to_csv(self.filename_accel, sep=',' , index=None)
                
        except Exception as e:
            print(e)

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
        self.spi.max_speed_hz=10000000
        self.CS_ADC = DigitalOutputDevice(pin, active_high=False, initial_value=True)
        self.filename = 'messdaten/csv/readings.csv'


    def read(self, channel):

        adc = self.spi.xfer2([1, (8+channel)<<4, 0]) # 00000001, 1xxx0000, 00000000, xxx is the channel id
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def cont_read(self, duration_s, num_channels):
        
        # waiting for all threads to be set up
        print("ADC sensor started")

        df = pd.DataFrame(columns=['time', 'vl', 'vr', 'hl', 'hr'])
        

        sample_rate = 100
        sample_period = 1/sample_rate
        start_time = time.time()
        current_time = start_time
        last_reading = sample_period
        elapsed_time = 0
        data = []
        self.CS_ADC.on()
        
        while (time.time() < (start_time + duration_s)):
        

            current_time = time.time()
            elapsed_time = current_time - last_reading

            try:
                if (elapsed_time >= sample_period):

                    sample = np.zeros(num_channels+1)
                    sample[0] = current_time - start_time
                    

                    tick = time.time()
                    for channel in range(num_channels):
                        
                        sample[channel+1] = self.read(channel)
                        last_reading = time.time()
                    

                    #print(f'duration: {tock - tick}')
                    
                    data.append(sample)

            except Exception as e:
                print(e)
        
        self.CS_ADC.off()

        try:
            data_df = pd.DataFrame(data, columns=['time','vl','vr','hl','hr'])
            data_df.to_csv(self.filename, sep=',' , index=None)

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
