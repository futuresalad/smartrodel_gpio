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
        self.filename = "messdaten/csv/imu_data.csv"


    def cont_read(self, duration):

        print("IMU sensor started")
        data_df = pd.DataFrame(columns=['time','gyr_x','gyr_y','gyr_z','acc_x','acc_y','acc_z'])
        data = []
        samplerate = 60
        sampletime = 1/samplerate
        start = time.time()
        lastread = 0
        dt = 0
        duration = 60

        tick = time.time()

        while dt <= duration:
            
            dt =  time.time() - start
            
            if (dt >= (lastread + sampletime)):

                lastread = time.time() - start
                
                try:
                    data1 = self.sensor.get_gyro_data()
                    data2 = self.sensor.get_accel_data()

                except Exception as e:
                    print(e)
                
                finally:
                    data.append([lastread,data1['x'],data1['y'],data1['z'],data2['x'],data2['y'],data2['z']])

        try:
            print("Creating dataframe")
            data_df = pd.DataFrame(data, columns=['time','gyr_x','gyr_y','gyr_z','acc_x','acc_y','acc_z'])
            print("Writing to CSV")
            data_df.to_csv(self.filename, sep=',' , index=None)
            print("CSV finished")

        except Exception as e:
            print(e)