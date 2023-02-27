#!/usr/bin/python3

from mpu6050 import mpu6050
import time
import numpy as np
import spidev
from gpiozero import DigitalOutputDevice
import pandas as pd

class Imu():
    def __init__(self, address):
        
        # IMU config
        self.address = address
        self.sensor = mpu6050(self.address)

        # SPI ADC config
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000
        self.CS_ADC = DigitalOutputDevice(12, active_high=False, initial_value=False)
        self.num_channels = 4

    def adc_read(self, buffer):


        for channel in range(self.num_channels):
            self.CS_ADC.on()
            adc = self.spi.xfer2([1,(8+channel)<<4,0])
            buffer[channel] = ((((adc[1]&3) << 8) + adc[2]))
            self.CS_ADC.off()

        return buffer

    def cont_read(self, duration, rec_number):

        print("Sensors started")
        data = []
        dist_data = np.zeros(4)
        samplerate = 100
        sampletime = 1/samplerate
        start = time.time()
        lastread = 0
        dt = 0

        tick = time.time()

        while dt <= duration:
            
            dt =  time.time() - start
            
            if (dt >= (lastread + sampletime)):

                lastread = time.time() - start
                
                try:
                    tick = time.time()
                    imu_data1 = self.sensor.get_gyro_data()
                    imu_data2 = self.sensor.get_accel_data()
                    dist_data = self.adc_read(dist_data)
                    #print(time.time()-tick)
                
                except Exception as e:
                    print(e)
                
                finally:
                    try:
                        data.append([lastread, dist_data[0], dist_data[1], dist_data[2], dist_data[3], imu_data1['x'], imu_data1['y'], imu_data1['z'],imu_data2['x'],imu_data2['y'],imu_data2['z']])
                    except Exception as e:
                        print(e)
        try:
            print("Creating dataframe")
            data_df = pd.DataFrame(data, columns=['time','vl','vr','hl','hr','gyr_x','gyr_y','gyr_z','acc_x','acc_y','acc_z'])
            print("Writing to CSV")


            filename = f"~/smartrodel_gpio/messdaten/csv/sensor_data_{rec_number}.csv"
            data_df.to_csv(filename, sep=',' , index=None)
            print("CSV finished")

        except Exception as e:
            print(e)